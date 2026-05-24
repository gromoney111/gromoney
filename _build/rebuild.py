#!/usr/bin/env python3
"""
GroMoney Capital — v2 rebuild.

For every existing *.html file in the repo root, replace:
- the existing <header>...</header> block with the new utility-bar + main nav
- the existing <footer>...</footer> block with the new compliance-rich footer
- legacy phone/email placeholders with the real numbers

Usage:  python3 _build/rebuild.py
"""

import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent

PHONE = "9664019564"
PHONE_DISPLAY = "+91 96640 19564"
WHATSAPP = "919664019564"
EMAIL = "contact@gromoneycapital.com"
ARN = "270739"
LOGIN_URL = "https://ewa.njindiaonline.com/ewa/login"
NJ_LINK = "http://p.njw.bz/29511"
GROMO_LINK = "https://sales.gromo.in/gp-website/g/0E9yO8aWdbur0QPHJaqDY"

# ----- Professional SVG logo -----
SVG_LOGO = """<svg class="brand-svg" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-label="GroMoney Capital logo">
  <defs>
    <linearGradient id="lg1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0b3d6b"/>
      <stop offset="100%" stop-color="#1a5a96"/>
    </linearGradient>
    <linearGradient id="lg2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f5a623"/>
      <stop offset="100%" stop-color="#d68910"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="60" height="60" rx="14" fill="url(#lg1)"/>
  <path d="M16 44 L26 32 L34 38 L48 22" stroke="url(#lg2)" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="48" cy="22" r="3.5" fill="#f5a623"/>
  <text x="32" y="56" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="800" fill="#fff" text-anchor="middle" letter-spacing="1">GROW</text>
</svg>"""

# ----- New header markup -----
HEADER = f"""<div class="utility-bar">
  <div class="container">
    <div class="util-left">
      <span>AMFI Reg. ARN: {ARN}</span>
      <span>IRDA Registered</span>
      <span>NJ Wealth Partner</span>
    </div>
    <div class="util-right">
      <a href="tel:+91{PHONE}" class="util-phone">{PHONE_DISPLAY}</a>
      <a href="{LOGIN_URL}" target="_blank" rel="noopener" class="util-login">Client Login</a>
    </div>
  </div>
</div>
<header class="site-header">
  <div class="container nav-bar">
    <a class="brand" href="index.html">
      {SVG_LOGO}
      <span class="brand-text">
        <strong>Gro<em>Money</em> Capital</strong>
        <small>Mutual Funds · Insurance · Loans</small>
      </span>
    </a>
    <button class="menu-toggle" aria-label="Toggle menu"><span></span><span></span><span></span></button>
    <ul class="nav-links">
      <li><a href="index.html">Home</a></li>
      <li><a href="about.html">About</a></li>
      <li><a href="mutual-funds.html">Mutual Funds</a></li>
      <li class="has-sub"><a href="insurance.html">Insurance</a>
        <ul class="submenu">
          <li><a href="insurance.html">All Insurance</a></li>
          <li><a href="life-insurance.html">Life Insurance</a></li>
          <li><a href="term-insurance.html">Term Insurance</a></li>
          <li><a href="health-insurance.html">Health Insurance</a></li>
          <li><a href="travel-insurance.html">Travel Insurance</a></li>
        </ul>
      </li>
      <li class="has-sub"><a href="loans.html">Loans &amp; Cards</a>
        <ul class="submenu">
          <li><a href="loans.html">All Products</a></li>
          <li><a href="credit-card.html">Credit Cards</a></li>
          <li><a href="personal-loan.html">Personal Loan</a></li>
          <li><a href="home-loan.html">Home Loan</a></li>
          <li><a href="auto-loan.html">Auto Loan</a></li>
          <li><a href="cibil-check.html">Free CIBIL Check</a></li>
        </ul>
      </li>
      <li><a href="financial-products.html">Apply Online</a></li>
      <li><a href="tools.html">Tools</a></li>
      <li><a href="contact.html">Contact</a></li>
      <li class="nav-cta"><a class="btn btn-primary" href="{NJ_LINK}" target="_blank" rel="noopener">Open MF A/c</a></li>
    </ul>
  </div>
</header>"""

