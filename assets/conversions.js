/* Basic consent: no Google script or analytics requests before opt-in. */
(() => {
  const consentKey = 'monster-analytics-consent-v1';
  const maxAge = 180 * 24 * 60 * 60 * 1000;
  const events = new Set(['quote_click', 'quote_submit_success', 'email_click', 'whatsapp_click']);
  let measurementId = '';
  let loaded = false;
  let panel;
  let settings;
  window.monsterAnalyticsConsent = false;
  const cleanPath = value => /^\/[a-zA-Z0-9/_-]{0,200}$/.test(value) ? value : '/';
  const parameters = source => ({
    source_page: cleanPath(source),
    page_location: location.origin + cleanPath(location.pathname),
    page_referrer: '',
    page_title: document.title
  });
  function track(name, source = location.pathname) {
    if (!events.has(name) || !measurementId || window.monsterAnalyticsConsent !== true || typeof window.gtag !== 'function') return;
    window.gtag('event', name, parameters(source));
  }
  window.monsterTrack = track;
  document.addEventListener('click', event => {
    const link = event.target.closest?.('a[href]');
    if (!link) return;
    const url = new URL(link.href, location.href);
    if (url.protocol === 'mailto:') track('email_click');
    else if (url.hostname === 'wa.me') track('whatsapp_click');
    else if (url.origin === location.origin && url.pathname === '/contact/') track('quote_click');
  });
  function remember(choice) {
    try { localStorage.setItem(consentKey, JSON.stringify({ choice, time: Date.now() })); } catch { /* Consent applies only to this page if storage is blocked. */ }
  }
  function remembered() {
    try {
      const value = JSON.parse(localStorage.getItem(consentKey));
      if (['accepted', 'rejected'].includes(value?.choice) && Number.isFinite(value.time) && Date.now() >= value.time && Date.now() - value.time < maxAge) return value.choice;
    } catch { /* Invalid or unavailable storage defaults to no consent. */ }
    return null;
  }
  function removeAnalyticsCookies() {
    for (const cookie of document.cookie.split(';')) {
      const name = cookie.split('=')[0].trim();
      if (name !== '_ga' && !name.startsWith('_ga_')) continue;
      // New cookies are host-only; also remove any legacy parent-domain cookies.
      document.cookie = `${name}=; Max-Age=0; Path=/; SameSite=Lax`;
      const parts = location.hostname.split('.');
      for (let i = 0; i < parts.length - 1; i++) {
        document.cookie = `${name}=; Max-Age=0; Path=/; Domain=${parts.slice(i).join('.')}; SameSite=Lax`;
      }
    }
  }
  function accept(save = true) {
    if (navigator.globalPrivacyControl === true) return;
    if (save) remember('accepted');
    panel.hidden = true;
    window.monsterAnalyticsConsent = true;
    window['ga-disable-' + measurementId] = false;
    if (loaded) return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
    window.gtag('consent', 'update', { analytics_storage: 'granted' });
    window.gtag('js', new Date());
    window.gtag('config', measurementId, {
      send_page_view: false,
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      cookie_domain: 'none',
      cookie_expires: 15552000,
      ...parameters(location.pathname)
    });
    window.gtag('event', 'page_view', parameters(location.pathname));
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(measurementId);
    document.head.appendChild(script);
  }
  function reject(save = true) {
    if (save) remember('rejected');
    window.monsterAnalyticsConsent = false;
    window['ga-disable-' + measurementId] = true;
    removeAnalyticsCookies();
    panel.hidden = true;
    settings.focus();
    // Unload the already-initialized tag; the next page respects the stored refusal.
    if (loaded) location.reload();
  }
  function mount() {
    const style = document.createElement('link');
    style.rel = 'stylesheet';
    style.href = '/assets/analytics-consent.css?v=20261018';
    document.head.appendChild(style);
    panel = document.createElement('section');
    panel.className = 'analytics-consent';
    panel.setAttribute('aria-labelledby', 'analytics-consent-title');
    panel.innerHTML = '<h2 id="analytics-consent-title">Optional website analytics</h2><p>With your permission, we use Google Analytics to understand page visits and inquiry actions. We do not send form contents or email addresses in these events. You can decline and still use the website and inquiry form.</p><a href="/privacy-policy/">Privacy Policy</a><div class="analytics-consent-actions"><button type="button" data-consent="reject">Reject analytics</button><button type="button" data-consent="accept">Accept analytics</button></div>';
    panel.querySelector('[data-consent="reject"]').addEventListener('click', () => reject());
    panel.querySelector('[data-consent="accept"]').addEventListener('click', () => accept());
    settings = document.createElement('button');
    settings.type = 'button';
    settings.className = 'analytics-settings';
    settings.textContent = 'Privacy choices';
    settings.addEventListener('click', () => { panel.hidden = false; panel.querySelector('button').focus(); });
    (document.querySelector('footer') || document.body).appendChild(settings);
    document.body.appendChild(panel);
    if (navigator.globalPrivacyControl === true) {
      panel.querySelector('p').textContent = 'Your browser requests privacy protection. Optional analytics is disabled. You can use the website and inquiry form normally.';
      panel.querySelector('[data-consent="accept"]').disabled = true;
      panel.hidden = true;
      removeAnalyticsCookies();
    } else if (remembered() === 'accepted') accept(false);
    else if (remembered() === 'rejected') { panel.hidden = true; removeAnalyticsCookies(); }
  }
  window.addEventListener('storage', event => {
    if (measurementId && (event.key === consentKey || event.key === null) && remembered() !== 'accepted') reject(false);
  });
  fetch('/assets/analytics-config.json', { cache: 'no-store' })
    .then(response => response.ok ? response.json() : null)
    .then(config => {
      if (!/^G-[A-Z0-9]{5,20}$/.test(config?.measurementId || '')) return;
      measurementId = config.measurementId;
      mount();
    }).catch(() => { /* Missing configuration keeps analytics disabled. */ });
})();
