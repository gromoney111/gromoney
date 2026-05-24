#!/usr/bin/env python3
"""
GroMoney Capital — static site builder.

Composes header + footer + per-page content into final HTML files.
Run:  python3 _build/build.py

This is a one-off generator; all output is plain static HTML
that can be uploaded to any host (Hostinger, Netlify, GitHub Pages,
Bluehost, or imported into a WordPress page via custom HTML block).
"""
import os, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "_build" / "pages"

NAV_LINKS = """
      <li><a href="index.html"{home_active}>Home</a></li>
      <li><a href="about.html"{about_active}>About</a></li>
      <li><a href="mutual-funds.html"{mf_active}>Mutual Funds</a></li>
      <li class="has-sub"><a href="insurance.html"{ins_active}>Insurance</a>
        <ul class="submenu">
          <li><a href="insurance.html">All Insurance</a></li>
          <li><a href="life-insurance.html">Life Insurance</a></li>
          <li><a href="term-insurance.html">Term Insurance</a></li>
          <li><a href="health-insurance.html">Health Insurance</a></li>
          <li><a href="travel-insurance.html">Travel Insurance</a></li>
        </ul>
      </li>
      <li class="has-sub"><a href="loans.html"{loan_active}>Loans &amp; Cards</a>
        <ul class="submenu">
          <li><a href="loans.html">All Products</a></li>
          <li><a href="credit-card.html">Credit Cards</a></li>
          <li><a href="personal-loan.html">Personal Loan</a></li>
          <li><a href="home-loan.html">Home Loan</a></li>
          <li><a href="auto-loan.html">Auto Loan</a></li>
          <li><a href="cibil-check.html">Free CIBIL Check</a></li>
        </ul>
      </li>
      <li><a href="tools.html"{tools_active}>Tools</a></li>
      <li><a href="testimonials.html"{rev_active}>Reviews</a></li>
      <li><a href="contact.html"{con_active}>Contact</a></li>
      <li class="nav-cta"><a class="btn btn-primary" href="http://p.njw.bz/29511" target="_blank" rel="noopener">Open MF A/c</a></li>
"""

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="https://gromoneycapital.com/{slug}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://gromoneycapital.com/{slug}">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230b3d6b'/%3E%3Ctext x='32' y='42' font-family='Arial' font-size='32' font-weight='bold' fill='%23f5a623' text-anchor='middle'%3EG%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{schema}
</head>
<body>
<header class="site-header">
  <div class="container nav-bar">
    <a class="brand" href="index.html"><span class="brand-logo">G</span><span>GroMoney Capital<small>NJ Wealth Partner</small></span></a>
    <button class="menu-toggle" aria-label="Toggle menu"><span></span><span></span><span></span></button>
    <ul class="nav-links">""" + NAV_LINKS + """</ul>
  </div>
</header>
"""

FOOTER = """
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <div class="brand" style="color:#fff;"><span class="brand-logo">G</span><span style="color:#fff;">GroMoney Capital<small style="color:rgba(255,255,255,.7);">NJ Wealth Partner</small></span></div>
      <p>Empowering Indian families to invest, protect and grow their wealth — one financial decision at a time.</p>
      <div class="social"><a href="#" aria-label="Facebook">f</a><a href="#" aria-label="Twitter">t</a><a href="#" aria-label="LinkedIn">in</a><a href="#" aria-label="WhatsApp">w</a></div>
    </div>
    <div><h4>Quick Links</h4><a href="index.html">Home</a><a href="about.html">About Us</a><a href="contact.html">Contact</a><a href="testimonials.html">Reviews</a><a href="tools.html">Calculators</a></div>
    <div><h4>Products</h4><a href="mutual-funds.html">Mutual Funds</a><a href="insurance.html">Insurance</a><a href="loans.html">Loans &amp; Cards</a><a href="cibil-check.html">CIBIL Check</a></div>
    <div><h4>Legal</h4><a href="privacy-policy.html">Privacy Policy</a><a href="terms.html">Terms of Service</a><a href="disclaimer.html">Disclaimer</a></div>
  </div>
  <div class="footer-bottom container">© <span id="year"></span> GroMoney Capital. All rights reserved.
    <a href="privacy-policy.html">Privacy</a>·<a href="terms.html">Terms</a>·<a href="disclaimer.html">Disclaimer</a>
  </div>
  <div class="disclaimer-strip"><div class="container">Mutual fund investments are subject to market risks. Read all scheme-related documents carefully. Insurance is a subject matter of solicitation. GroMoney Capital is a distributor and does not provide investment advice. We earn referral/commission from partner products.</div></div>
</footer>
<script src="assets/js/main.js"></script>
</body>
</html>
"""

def render(meta, body):
    actives = {k: "" for k in ["home", "about", "mf", "ins", "loan", "tools", "rev", "con"]}
    if meta.get("active"):
        actives[meta["active"]] = ' class="active"'
    head = HEAD.format(
        title=meta["title"],
        description=meta["description"],
        keywords=meta.get("keywords", "GroMoney Capital, NJ Wealth Partner"),
        slug=meta["slug"],
        schema=meta.get("schema", ""),
        home_active=actives["home"],
        about_active=actives["about"],
        mf_active=actives["mf"],
        ins_active=actives["ins"],
        loan_active=actives["loan"],
        tools_active=actives["tools"],
        rev_active=actives["rev"],
        con_active=actives["con"],
    )
    return head + body + FOOTER

def write(slug, meta, body):
    meta["slug"] = slug
    out = ROOT / slug
    out.write_text(render(meta, body), encoding="utf-8")
    print(f"  wrote {slug}")

# =================== PAGE BODIES ===================

def page_hero(crumbs, h1, subtitle):
    return f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumb">{crumbs}</div>
    <h1>{h1}</h1>
    <p>{subtitle}</p>
  </div>
</section>
"""

