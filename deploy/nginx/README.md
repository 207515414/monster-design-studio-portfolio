# China-site IP redirect

The Chinese site is served from `https://monster-cg.com/zh/`. Existing English pages are not changed.

## Server prerequisites

1. Keep the `monster-cg.com`, `www` and `web` DNS records proxied through Cloudflare (orange-cloud status enabled).
2. Cloudflare supplies the visitor country as the `CF-IPCountry` request header. No Nginx GeoIP module or server-side country database is needed.
3. A request that bypasses Cloudflare has no country header and remains on the English home page.

## Nginx include order

1. Include `cloudflare-country-map.conf` in Nginx's `http {}` block.
2. Include `china-ip-redirect.conf` in the `server {}` block that serves `monster-cg.com`.
3. Validate with `sudo nginx -t`, then reload only after it succeeds.

The redirect affects only `/`: visitors whose country code is `CN` receive a `302` redirect to `/zh/`. A visitor who selects English uses `/locale/english/`, which stores a `monster_locale=en` cookie and prevents future automatic home-page redirects.

## VPN verification after deployment

1. With a China-based public IP and a fresh browser session (or after clearing the `monster_locale` cookie), open `https://www.monster-cg.com/`. Expect `302` and then `https://www.monster-cg.com/zh/`.
2. Select **English** on the Chinese site. Expect the English home page to load and remain selected after refresh.
3. Enable a non-China VPN, use a fresh browser session, and open `https://www.monster-cg.com/`. Expect the original English home page without redirect.
4. Check `https://www.monster-cg.com/services/` from both networks. It must remain on the existing English URL because only the home page redirects.

## Rollback

Remove the `china-ip-redirect.conf` include and reload Nginx. The static `/zh/` pages can remain in the deployment; no English content or contact method is changed.