# ----- New footer markup (with reviews link, contact, AMFI/IRDA) -----
FOOTER = f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <div class="brand" style="color:#fff;">
        {SVG_LOGO}
        <span class="brand-text" style="color:#fff;">
          <strong style="color:#fff;">Gro<em style="color:#f5a623; font-style:normal;">Money</em> Capital</strong>
          <small style="color:rgba(255,255,255,.7);">NJ Wealth · AMFI · IRDA Registered</small>
        </span>
      </div>
      <p>Empowering Indian families to invest, protect and grow their wealth — one financial decision at a time.</p>
      <p style="font-size:.85rem; color:rgba(255,255,255,.85);">
        <strong>Contact:</strong><br>
        📞 <a href="tel:+91{PHONE}" style="display:inline;">{PHONE_DISPLAY}</a><br>
        ✉️ <a href="mailto:{EMAIL}" style="display:inline;">{EMAIL}</a><br>
        💬 <a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener" style="display:inline;">WhatsApp Chat</a>
      </p>
      <div class="social"><a href="#" aria-label="Facebook">f</a><a href="#" aria-label="Twitter">t</a><a href="#" aria-label="LinkedIn">in</a><a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener" aria-label="WhatsApp">w</a></div>
    </div>
    <div>
      <h4>Quick Links</h4>
      <a href="index.html">Home</a>
      <a href="about.html">About Us</a>
      <a href="contact.html">Contact</a>
      <a href="testimonials.html">Client Reviews</a>
      <a href="tools.html">Calculators</a>
      <a href="{LOGIN_URL}" target="_blank" rel="noopener">Client Login</a>
    </div>
    <div>
      <h4>Products</h4>
      <a href="mutual-funds.html">Mutual Funds</a>
      <a href="insurance.html">Insurance</a>
      <a href="loans.html">Loans &amp; Cards</a>
      <a href="financial-products.html">All Products</a>
      <a href="cibil-check.html">CIBIL Check</a>
    </div>
    <div>
      <h4>Legal</h4>
      <a href="privacy-policy.html">Privacy Policy</a>
      <a href="terms.html">Terms of Service</a>
      <a href="disclaimer.html">Disclaimer</a>
    </div>
  </div>
  <div class="footer-bottom container">
    © <span id="year"></span> GroMoney Capital · AMFI Reg. ARN: {ARN} · IRDA Registered. All rights reserved.
    <a href="privacy-policy.html">Privacy</a>·<a href="terms.html">Terms</a>·<a href="disclaimer.html">Disclaimer</a>
  </div>
  <div class="disclaimer-strip"><div class="container">
    Mutual fund investments are subject to market risks. Read all scheme-related documents carefully before investing. Past performance is not indicative of future returns. Insurance is the subject matter of solicitation. GroMoney Capital is an AMFI-registered Mutual Fund Distributor (ARN: {ARN}) under the NJ Wealth Partner network and a referral partner for insurance &amp; loan products. We do not provide investment advice.
  </div></div>
</footer>"""

# ----- Header / footer replacement -----
re_header = re.compile(r"<header class=\"site-header\">.*?</header>", re.DOTALL)
re_utility_already = re.compile(r"<div class=\"utility-bar\">.*?</div>\s*</div>\s*</div>\s*", re.DOTALL)
re_footer = re.compile(r"<footer class=\"site-footer\">.*?</footer>", re.DOTALL)

# ----- Phone/email replacements (legacy placeholders → real values) -----
SUBSTITUTIONS = [
    ("+91 90000 00000", PHONE_DISPLAY),
    ("+919000000000",  f"+91{PHONE}"),
    ("9000000000",     PHONE),
    ("919000000000",   WHATSAPP),
    ("+91-90000-00000", PHONE_DISPLAY),
]

count = 0
for html_file in sorted(ROOT.glob("*.html")):
    s = html_file.read_text(encoding="utf-8")
    # Strip any pre-existing utility bar (so we don't duplicate)
    s = re_utility_already.sub("", s, count=1)
    # Replace header
    s, n = re_header.subn(HEADER, s, count=1)
    # Replace footer
    s, m = re_footer.subn(FOOTER, s, count=1)
    # Phone/email substitutions
    for old, new in SUBSTITUTIONS:
        s = s.replace(old, new)
    html_file.write_text(s, encoding="utf-8")
    print(f"  updated {html_file.name}  (header={n}, footer={m})")
    count += 1
print(f"Done. {count} files updated.")