def insurance_sub(slug, name, hero_img, kw, desc, intro, perks, types, faqs):
    body = page_hero(
        f'<a href="index.html">Home</a> / <a href="insurance.html">Insurance</a> / {name}',
        f"{name}",
        desc,
    )
    body += f"""
<section class="section">
  <div class="container split">
    <div>
      <span class="badge">Insurance</span>
      <h2>{intro['heading']}</h2>
      <p>{intro['p']}</p>
      <ul class="feature-list">
        {''.join(f'<li>{x}</li>' for x in perks)}
      </ul>
      <a href="https://sales.gromo.in/gp-website/g/0E9yO8aWdbur0QPHJaqDY" target="_blank" rel="noopener" class="btn btn-primary">Free Consultation</a>
      <a href="contact.html" class="btn btn-outline">Talk to Advisor</a>
    </div>
    <div><img src="{hero_img}" alt="{name}"></div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <h2 class="section-title">Plan Types &amp; Features</h2>
    <div class="grid grid-3">
      {''.join(f'<div class="card"><div class="card-icon{" gold" if i%2 else ""}">{t["icon"]}</div><h3>{t["title"]}</h3><p>{t["desc"]}</p></div>' for i,t in enumerate(types))}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="section-title">FAQs</h2>
    <div style="max-width:800px;margin:0 auto;">
      {''.join(f'<div class="faq-item"><button class="faq-q">{q}</button><div class="faq-a">{a}</div></div>' for q,a in faqs)}
    </div>
  </div>
</section>

<section class="container">
  <div class="cta-banner">
    <h2>Get the right cover, at the best price</h2>
    <p>Free, no-obligation comparison from 8+ top insurers.</p>
    <a class="btn btn-primary" href="https://sales.gromo.in/gp-website/g/0E9yO8aWdbur0QPHJaqDY" target="_blank" rel="noopener">Get Free Quote</a>
    <a class="btn btn-light" href="contact.html">Contact Us</a>
  </div>
</section>
"""
    write(slug, {"title": f"{name} Plans in India | GroMoney Capital",
                 "description": desc, "keywords": kw, "active": "ins"}, body)

# ---------- Term Insurance ----------
insurance_sub(
    "term-insurance.html", "Term Insurance",
    "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=900&q=70",
    "term insurance India, term plan, term cover, low premium term plan",
    "Pure protection at the lowest premium. Get up to ₹2 Crore term insurance cover from just ₹500/month.",
    {"heading": "Maximum cover at minimum premium",
     "p": "A term plan is the cheapest and most efficient form of life cover. You pay a small premium, and your nominee receives a lump-sum payout if anything happens to you during the policy term. Pure protection — no investment, no confusion."},
    ["Cover up to ₹2 Cr at ~₹500/month", "Premium locked-in for entire term",
     "Critical illness &amp; accidental rider options", "Tax benefit under 80C &amp; 10(10D)",
     "Higher claim settlement ratios from top insurers"],
    [
      {"icon":"🛡️","title":"Pure Term","desc":"Lump-sum payout to nominee on death during term."},
      {"icon":"📈","title":"Increasing Cover","desc":"Cover automatically rises with inflation/age."},
      {"icon":"💰","title":"Return of Premium","desc":"Get all premiums back if you survive the term."},
      {"icon":"🏥","title":"With Critical Illness","desc":"Lump-sum payout on diagnosis of major illness."},
      {"icon":"⚡","title":"Accidental Death","desc":"Additional benefit on accidental demise."},
      {"icon":"👨‍👩‍👧","title":"Joint / Spouse Cover","desc":"Single policy covering both partners."}
    ],
    [
      ("How much term cover should I take?", "Ideally 10–15× your annual income plus all outstanding loans. We calculate the exact figure during your free consultation."),
      ("Why is term insurance the cheapest?", "Because it's pure risk cover — no savings or investment component. You only pay for the death benefit."),
      ("What is claim settlement ratio?", "It's the % of claims an insurer settles vs received. We recommend insurers with 95%+ ratio for the past 3 years."),
      ("Can I increase cover later?", "Yes, most plans allow you to increase cover at major life events like marriage, child birth or new home loan.")
    ]
)

# ---------- Health Insurance ----------
insurance_sub(
    "health-insurance.html", "Health Insurance",
    "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=900&q=70",
    "health insurance India, mediclaim, family floater, cashless hospital",
    "Cashless hospitalisation across 10,000+ hospitals. Family floater, individual and senior citizen plans.",
    {"heading":"One hospital bill can wipe out years of savings","p":"A medical emergency is the leading cause of debt in India. Health insurance protects your family from sudden, large hospital bills, with cashless treatment across thousands of network hospitals."},
    ["Cashless treatment at 10,000+ hospitals","Pre &amp; post hospitalisation cover (60–90 days)","No-claim bonus up to 200% sum insured",
     "Day-care procedures &amp; modern treatments covered","Tax benefit up to ₹75,000 under Section 80D"],
    [
      {"icon":"👤","title":"Individual Plan","desc":"Separate cover for each member; ideal for young singles."},
      {"icon":"👨‍👩‍👧","title":"Family Floater","desc":"Single sum insured shared across the whole family."},
      {"icon":"👴","title":"Senior Citizen","desc":"Specially designed plans for parents 60+."},
      {"icon":"🚨","title":"Critical Illness","desc":"Lump-sum on diagnosis of cancer, heart attack, etc."},
      {"icon":"🤰","title":"Maternity Cover","desc":"Pregnancy &amp; newborn care included."},
      {"icon":"🏥","title":"Top-up &amp; Super Top-up","desc":"Extend existing cover at low cost."}
    ],
    [
      ("How much health cover do I need?","For a metro-based family of 4, ₹10–25 lakh is recommended. Tier-2 cities can start at ₹5–10 lakh."),
      ("What is the waiting period?","Most plans have 30 days for new illnesses, 2–4 years for pre-existing conditions, and 9 months–4 years for maternity."),
      ("Will my employer's cover suffice?","Usually no — corporate covers are often only ₹3–5 lakh and stop the moment you change/leave the job."),
      ("Are pre-existing diseases covered?","Yes, after the waiting period (typically 2–4 years). Always declare them honestly to avoid claim rejection.")
    ]
)

