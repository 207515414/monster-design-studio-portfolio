/* No analytics vendor, storage or consent assumption. Integrate with an approved CMP. */
(() => {
  function track(name, source = location.pathname) {
    if (window.monsterAnalyticsConsent !== true || typeof window.gtag !== 'function') return;
    const path = /^\/[a-zA-Z0-9/_-]{0,200}$/.test(source) ? source : '/';
    window.gtag('event', name, { source_page: path, page_location: location.origin + location.pathname, page_referrer: '' });
  }
  window.monsterTrack = track;
  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    const url = new URL(link.href, location.href);
    if (url.protocol === 'mailto:') track('email_click');
    else if (url.hostname === 'wa.me') track('whatsapp_click');
    else if (url.origin === location.origin && url.pathname === '/contact/') track('quote_click');
  });
})();
