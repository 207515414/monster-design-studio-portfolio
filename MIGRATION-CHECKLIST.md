# Migration Checklist

- [x] Keep the existing static-site structure and public portfolio assets.
- [x] Keep email, WhatsApp and social links.
- [x] Add static, crawlable service, industry, portfolio and blog URLs.
- [x] Set sitemap and robots references to `https://monster-cg.com`.
- [x] Restore the active `CNAME` file with `monster-cg.com` before deployment.
- [ ] In GitHub Pages, verify `monster-cg.com` is the custom domain and HTTPS is enforced.
- [ ] Publish, then check `/robots.txt`, `/sitemap.xml`, homepage canonical and core service canonicals on production.
- [ ] Submit the sitemap in Google Search Console and request indexing for home, services and priority service pages.
- [ ] Validate structured data with Google Rich Results Test after deployment.
- [ ] Run PageSpeed Insights against production mobile and desktop URLs; optimize only issues confirmed by the report.
