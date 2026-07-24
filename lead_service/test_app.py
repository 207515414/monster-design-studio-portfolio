import unittest

from lead_service.app import LeadStore, ValidationError, validate_lead


def valid_payload(email="studio@example.com"):
    return {
        "email": email,
        "service": "rendering",
        "brief": "Need two interior images for a hospitality proposal.",
    }


class LeadValidationTests(unittest.TestCase):
    def test_valid_lead_is_normalized(self):
        lead = validate_lead({"email": "  studio@example.com ", "service": "rendering", "brief": " Need two interior images. "})
        self.assertEqual(lead["email"], "studio@example.com")
        self.assertEqual(lead["brief"], "Need two interior images.")

    def test_missing_required_fields_are_rejected(self):
        with self.assertRaises(ValidationError):
            validate_lead({"email": "", "service": "", "brief": ""})

    def test_honeypot_and_oversized_brief_are_rejected(self):
        with self.assertRaises(ValidationError):
            validate_lead({**valid_payload(), "company_website": "bot"})
        with self.assertRaises(ValidationError):
            validate_lead({**valid_payload(), "brief": "x" * 5001})


class LeadStoreTests(unittest.TestCase):
    def test_store_assigns_identifier_and_lists_newest_first(self):
        store = LeadStore(":memory:")
        first = store.insert(valid_payload("first@example.com"), "127.0.0.1")
        second = store.insert(valid_payload("second@example.com"), "127.0.0.1")
        self.assertLess(first["id"], second["id"])
        self.assertEqual(store.list_leads()[0]["email"], "second@example.com")


if __name__ == "__main__":
    unittest.main()
