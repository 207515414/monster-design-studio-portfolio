import json
import os
import tempfile
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from unittest.mock import patch
from server import quote


class QuoteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, {'SMTP_HOST': 'test', 'SMTP_USER': 'test', 'SMTP_PASSWORD': 'test', 'SMTP_FROM': 'test@example.com', 'QUOTE_RATE_SECRET': 'test-only', 'QUOTE_RATE_DB': self.tmp.name + '/rate.db'})
        self.env.start()
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), quote.Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.data = dict(company='Architecture Studio', email='designer@example.com', service='Interior Rendering', quantity='3', deadline='', message='Living room and kitchen views for client review.', website='', source='/portfolio/shanghai-duplex/')

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.env.stop()
        self.tmp.cleanup()

    def request(self, data=None, origin='https://monster-cg.com', path='/api/quote', method='POST', raw=None):
        connection = HTTPConnection(*self.server.server_address, timeout=5)
        connection.request(method, path, raw if raw is not None else json.dumps(self.data if data is None else data), {'Origin': origin, 'Content-Type': 'application/json'})
        response = connection.getresponse()
        status, body = response.status, json.loads(response.read())
        connection.close()
        return status, body

    def test_only_confirmed_smtp_acceptance_reports_success(self):
        with patch.object(quote, 'send_mail') as send:
            status, body = self.request()
            self.assertEqual(status, 200)
            self.assertTrue(body['success'])
            self.assertEqual(send.call_args.args[0]['source'], '/portfolio/shanghai-duplex/')

    def test_smtp_failure_never_reports_success(self):
        with patch.object(quote, 'send_mail', side_effect=OSError('private credential error')):
            status, body = self.request()
            self.assertEqual(status, 502)
            self.assertNotIn('success', body)
            self.assertNotIn('private', body['message'])

    def test_missing_configuration_fails_closed(self):
        with patch.dict(os.environ, {'SMTP_PASSWORD': ''}):
            self.assertEqual(self.request()[0], 503)
            self.assertFalse(self.request(path='/api/quote/status', method='GET')[1]['available'])

    def test_validation_and_header_injection(self):
        for field, value in [('email', 'x@example.com\r\nBcc: victim@example.com'), ('service', 'Unknown'), ('quantity', '-1'), ('quantity', '1001'), ('deadline', '2020-01-01'), ('message', 'short'), ('website', 'spam')]:
            with self.subTest(field=field, value=value):
                with self.assertRaises(ValueError):
                    quote.validate({**self.data, field: value})
        self.assertEqual(quote.validate({**self.data, 'source': '/?email=private'})['source'], '/contact/')

    def test_invalid_json_origin_and_size_do_not_send(self):
        with patch.object(quote, 'send_mail') as send:
            self.assertEqual(self.request(raw='{')[0], 400)
            self.assertEqual(self.request(origin='https://attacker.example')[0], 403)
            self.assertEqual(self.request(raw='a' * 17000)[0], 413)
            send.assert_not_called()

    def test_rate_limit_is_persistent_and_expires(self):
        for _ in range(5):
            self.assertTrue(quote.allow_request('127.0.0.1', 10000))
        self.assertFalse(quote.allow_request('127.0.0.1', 10001))
        self.assertTrue(quote.allow_request('127.0.0.2', 10001))
        self.assertTrue(quote.allow_request('127.0.0.1', 13601))

    def test_recipient_is_fixed_and_tls_is_used(self):
        with patch.object(quote.smtplib, 'SMTP') as smtp:
            smtp.return_value.__enter__.return_value = smtp.return_value
            smtp.return_value.send_message.return_value = {}
            quote.send_mail(quote.validate(self.data))
            smtp.return_value.starttls.assert_called_once()
            mail = smtp.return_value.send_message.call_args.args[0]
            self.assertEqual(mail['To'], 'zhangzheng270@gmail.com')
            self.assertEqual(mail['Reply-To'], 'designer@example.com')


if __name__ == '__main__':
    unittest.main()