# ---------- Travel Insurance ----------
insurance_sub(
    "travel-insurance.html", "Travel Insurance",
    "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=900&q=70",
    "travel insurance India, international travel insurance, schengen visa insurance",
    "Domestic and international travel cover for medical emergencies, trip cancellation, lost baggage and more.",
    {"heading":"Travel worry-free, anywhere in the world","p":"Travel insurance protects you from medical emergencies abroad, trip cancellation, lost luggage and many other unforeseen events. Mandatory for Schengen visa and recommended for all overseas trips."},
    ["Emergency medical &amp; hospitalisation abroad","Trip cancellation/interruption cover",
     "Lost passport &amp; baggage compensation","24x7 emergency assistance helpline",
     "Schengen-compliant cover available"],
    [
      {"icon":"🌍","title":"International Travel","desc":"Worldwide medical, evacuation &amp; baggage cover."},
      {"icon":"🇮🇳","title":"Domestic Travel","desc":"India-only travel cover at low premium."},
      {"icon":"🎓","title":"Student Travel","desc":"Specialised cover for students studying abroad."},
      {"icon":"💼","title":"Business Travel","desc":"Multi-trip annual plans for frequent flyers."},
      {"icon":"👨‍👩‍👧","title":"Family Plan","desc":"Cover the whole family in a single policy."},
      {"icon":"🏔️","title":"Adventure Sports","desc":"Add-on for skiing, trekking, diving, etc."}
    ],
    [
      ("Is travel insurance mandatory?","For Schengen and many other countries' visas, yes. Even where it's optional, we strongly recommend it."),
      ("When should I buy it?","Ideally right after booking your tickets — that way you're covered for trip cancellation too."),
      ("Does it cover COVID-19?","Most modern plans now cover COVID-19 hospitalisation abroad. Always check specific policy wording."),
      ("Can I extend the policy abroad?","Many insurers allow online extension before your existing cover expires.")
    ]
)

# ============= LOANS =============

def loan_sub(slug, name, hero_img, kw, desc, intro_h, intro_p, perks, features, faqs):
    body = page_hero(
        f'<a href="index.html">Home</a> / <a href="loans.html">Loans &amp; Cards</a> / {name}',
        name, desc
    )
    body += f"""
<section class="section">
  <div class="container split">
    <div>
      <span class="badge">Powered by GroMo</span>
      <h2>{intro_h}</h2>
      <p>{intro_p}</p>
      <ul class="feature-list">
        {''.join(f'<li>{x}</li>' for x in perks)}
      </ul>
      <a href="https://sales.gromo.in/gp-website/g/0E9yO8aWdbur0QPHJaqDY" target="_blank" rel="noopener" class="btn btn-primary">Apply Now</a>
      <a href="contact.html" class="btn btn-outline">Talk to Advisor</a>
    </div>
    <div><img src="{hero_img}" alt="{name}"></div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <h2 class="section-title">Key Features</h2>
    <div class="grid grid-3">
      {''.join(f'<div class="card"><div class="card-icon{" gold" if i%2 else ""}">{t["icon"]}</div><h3>{t["title"]}</h3><p>{t["desc"]}</p></div>' for i,t in enumerate(features))}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="section-title">FAQs</h2>
    <div style="max-width:800px;margin:0 auto;">
      {''.join(f'<div class="faq-item"><button class="faq-q">{q}</button><div class="faq-a">{a}</div></div>' for q,a in faqs)}
    </div>
  </div>
</section>

<section class="container">
  <div class="cta-banner">
    <h2>Ready to apply?</h2>
    <p>Quick approvals, paperless documentation, best rates from leading lenders.</p>
    <a class="btn btn-primary" href="https://sales.gromo.in/gp-website/g/0E9yO8aWdbur0QPHJaqDY" target="_blank" rel="noopener">Apply Now</a>
    <a class="btn btn-light" href="tools.html">EMI Calculator</a>
  </div>
</section>
"""
    write(slug, {"title": f"{name} Online | GroMoney Capital",
                 "description": desc, "keywords": kw, "active": "loan"}, body)

# Credit Card
loan_sub(
    "credit-card.html", "Credit Cards",
    "https://images.unsplash.com/photo-1556742044-3c52d6e88c62?auto=format&fit=crop&w=900&q=70",
    "credit card India, best credit card, lifetime free credit card, apply credit card online",
    "Apply for the best credit cards in India — lifetime free, fuel cards, travel cards, cashback &amp; reward cards.",
    "Find the perfect credit card for your lifestyle",
    "From cashback to travel rewards, business cards to lifetime-free options — we help you compare 30+ credit cards from leading banks and apply online in minutes.",
    ["Lifetime free options available", "Instant digital approval",
     "Cashback, travel &amp; reward cards", "0% forex markup on travel cards", "Business &amp; corporate cards too"],
    [
      {"icon":"💳","title":"Lifetime Free Cards","desc":"No joining or annual fees, ever."},
      {"icon":"✈️","title":"Travel Cards","desc":"Lounge access, miles, 0% forex markup."},
      {"icon":"💰","title":"Cashback Cards","desc":"Up to 5% cashback on online &amp; offline spends."},
      {"icon":"⛽","title":"Fuel Cards","desc":"1% surcharge waiver + extra fuel rewards."},
      {"icon":"🛍️","title":"Reward Cards","desc":"Points on shopping, dining &amp; entertainment."},
      {"icon":"🏢","title":"Business Cards","desc":"Higher limits + GST input credit on spends."}
    ],
    [
      ("What CIBIL score is needed?","Generally 750+ for premium cards. Some entry-level cards approve at 700+. Check your score free on our CIBIL page."),
      ("Will applying affect my credit score?","A formal application creates a hard enquiry which may temporarily lower your score by 5–10 points. Multiple applications in short succession are flagged."),
      ("Are lifetime free cards really free?","Yes, no joining or annual fee — but you should still pay statements on time to avoid interest and late fees."),
      ("How long does approval take?","Most banks now offer instant digital approval (5–10 minutes), with the physical card delivered in 5–7 days.")
    ]
)

