(() => {
  const form = document.querySelector('#quote-form');
  if (!form) return;
  const status = document.querySelector('#quote-status');
  const submit = form.querySelector('button[type="submit"]');
  let source = '/contact/';
  try {
    const previous = new URL(document.referrer);
    if (previous.origin === location.origin) source = previous.pathname;
  } catch { /* Direct visitor. */ }
  const show = (message, state) => { status.textContent = message; status.dataset.state = state; };
  async function availability() {
    try {
      const response = await fetch('/api/quote/status', { cache: 'no-store', signal: AbortSignal.timeout(10000) });
      if (!response.ok || !(await response.json()).available) throw new Error();
      submit.disabled = false;
      show('Ready to send. Please do not include confidential files or passwords.', 'ready');
    } catch {
      show('The online form is currently unavailable. Please use the email or WhatsApp links above.', 'error');
    }
  }
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity() || submit.disabled) return;
    form.querySelectorAll('[aria-invalid]').forEach((field) => field.removeAttribute('aria-invalid'));
    submit.disabled = true;
    form.setAttribute('aria-busy', 'true');
    show('Sending your inquiry…', 'pending');
    try {
      const data = Object.fromEntries(new FormData(form));
      data.source = source;
      const response = await fetch('/api/quote', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data), signal: AbortSignal.timeout(85000) });
      const result = await response.json();
      if (!response.ok || result.success !== true) {
        if (['company', 'email', 'service', 'quantity', 'deadline', 'message'].includes(result.field)) {
          const field = form.elements.namedItem(result.field);
          field?.setAttribute('aria-invalid', 'true');
          field?.focus();
        }
        throw new Error(result.message || 'We could not confirm sending. Please use email or WhatsApp.');
      }
      show(result.message, 'success');
      window.monsterTrack?.('quote_submit_success', source);
      form.reset();
      submit.textContent = 'Inquiry sent';
      // Keep disabled after success to prevent accidental duplicate submission.
    } catch (error) {
      show(error instanceof SyntaxError || error.name === 'TimeoutError' || error.name === 'TypeError' ? 'We could not confirm sending. Please contact us by email or WhatsApp before retrying.' : error.message, 'error');
      submit.disabled = false;
    } finally {
      form.removeAttribute('aria-busy');
    }
  });
  availability();
})();
