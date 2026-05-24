# GroMoney Capital — Website

A complete, responsive, SEO-friendly multi-page website for **GroMoney Capital** (Authorised NJ Wealth Partner) covering Mutual Funds, Insurance, Loans, Credit Cards, Calculators and more.

> **Domain:** gromoneycapital.com
> **Built as:** plain static HTML / CSS / JS — no build tools, no frameworks, no database. Just upload and go.

---

## Pages included

| Page | File |
|---|---|
| Home | `index.html` |
| About Us | `about.html` |
| Contact Us | `contact.html` |
| Mutual Funds | `mutual-funds.html` |
| Insurance hub | `insurance.html` |
| Life Insurance | `life-insurance.html` |
| Term Insurance | `term-insurance.html` |
| Health Insurance | `health-insurance.html` |
| Travel Insurance | `travel-insurance.html` |
| Loans hub | `loans.html` |
| Credit Cards | `credit-card.html` |
| Personal Loan | `personal-loan.html` |
| Home Loan | `home-loan.html` |
| Auto Loan | `auto-loan.html` |
| Free CIBIL Check | `cibil-check.html` |
| Calculators (SIP/Lumpsum/EMI/Goal) | `tools.html` |
| Client Reviews | `testimonials.html` |
| Privacy Policy | `privacy-policy.html` |
| Terms of Service | `terms.html` |
| Disclaimer | `disclaimer.html` |

Plus `sitemap.xml` and `robots.txt` for SEO.

## Folder structure

```
.
├── index.html, about.html, contact.html, ... (all page files)
├── sitemap.xml
├── robots.txt
├── assets/
│   ├── css/style.css       — single master stylesheet
│   └── js/main.js          — menu, calculators, animations
└── _build/build.py         — optional generator (not needed at runtime)
```

The `_build/` folder is **only** a developer convenience for re-generating repetitive pages. You do not need to upload it to your host.

---

## How to deploy

### Option A — Plain hosting (Hostinger, Bluehost, GoDaddy, etc.)

1. Buy your domain `gromoneycapital.com` (you already own this).
2. Connect domain to any shared/static host.
3. Upload **all files except `_build/` and `README.md`** to your `public_html` (or web root).
4. Done — visit https://gromoneycapital.com.

### Option B — Free hosting (GitHub Pages / Netlify / Cloudflare Pages)

1. Push this repo to GitHub.
2. Enable GitHub Pages in repo Settings → Pages → Branch: main → root.
3. Add your domain in the same screen and add a `CNAME` record at your DNS to GitHub's IP.

### Option C — Use it inside WordPress

Since you mentioned you manage WordPress sites, you have two options:

1. **Replace WordPress** — point `gromoneycapital.com` to this static site. It will load 5–10× faster than WordPress, no plugin updates, no security scans.
2. **Keep WordPress, copy each page**:
    - In WordPress admin, create a new Page (e.g. "Mutual Funds").
    - Switch editor to **HTML / Code view**.
    - Copy the contents of `<section>` blocks from `mutual-funds.html` into the page.
    - Repeat for each page.
    - Use the same CSS by uploading `assets/css/style.css` to your theme and enqueuing it.

---

## Customisation

### Change phone, email, WhatsApp number
Search/replace these placeholders across all `*.html`:

| Placeholder | Where to update |
|---|---|
| `+91 90000 00000` | Phone — used in `contact.html`, footer (currently only in contact) |
| `contact@gromoneycapital.com` | Email |
| `https://wa.me/919000000000` | WhatsApp link in `contact.html` |

### Affiliate / referral links
Already wired up:
- **NJ Wealth (Mutual Fund A/c open):** `http://p.njw.bz/29511`
- **GroMo (Insurance / Loans / Cards / CIBIL):** `https://sales.gromo.in/gp-website/g/0E9yO8aWdbur0QPHJaqDY`

If these change, just search/replace across the project.

### Images
All images use [Unsplash](https://unsplash.com) royalty-free CDN URLs (no download needed). To change an image, just paste a different Unsplash URL into the `src=` attribute. To use your own photos: upload to `assets/images/` and update the `src`.

### Brand colours
Edit the variables at the top of `assets/css/style.css`:

```css
--color-primary:  #0b3d6b;   /* main blue */
--color-accent:   #f5a623;   /* gold / CTA */
```

---

## SEO checklist (already done)

- ✅ Mobile-first responsive layout
- ✅ Unique `<title>` and `<meta description>` per page
- ✅ Canonical URLs on every page
- ✅ Open Graph tags for social sharing
- ✅ Schema.org JSON-LD (FinancialService) on home & service pages
- ✅ Semantic HTML5 (header, nav, section, footer)
- ✅ `sitemap.xml` and `robots.txt`
- ✅ Fast — no jQuery, no frameworks
- ✅ Accessible (alt text, aria-labels, contrast, reduced-motion support)

After deploying, submit your sitemap to:
- https://search.google.com/search-console (add `https://gromoneycapital.com/sitemap.xml`)
- https://www.bing.com/webmasters

---

## Working features

- 📱 Hamburger menu on mobile, dropdown menus on desktop
- 🎢 Auto-rotating animated hero slideshow with Ken-Burns zoom
- 🔢 Animated counters (500+ Investors, ₹50 Cr+ assets)
- 🌊 Floating decorative shapes & images
- 🎚️ Scroll-reveal animations
- 🧮 Working SIP, Lumpsum, EMI and Goal calculators (no backend needed)
- ✉️ Contact form with mailto fallback (works without server)
- 🔍 FAQ accordion on every product page
- 📑 Tabbed calculators
- 🌐 Fully responsive — phone, tablet, desktop

---

## Re-generating pages (optional)

If you want to bulk-edit content across multiple similar pages (e.g. the 4 insurance or 4 loan pages), edit `_build/build.py` and run:

```bash
cd kiro-gromoney
python3 _build/build.py
```

This regenerates every page that the script owns. The hand-written pages (`index.html`, `about.html`, `contact.html`, `mutual-funds.html`, `insurance.html`) are **not** managed by the builder.

---

## Disclaimer

This codebase is provided for the GroMoney Capital website. All financial product references (NJ Wealth, GroMo, named AMCs) are placeholders for the partner's affiliate funnels — the partner is responsible for compliance with AMFI, IRDAI, RBI and SEBI guidelines for their region.

© 2026 GroMoney Capital