# Personal Loan
loan_sub(
    "personal-loan.html", "Personal Loan",
    "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=900&q=70",
    "personal loan India, instant personal loan, personal loan online apply",
    "Get a personal loan up to ₹50 Lakh at attractive interest rates. Quick approval, paperless application, flexible tenures.",
    "Personal loans for every life moment",
    "Whether it's a wedding, medical emergency, home renovation, or debt consolidation — get a personal loan up to ₹50 Lakh with minimal paperwork. Apply online and get money in your bank within 24–72 hours.",
    ["Loan amount up to ₹50 Lakh","Tenure 12–60 months",
     "Interest from 10.5% p.a.","Minimal documentation, fully digital",
     "No collateral required"],
    [
      {"icon":"⚡","title":"Quick Disbursal","desc":"Money in your bank within 24–72 hours."},
      {"icon":"📄","title":"Paperless","desc":"Apply 100% online with eKYC &amp; eSign."},
      {"icon":"📊","title":"Flexible Tenure","desc":"Choose EMIs from 12 to 60 months."},
      {"icon":"🎯","title":"Any Purpose","desc":"Wedding, travel, medical, debt consolidation."},
      {"icon":"🔒","title":"No Collateral","desc":"Unsecured loan — no asset pledge."},
      {"icon":"💼","title":"Salaried &amp; Self-Employed","desc":"Tailored offers for both segments."}
    ],
    [
      ("What is the eligibility?","Salaried 21–60 yrs with min ₹15K–25K monthly income depending on lender; self-employed with min 2–3 yrs of business."),
      ("What documents are needed?","PAN, Aadhaar, last 3 months bank statement, last 2 salary slips (for salaried) or ITR (for self-employed)."),
      ("Can I prepay or foreclose?","Yes, most lenders allow it after 6–12 EMIs. Foreclosure charges range from 0–4% on the outstanding."),
      ("Will it affect my CIBIL?","Each application creates a hard enquiry. Multiple applications close together can hurt your score. Apply through us — we match you to lenders pre-eligible for you.")
    ]
)

# Home Loan
loan_sub(
    "home-loan.html", "Home Loan",
    "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=900&q=70",
    "home loan India, housing loan, lowest home loan rate, home loan balance transfer",
    "Buy your dream home with attractive home loans up to ₹5 Crore at competitive rates. Free CIBIL check &amp; advisory.",
    "Your dream home, made easy",
    "We help you find the lowest home loan rates from 25+ banks &amp; HFCs, compare offers and pick the right tenure. Whether it's a new home, plot, construction or balance transfer — we've got you covered.",
    ["Loan up to ₹5 Crore", "Tenure up to 30 years",
     "Interest from 8.35% p.a.", "PMAY subsidy up to ₹2.67 Lakh*",
     "Free pre-approval &amp; document advisory"],
    [
      {"icon":"🏠","title":"Home Purchase","desc":"For new &amp; resale residential property."},
      {"icon":"🏗️","title":"Construction Loan","desc":"For self-construction on owned plot."},
      {"icon":"📐","title":"Plot Loan","desc":"To purchase residential land."},
      {"icon":"🔁","title":"Balance Transfer","desc":"Move existing loan to lower-rate lender."},
      {"icon":"🛠️","title":"Top-Up","desc":"Extra funds for renovation/personal use."},
      {"icon":"💰","title":"Tax Benefits","desc":"Up to ₹3.5 Lakh deduction under 80C &amp; 24(b)."}
    ],
    [
      ("How much home loan can I get?","Most lenders fund 75–90% of property value, EMI capped at 40–50% of net income. Get a free pre-approval through us."),
      ("Fixed vs floating rate?","Floating rates are usually 0.5–1% lower than fixed. With falling rates expected, floating is generally smarter."),
      ("Can I claim tax benefits?","Yes — up to ₹1.5 Lakh principal (80C) and ₹2 Lakh interest (24b) per year on a self-occupied home."),
      ("What is balance transfer?","Moving your existing home loan to a lender offering a lower rate. Even 0.5% saving over 20 years can save lakhs.")
    ]
)

# Auto Loan
loan_sub(
    "auto-loan.html", "Auto Loan",
    "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=900&q=70",
    "auto loan, car loan India, two wheeler loan, used car loan",
    "Drive your dream car home — auto loans up to ₹1 Crore at attractive rates for new car, used car &amp; two-wheeler.",
    "Car loans, fast and friendly",
    "Get up to 100% on-road funding for your new car, attractive rates on used cars, and quick two-wheeler loans. We compare offers from 20+ lenders to give you the best fit.",
    ["Up to 100% on-road funding","Tenure up to 7 years",
     "Interest from 8.75% p.a.","Quick approval, in-dealer disbursal",
     "Used car &amp; two-wheeler loans available"],
    [
      {"icon":"🚗","title":"New Car Loan","desc":"Up to 100% on-road funding from top banks."},
      {"icon":"🚙","title":"Used Car Loan","desc":"Up to 90% loan on certified pre-owned cars."},
      {"icon":"🏍️","title":"Two-Wheeler Loan","desc":"Quick &amp; easy financing for bikes &amp; scooters."},
      {"icon":"🚛","title":"Commercial Vehicle","desc":"Loans for taxis, trucks &amp; goods carriers."},
      {"icon":"⚡","title":"EV Loan","desc":"Special rates for electric vehicle financing."},
      {"icon":"🔁","title":"Refinance","desc":"Move existing car loan to a lower-rate lender."}
    ],
    [
      ("Can I get 100% loan on new cars?","Yes, many lenders fund the full on-road price (ex-showroom + insurance + RTO) based on your profile."),
      ("What's the down payment for used cars?","Typically 10–20% of the valuation. The lender's surveyor will assess the vehicle's market value."),
      ("Tenure options?","New car: up to 7 years. Used car: up to 5 years (and not exceeding 8 yrs of total vehicle age). Two-wheeler: 1–4 years."),
      ("Tax benefits on auto loan?","Self-employed can claim interest as a business expense if the vehicle is used for business. Salaried employees usually can't.")
    ]
)

# CIBIL Check
write("cibil-check.html",
      {"title":"Free CIBIL Score Check Online | GroMoney Capital",
       "description":"Check your CIBIL credit score for free in 2 minutes. Get tips to improve your score and unlock better loan and credit card offers.",
       "keywords":"free CIBIL check, credit score India, improve CIBIL, check credit score online",
       "active":"loan"},
      page_hero(
        '<a href="index.html">Home</a> / <a href="loans.html">Loans &amp; Cards</a> / Free CIBIL Check',
        "Free CIBIL Score Check",
        "Know your credit score instantly. Get personalised tips to improve and qualify for better loan and card offers."
      ) + """
<section class="section">
  <div class="container split">
    <div>
      <span class="badge">100% Free Forever</span>
      <h2>Why your credit score matters</h2>
      <p>Your CIBIL score (300–900) is the single biggest factor in getting your loan and credit card application approved — and the interest rate you'll pay. A score of 750+ unlocks the best rates, while below 650 makes approvals difficult.</p>
      <ul class="feature-list">
        <li>Check unlimited times — no impact on score</li>
        <li>Identify reasons your score is low</li>
        <li>Personalised improvement plan</li>
        <li>Pre-approved offers tailored to your score</li>
        <li>Bank-grade data security &amp; privacy</li>
      </ul>
      <a href="https://sales.gromo.in/gp-website/g/0E9yO8aWdbur0QPHJaqDY" target="_blank" rel="noopener" class="btn btn-primary">Check Score Free</a>
    </div>
    <div><img src="https://images.unsplash.com/photo-1554224154-26032ffc0d07?auto=format&fit=crop&w=900&q=70" alt="Credit score check"></div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <h2 class="section-title">What is a Good Credit Score?</h2>
    <div class="grid grid-4">
      <div class="card text-center"><div class="card-icon" style="background:#dc2626;">300-549</div><h3>Poor</h3><p>Loan approvals very difficult. Focus on building credit history.</p></div>
      <div class="card text-center"><div class="card-icon" style="background:#f59e0b;">550-649</div><h3>Fair</h3><p>Approvals possible but at higher interest rates.</p></div>
      <div class="card text-center"><div class="card-icon" style="background:#3b82f6;">650-749</div><h3>Good</h3><p>Most lenders approve at standard rates.</p></div>
      <div class="card text-center"><div class="card-icon gold">750-900</div><h3>Excellent</h3><p>Best rates, premium credit cards, instant approvals.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="section-title">5 Tips to Improve Your CIBIL Score</h2>
    <div class="grid grid-3">
      <div class="service-tile"><div class="icon-circle">⏰</div><h3>Pay on time</h3><p>Even 1 day delay can drop your score 30–50 points. Set up auto-pay.</p></div>
      <div class="service-tile"><div class="icon-circle">📊</div><h3>Keep utilization &lt;30%</h3><p>Don't max out your credit cards. Stay below 30% of total limit.</p></div>
      <div class="service-tile"><div class="icon-circle">🚫</div><h3>Avoid multiple applications</h3><p>Each loan/card enquiry hurts your score. Apply only when needed.</p></div>
      <div class="service-tile"><div class="icon-circle">📜</div><h3>Maintain credit mix</h3><p>A healthy mix of secured (home/auto) and unsecured (PL/CC) loans helps.</p></div>
      <div class="service-tile"><div class="icon-circle">🕰️</div><h3>Long credit history</h3><p>Don't close old credit cards — longer history = higher score.</p></div>
      <div class="service-tile"><div class="icon-circle">🔍</div><h3>Check report regularly</h3><p>Dispute errors on your report. Free unlimited checks through us.</p></div>
    </div>
  </div>
</section>

<section class="container">
  <div class="cta-banner">
    <h2>Find out your CIBIL score now</h2>
    <p>Free, secure and takes only 2 minutes.</p>
    <a class="btn btn-primary" href="https://sales.gromo.in/gp-website/g/0E9yO8aWdbur0QPHJaqDY" target="_blank" rel="noopener">Check My Score</a>
  </div>
</section>
""")

# ============= LOANS HUB =============
loans_hub_body = page_hero(
  '<a href="index.html">Home</a> / Loans &amp; Cards',
  "Loans &amp; Credit Cards",
  "Compare and apply for credit cards, personal loans, home loans, auto loans &amp; more — all from trusted Indian lenders."
) + """
<section class="section">
  <div class="container">
    <h2 class="section-title">Choose your product</h2>
    <p class="section-sub">Powered by our partner GroMo — India's largest digital financial marketplace.</p>
    <div class="grid grid-3">
      <div class="card"><div class="card-icon">💳</div><h3>Credit Cards</h3><p>Compare 30+ cards from top banks. Lifetime free, cashback, travel — find your perfect card.</p><a class="card-link" href="credit-card.html">Explore Credit Cards →</a></div>
      <div class="card"><div class="card-icon gold">💰</div><h3>Personal Loan</h3><p>Up to ₹50 Lakh, fully online application, money in 24–72 hours. From 10.5% p.a.</p><a class="card-link" href="personal-loan.html">Explore Personal Loan →</a></div>
      <div class="card"><div class="card-icon">🏠</div><h3>Home Loan</h3><p>Up to ₹5 Cr, tenures up to 30 years, lowest rates from 25+ lenders. PMAY subsidies available.</p><a class="card-link" href="home-loan.html">Explore Home Loan →</a></div>
      <div class="card"><div class="card-icon gold">🚗</div><h3>Auto Loan</h3><p>Up to 100% funding on new cars, used cars &amp; two-wheelers. From 8.75% p.a.</p><a class="card-link" href="auto-loan.html">Explore Auto Loan →</a></div>
      <div class="card"><div class="card-icon">📊</div><h3>Free CIBIL Check</h3><p>Know your credit score in 2 mins. No impact on score. Improve and unlock better offers.</p><a class="card-link" href="cibil-check.html">Check Score →</a></div>
      <div class="card"><div class="card-icon gold">🤝</div><h3>Free Consultation</h3><p>Not sure which product is right? Get free, unbiased advice from a certified expert.</p><a class="card-link" href="contact.html">Get Started →</a></div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container split">
    <div><img src="https://images.unsplash.com/photo-1554224154-22dec7ec8818?auto=format&fit=crop&w=900&q=70" alt="Credit and loans"></div>
    <div>
      <span class="badge">Why apply through us?</span>
      <h2>Best rates. Faster approvals. Zero hassle.</h2>
      <ul class="feature-list">
        <li>Pre-eligibility check before formal application (no CIBIL hit)</li>
        <li>Compare 25+ banks &amp; NBFCs in one click</li>
        <li>Instant digital approval &amp; eKYC</li>
        <li>Personal advisor at every step</li>
        <li>No charges to you — we earn from the lender</li>
      </ul>
      <a class="btn btn-primary" href="https://sales.gromo.in/gp-website/g/0E9yO8aWdbur0QPHJaqDY" target="_blank" rel="noopener">Get Started</a>
    </div>
  </div>
</section>
"""
write("loans.html",
      {"title":"Credit Cards, Personal Loan, Home Loan &amp; More | GroMoney Capital",
       "description":"Apply for credit cards, personal loans, home loans, auto loans and free CIBIL check — best offers from 25+ banks &amp; NBFCs.",
       "keywords":"credit card, personal loan, home loan, auto loan, CIBIL India",
       "active":"loan"},
      loans_hub_body)

# ============= TOOLS / CALCULATORS =============
tools_body = page_hero(
  '<a href="index.html">Home</a> / Tools',
  "Financial Calculators",
  "Free, accurate calculators for SIP, lumpsum, EMI &amp; goal planning. Get instant insights on your money."
) + """
<section class="section">
  <div class="container">
    <div class="tabs">
      <button class="tab-btn active" data-target="tab-sip">SIP Calculator</button>
      <button class="tab-btn" data-target="tab-ls">Lumpsum</button>
      <button class="tab-btn" data-target="tab-emi">EMI Calculator</button>
      <button class="tab-btn" data-target="tab-goal">Goal Planner</button>
    </div>

    <div id="tab-sip" class="tab-pane active">
      <form id="sipCalc" class="calc">
        <h3>SIP Calculator — How much will my SIP grow?</h3>
        <div class="calc-row">
          <label>Monthly Investment <span id="sipAmountVal">5,000</span></label>
          <input id="sipAmount" type="range" min="500" max="200000" step="500" value="5000">
          <label>Investment Period <span id="sipYearsVal">15 yr</span></label>
          <input id="sipYears" type="range" min="1" max="40" value="15">
          <label>Expected Return (p.a.) <span id="sipReturnVal">12%</span></label>
          <input id="sipReturn" type="range" min="1" max="25" step="0.5" value="12">
        </div>
        <div class="calc-result">
          <div class="item"><small>Total Invested</small><strong id="sipInv">—</strong></div>
          <div class="item"><small>Wealth Gained</small><strong id="sipGain">—</strong></div>
          <div class="item"><small>Future Value</small><strong id="sipFV">—</strong></div>
        </div>
      </form>
    </div>

    <div id="tab-ls" class="tab-pane">
      <form id="lumpsumCalc" class="calc">
        <h3>Lumpsum Calculator — One-time investment growth</h3>
        <div class="calc-row">
          <label>Investment Amount <span id="lsAmountVal">100,000</span></label>
          <input id="lsAmount" type="range" min="1000" max="10000000" step="1000" value="100000">
          <label>Investment Period <span id="lsYearsVal">10 yr</span></label>
          <input id="lsYears" type="range" min="1" max="40" value="10">
          <label>Expected Return (p.a.) <span id="lsReturnVal">12%</span></label>
          <input id="lsReturn" type="range" min="1" max="25" step="0.5" value="12">
        </div>
        <div class="calc-result">
          <div class="item"><small>Invested</small><strong id="lsInv">—</strong></div>
          <div class="item"><small>Wealth Gained</small><strong id="lsGain">—</strong></div>
          <div class="item"><small>Future Value</small><strong id="lsFV">—</strong></div>
        </div>
      </form>
    </div>

    <div id="tab-emi" class="tab-pane">
      <form id="emiCalc" class="calc">
        <h3>EMI Calculator — Monthly loan EMI</h3>
        <div class="calc-row">
          <label>Loan Amount <span id="emiAmountVal">2,500,000</span></label>
          <input id="emiAmount" type="range" min="50000" max="50000000" step="10000" value="2500000">
          <label>Loan Tenure <span id="emiYearsVal">20 yr</span></label>
          <input id="emiYears" type="range" min="1" max="30" value="20">
          <label>Interest Rate (p.a.) <span id="emiRateVal">8.5%</span></label>
          <input id="emiRate" type="range" min="5" max="20" step="0.1" value="8.5">
        </div>
        <div class="calc-result">
          <div class="item"><small>Monthly EMI</small><strong id="emiVal">—</strong></div>
          <div class="item"><small>Total Interest</small><strong id="emiInterest">—</strong></div>
          <div class="item"><small>Total Payable</small><strong id="emiTotal">—</strong></div>
        </div>
      </form>
    </div>

    <div id="tab-goal" class="tab-pane">
      <form id="goalCalc" class="calc">
        <h3>Goal Planner — How much SIP do I need?</h3>
        <div class="calc-row">
          <label>Target Amount <span id="goalAmountVal">10,000,000</span></label>
          <input id="goalAmount" type="range" min="100000" max="100000000" step="50000" value="10000000">
          <label>Years to Goal <span id="goalYearsVal">15 yr</span></label>
          <input id="goalYears" type="range" min="1" max="40" value="15">
          <label>Expected Return (p.a.) <span id="goalReturnVal">12%</span></label>
          <input id="goalReturn" type="range" min="1" max="25" step="0.5" value="12">
        </div>
        <div class="calc-result">
          <div class="item"><small>Required Monthly SIP</small><strong id="goalSIP">—</strong></div>
          <div class="item"><small>Total You'll Invest</small><strong id="goalInv">—</strong></div>
        </div>
      </form>
    </div>
  </div>
</section>

<section class="container">
  <div class="cta-banner">
    <h2>Numbers look good? Start now.</h2>
    <p>Open your mutual fund account in 10 minutes and start your SIP today.</p>
    <a class="btn btn-primary" href="http://p.njw.bz/29511" target="_blank" rel="noopener">Open MF Account</a>
    <a class="btn btn-light" href="contact.html">Get Free Plan</a>
  </div>
</section>
"""
write("tools.html",
      {"title":"Free SIP, Lumpsum &amp; EMI Calculator | GroMoney Capital",
       "description":"Free online calculators for SIP, Lumpsum mutual fund returns, loan EMI and goal-based investment planning.",
       "keywords":"SIP calculator, EMI calculator, lumpsum calculator, mutual fund calculator India",
       "active":"tools"},
      tools_body)

# ============= TESTIMONIALS =============
def t_card(name, role, text, img):
    return f"""<div class="testimonial">
      <div class="stars">★★★★★</div>
      <p class="testimonial-text">{text}</p>
      <div class="testimonial-author"><img src="{img}" alt="{name}"><div><strong>{name}</strong><span>{role}</span></div></div>
    </div>"""

reviews = [
  ("Rahul Sharma","Software Engineer, Pune","Started my SIP journey with GroMoney 3 years ago. The personalised advice and quick support made all the difference. My portfolio has grown beautifully and I always know exactly where my money is.","https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=120&q=70"),
  ("Priya Mehta","Doctor, Mumbai","Got my term plan and health insurance done through them. They compared 8 insurers and found me the best premium. Saved nearly ₹4,000/year on premiums while getting better cover!","https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=120&q=70"),
  ("Amit Verma","Business Owner, Delhi","Personal loan got approved in 24 hours and the home loan team was patient enough to explain every step. Truly a one-stop financial solution.","https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=120&q=70"),
  ("Anita Joshi","Teacher, Jaipur","I had no idea about ELSS funds until they explained the tax benefits. Now I save ₹46,800 in tax every year while building wealth. Wish I had met them earlier!","https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=120&q=70"),
  ("Vikram Singh","Govt Employee, Lucknow","Completely transparent. They told me which products NOT to buy and that built so much trust. My retirement plan is now on track.","https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=120&q=70"),
  ("Sneha Iyer","Marketing Manager, Bangalore","CIBIL check was free, advice was free, and they helped me improve my score from 680 to 790 in 8 months. Got a premium credit card after that!","https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=120&q=70"),
  ("Karthik Reddy","Self-employed, Hyderabad","As a self-employed person, getting a home loan was tough. Their team did all the heavy lifting and got me approved at a great rate.","https://images.unsplash.com/photo-1564564321837-a57b7070ac4f?auto=format&fit=crop&w=120&q=70"),
  ("Meera Banerjee","Retired, Kolkata","At 62, I was worried no one would advise honestly. They suggested conservative debt funds and senior citizen health cover. Beautifully done.","https://images.unsplash.com/photo-1581579438747-104c53e7e0a8?auto=format&fit=crop&w=120&q=70"),
  ("Ravi Kumar","Engineer, Chennai","Travel insurance for my family Schengen trip was sorted in 10 minutes. Premium was lower than 3 other quotes I got. Loved the service.","https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=120&q=70"),
]
testi_body = page_hero(
  '<a href="index.html">Home</a> / Reviews',
  "What Our Clients Say",
  "Real stories from real investors who trusted us with their financial journey."
) + f"""
<section class="section">
  <div class="container">
    <div class="grid grid-3">
      {''.join(t_card(*r) for r in reviews)}
    </div>
    <div class="text-center mt-3"><a class="btn btn-primary" href="contact.html">Be Our Next Happy Client</a></div>
  </div>
</section>
"""
write("testimonials.html",
      {"title":"Client Reviews &amp; Testimonials | GroMoney Capital",
       "description":"Read genuine reviews from GroMoney Capital clients across India — mutual funds, insurance, loans &amp; more.",
       "keywords":"client reviews, GroMoney testimonials, NJ Wealth Partner reviews",
       "active":"rev"},
      testi_body)

# ============= LEGAL PAGES =============
def legal_page(slug, title, content_html):
    body = page_hero(
        f'<a href="index.html">Home</a> / {title}',
        title, "Last updated: 2026"
    ) + f"""
<section class="section">
  <div class="container" style="max-width: 880px;">
    {content_html}
  </div>
</section>"""
    write(slug, {"title": f"{title} | GroMoney Capital",
                 "description": f"{title} for the GroMoney Capital website.",
                 "keywords": f"{title.lower()}"}, body)

privacy = """
<h2>1. Information We Collect</h2>
<p>We collect personal information that you voluntarily provide when you contact us, fill out forms, or apply for products through our website. This may include your name, mobile number, email address, PAN, Aadhaar, income details and bank information needed to process applications.</p>

<h2>2. How We Use Your Information</h2>
<p>Your information is used to: (a) respond to your enquiries; (b) submit applications to our partner banks, AMCs, insurers and NBFCs on your behalf; (c) send you transactional updates; (d) provide ongoing financial advisory; (e) comply with regulatory and legal obligations.</p>

<h2>3. Sharing of Information</h2>
<p>We share your information with: (a) NJ Wealth (for mutual fund processing); (b) GroMo and its partner lenders/insurers; (c) regulators when legally required. We do <strong>not</strong> sell your data to third parties.</p>

<h2>4. Data Security</h2>
<p>We use industry-standard security measures including SSL encryption, secure servers and access controls. However, no online transmission is 100% secure and you transmit information at your own risk.</p>

<h2>5. Cookies</h2>
<p>Our website uses cookies for analytics and to improve user experience. You can disable cookies in your browser settings.</p>

<h2>6. Your Rights</h2>
<p>You may request access, correction or deletion of your personal data at any time by emailing <a href="mailto:contact@gromoneycapital.com">contact@gromoneycapital.com</a>.</p>

<h2>7. Updates to This Policy</h2>
<p>We may update this policy occasionally. The latest version will always be posted on this page.</p>

<h2>8. Contact</h2>
<p>For privacy questions, write to us at <a href="mailto:contact@gromoneycapital.com">contact@gromoneycapital.com</a>.</p>
"""

terms = """
<h2>1. Acceptance of Terms</h2>
<p>By using gromoneycapital.com, you agree to these Terms of Service. If you do not agree, please do not use the website.</p>

<h2>2. Nature of Services</h2>
<p>GroMoney Capital is an authorised mutual fund distributor under the NJ Wealth Partner network and operates as a referral partner for insurance, loans and credit cards. We <strong>do not</strong> provide investment advice and our recommendations are based on standard product features.</p>

<h2>3. No Investment Advice</h2>
<p>Information on this website is for general educational purposes only and is not personalised investment, legal or tax advice. Please consult a SEBI-registered investment advisor for personalised recommendations.</p>

<h2>4. Eligibility</h2>
<p>You must be at least 18 years of age and a resident of India to use the products and services available through this website.</p>

<h2>5. Third-Party Links</h2>
<p>Our site contains links to NJ Wealth, GroMo and other third-party sites. We are not responsible for the content, terms or privacy practices of those sites.</p>

<h2>6. Intellectual Property</h2>
<p>All content on this website (text, images, logos) is owned by GroMoney Capital or used with permission. You may not reproduce, distribute or modify it without written consent.</p>

<h2>7. Limitation of Liability</h2>
<p>Use of this website and any products applied for is at your own risk. GroMoney Capital is not liable for any losses arising from market movements, product performance, or third-party actions.</p>

<h2>8. Governing Law</h2>
<p>These terms are governed by the laws of India. Any disputes are subject to the jurisdiction of courts in India.</p>

<h2>9. Changes</h2>
<p>We reserve the right to modify these terms at any time. Continued use of the site implies acceptance of the updated terms.</p>
"""

disclaimer = """
<h2>General Disclaimer</h2>
<p>The information provided on this website is for general informational purposes only. While we strive to keep the information up-to-date and correct, we make no representations or warranties of any kind, express or implied, about the completeness, accuracy or reliability of the information.</p>

<h2>Mutual Funds</h2>
<p><strong>Mutual fund investments are subject to market risks. Read all scheme-related documents carefully before investing.</strong> Past performance is not indicative of future returns. The NAV of mutual fund schemes may go up or down depending on market conditions. GroMoney Capital is an AMFI-registered mutual fund distributor under the NJ Wealth Partner network and earns commission from the AMCs.</p>

<h2>Insurance</h2>
<p><strong>Insurance is a subject matter of solicitation.</strong> Please read the policy wordings, terms and exclusions carefully before concluding a sale. Premiums and benefits depend on individual underwriting and the specific insurer's terms. GroMoney Capital acts as a referral partner and does not act as an insurance broker or agent in the regulatory sense.</p>

<h2>Loans &amp; Credit Cards</h2>
<p>All loan and credit card approvals are at the sole discretion of the respective lenders/issuers. Interest rates, fees, eligibility criteria and processing times are determined by individual banks/NBFCs and are subject to change without notice. GroMoney Capital, through its partnership with GroMo, refers applications and earns referral fees from the lenders.</p>

<h2>No Guaranteed Returns</h2>
<p>No content on this website should be interpreted as a guarantee of returns or approval. All financial decisions should be made after considering your personal risk profile and consulting a qualified professional.</p>

<h2>Calculator Disclaimer</h2>
<p>The calculators on this website are for illustrative purposes only and are based on assumptions that may not reflect actual market or product performance. Actual returns, EMIs and outcomes may vary.</p>

<h2>External Links</h2>
<p>This website contains links to external websites including NJ Wealth (p.njw.bz) and GroMo (sales.gromo.in). GroMoney Capital is not responsible for the content, accuracy, or practices of these external websites.</p>
"""

legal_page("privacy-policy.html", "Privacy Policy", privacy)
legal_page("terms.html", "Terms of Service", terms)
legal_page("disclaimer.html", "Disclaimer", disclaimer)

print("Build complete.")
