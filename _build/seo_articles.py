#!/usr/bin/env python3
"""
Insert long-form SEO articles before the CTA banner in key product pages.
Idempotent: looks for an "article-marker" comment to skip if already inserted.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARKER = "<!-- SEO-ARTICLE-V1 -->"

ARTICLES = {
"mutual-funds.html": """
<section class="section section-alt">
  <div class="container">
    <h2 class="section-title reveal">The Complete Guide to Mutual Fund Investment in India (2026)</h2>
    <p class="section-sub reveal">Everything a smart Indian investor needs to know about SIP, ELSS, equity, debt &amp; hybrid funds.</p>
    <article class="article reveal">
      <h2>Why Mutual Funds Are India's #1 Wealth-Building Tool</h2>
      <p>India's mutual fund industry has crossed <strong>₹68 lakh crore in AUM</strong> as of 2026, with over 5 crore unique investors. The reason is simple — mutual funds offer professional management, diversification, liquidity and tax efficiency that no individual investor can replicate alone. Whether you have ₹500 a month or ₹50 lakh in lumpsum, there is a mutual fund scheme designed for your risk profile and time horizon.</p>

      <h2>SIP — The Magic of Disciplined Monthly Investing</h2>
      <p>A <strong>Systematic Investment Plan (SIP)</strong> lets you invest a fixed amount every month into a mutual fund of your choice. Three powerful concepts work in your favour:</p>
      <ul>
        <li><strong>Rupee-cost averaging:</strong> When markets fall, your fixed SIP buys more units; when they rise, you buy fewer. Over 5–10 years this smoothens the average buying price.</li>
        <li><strong>Power of compounding:</strong> Returns earned generate further returns. A monthly SIP of ₹10,000 at 12% p.a. for 25 years grows to ₹1.89 crore — even though you invest only ₹30 lakh.</li>
        <li><strong>Behavioural discipline:</strong> SIP auto-debits remove the temptation to time the market.</li>
      </ul>
      <p>Use our <a href="tools.html">SIP calculator</a> to see exactly how much your monthly investment can grow.</p>

      <h2>Types of Mutual Funds — Which One Is Right for You?</h2>
      <table>
        <tr><th>Type</th><th>Risk</th><th>Ideal For</th><th>Expected CAGR*</th></tr>
        <tr><td>Large-cap equity</td><td>Moderate</td><td>10+ year goals</td><td>10–13%</td></tr>
        <tr><td>Mid &amp; Small-cap</td><td>High</td><td>Aggressive 7+ year goals</td><td>13–18%</td></tr>
        <tr><td>Flexi-cap</td><td>Moderate</td><td>Core long-term holding</td><td>11–15%</td></tr>
        <tr><td>ELSS (tax saver)</td><td>Moderate-High</td><td>Section 80C + wealth</td><td>11–14%</td></tr>
        <tr><td>Hybrid / BAF</td><td>Moderate</td><td>3–5 year goals</td><td>9–11%</td></tr>
        <tr><td>Debt / Liquid</td><td>Low</td><td>Emergency fund, &lt;3 yr</td><td>6–8%</td></tr>
      </table>
      <p><em>*Indicative long-term ranges, not guaranteed. Past performance is not indicative of future returns.</em></p>

      <h2>Save Tax with ELSS — Up to ₹46,800 Every Year</h2>
      <p><strong>Equity Linked Savings Scheme (ELSS)</strong> is a special category of mutual fund that qualifies for a Section 80C tax deduction up to ₹1.5 lakh per year. With a tenure-locked-in for just 3 years (the shortest among all 80C options), it offers the dual benefit of tax saving and equity-market returns. Investors in the 30% slab save up to <strong>₹46,800 in tax</strong> every year while building long-term wealth.</p>

      <h2>How to Open Your Mutual Fund Account in 10 Minutes</h2>
      <ol>
        <li>Click "Open MF Account" — this takes you to our authorised <strong>NJ Wealth onboarding link</strong>.</li>
        <li>Fill in basic details: PAN, Aadhaar, mobile, email, bank account.</li>
        <li>Complete eKYC via Aadhaar OTP — fully paperless.</li>
        <li>Sign digitally using Aadhaar e-Sign.</li>
        <li>Receive your folio number and start your first SIP or lumpsum investment.</li>
      </ol>
      <blockquote>Pro tip: Set a SIP date between the 5th and 10th of the month — this is when most salaried investors get their salary credited and the auto-debit will rarely fail.</blockquote>

      <h2>Common Mistakes to Avoid</h2>
      <ul>
        <li><strong>Stopping SIPs in market crashes</strong> — this is when you should keep going to maximise rupee-cost averaging.</li>
        <li><strong>Chasing last year's top performer</strong> — last year's winner is rarely next year's winner.</li>
        <li><strong>Investing without a goal</strong> — every rupee should map to a goal (retirement, child, home).</li>
        <li><strong>Ignoring debt funds</strong> — even aggressive investors need 10–20% in debt for stability.</li>
        <li><strong>Direct vs Regular plans</strong> — Regular plans include advisor support, suitability checks and ongoing portfolio review. As an NJ Wealth Partner, our regular-plan advisory is free for life.</li>
      </ul>

      <h2>Why Choose GroMoney Capital as Your Distributor?</h2>
      <p>As an <strong>AMFI-registered Mutual Fund Distributor (ARN: 270739)</strong> under the NJ Wealth Partner network, GroMoney Capital gives you:</p>
      <ul>
        <li>Access to <strong>5,000+ schemes from 40+ AMCs</strong> — HDFC, ICICI Prudential, SBI, Axis, Kotak, Mirae, Nippon, DSP and more.</li>
        <li>Goal-based portfolio construction tailored to your income, risk profile and milestones.</li>
        <li>Single dashboard via the NJ Wealth platform to track your entire family's investments.</li>
        <li>Free quarterly review and rebalancing alerts.</li>
        <li>Lifetime relationship manager — call, WhatsApp or email anytime.</li>
        <li>Combined platform with insurance and credit products under one roof.</li>
      </ul>
      <p>Ready to begin? <a href="http://p.njw.bz/29511" target="_blank" rel="noopener"><strong>Open your free mutual fund account</strong></a> in 10 minutes, or <a href="contact.html">talk to our advisor</a> for personalised guidance.</p>
    </article>
  </div>
</section>
""",

"loans.html": """
<section class="section section-alt">
  <div class="container">
    <h2 class="section-title reveal">Loans &amp; Credit Cards in India — Complete 2026 Guide</h2>
    <p class="section-sub reveal">Compare, apply and get approved online for personal loan, home loan, auto loan and credit cards.</p>
    <article class="article reveal">
      <h2>Why Smart Borrowers Apply Through a Marketplace</h2>
      <p>Walking into a single bank branch limits you to that bank's products and rates. By applying through a digital marketplace like <strong>GroMoney Capital (powered by GroMo)</strong>, you tap into <strong>25+ lenders</strong> in one go — banks, NBFCs and fintechs — and receive pre-eligible offers tailored to your CIBIL score and income. This means lower interest rates, faster approvals and zero impact on your credit score until you formally accept an offer.</p>

      <h2>Personal Loan — Cash for Any Need, Within 24–72 Hours</h2>
      <p>An <strong>instant personal loan</strong> is unsecured and can be used for any purpose — wedding, medical emergency, home renovation, debt consolidation or vacation. Eligibility is based primarily on your income, employer category and credit score.</p>
      <ul>
        <li>Loan amount: ₹50,000 – ₹50 Lakh</li>
        <li>Tenure: 12–60 months</li>
        <li>Interest rate: from <strong>10.5% p.a.</strong> for prime borrowers</li>
        <li>Documents: PAN, Aadhaar, last 3 months bank statement, last 2 salary slips or ITR</li>
      </ul>
      <p>Use our <a href="tools.html">EMI calculator</a> to see what your monthly installment would look like.</p>

      <h2>Home Loan — Fulfill Your Dream of Owning a Home</h2>
      <p>A <strong>home loan</strong> is the largest financial commitment most Indians make. Even a 0.5% rate difference over 20 years can save you ₹4–5 lakh. We compare 25+ banks &amp; HFCs to find the lowest rate for your profile.</p>
      <table>
        <tr><th>Loan Type</th><th>Loan Amount</th><th>Tenure</th><th>Rate (from)</th></tr>
        <tr><td>Home Purchase</td><td>Up to ₹5 Cr</td><td>30 yrs</td><td>8.35% p.a.</td></tr>
        <tr><td>Construction Loan</td><td>Up to ₹3 Cr</td><td>20 yrs</td><td>8.50% p.a.</td></tr>
        <tr><td>Plot Loan</td><td>Up to ₹2 Cr</td><td>20 yrs</td><td>8.75% p.a.</td></tr>
        <tr><td>Balance Transfer</td><td>Existing loan</td><td>Remaining</td><td>8.20% p.a.</td></tr>
        <tr><td>Top-Up</td><td>Up to ₹50 L</td><td>15 yrs</td><td>9.00% p.a.</td></tr>
      </table>
      <p>Plus claim up to <strong>₹3.5 lakh annual tax benefit</strong> under Sections 80C (principal) and 24(b) (interest).</p>

      <h2>Credit Cards — Match the Card to Your Lifestyle</h2>
      <p>India has 30+ credit-card variants from leading banks. The right card can give you 1–6% cashback, free flight tickets, airport lounge access and zero forex markup on international spends. Common categories:</p>
      <ul>
        <li><strong>Lifetime Free Cards</strong> — no joining or annual fee, ever (e.g. IDFC FIRST Select, AU Bank LIT).</li>
        <li><strong>Travel Cards</strong> — air-mile accrual, lounge access, 0% forex markup (e.g. Axis Atlas, HDFC Diners).</li>
        <li><strong>Cashback Cards</strong> — 1–5% on spends (e.g. SBI Cashback, Cashback SBI Card).</li>
        <li><strong>Fuel Cards</strong> — surcharge waiver and fuel rewards.</li>
        <li><strong>Premium / Super-Premium</strong> — concierge, golf, hotel privileges (HDFC Infinia, Axis Magnus).</li>
      </ul>

      <h2>Improve Your CIBIL Score Before Applying</h2>
      <p>Your <strong>CIBIL score</strong> (300–900) is the single biggest factor in getting your loan or card approved. A score of <strong>750+</strong> unlocks the best rates and approvals; below 650 makes approvals difficult. Quick wins:</p>
      <ol>
        <li>Always pay credit-card and loan EMIs on or before the due date.</li>
        <li>Keep credit-card utilisation below 30% of your total limit.</li>
        <li>Don't apply for multiple cards/loans within a short time.</li>
        <li>Maintain a healthy mix of secured and unsecured credit.</li>
        <li>Don't close old credit cards — longer history = higher score.</li>
      </ol>
      <p>Check your CIBIL score for <a href="cibil-check.html"><strong>free in 2 minutes</strong></a> with no impact on the score.</p>

      <h2>Auto Loans — Drive Home Your Dream Car</h2>
      <p>Auto loans cover up to <strong>100% of on-road price</strong> for new cars (ex-showroom + insurance + RTO charges) at rates starting <strong>8.75% p.a.</strong> for tenures up to 7 years. Used-car loans, two-wheeler loans and EV loans are also available with attractive rates.</p>

      <h2>Why Apply Through GroMoney Capital?</h2>
      <ul>
        <li><strong>Pre-eligibility check</strong> before formal application — no CIBIL impact.</li>
        <li><strong>Best-rate offers</strong> from 25+ banks &amp; NBFCs in one click.</li>
        <li><strong>Paperless application</strong> with eKYC and eSign.</li>
        <li><strong>Personal advisor</strong> walks you through every step.</li>
        <li><strong>Zero charges</strong> to you — we earn referral commission from the lender.</li>
      </ul>
      <p>Ready to apply? Visit our <a href="financial-products.html"><strong>financial products marketplace</strong></a> or <a href="contact.html">talk to an advisor</a> for unbiased advice.</p>
    </article>
  </div>
</section>
""",

"insurance.html": """
<section class="section section-alt">
  <div class="container">
    <h2 class="section-title reveal">Insurance in India — A Practical Buyer's Guide (2026)</h2>
    <p class="section-sub reveal">Term, health, travel and life insurance — what to buy, how much cover, and the smartest way to save on premium.</p>
    <article class="article reveal">
      <h2>Why Insurance Is the Foundation of Every Financial Plan</h2>
      <p>Investments grow your wealth; insurance <em>protects</em> it. Without adequate insurance, one accident, illness or untimely demise can wipe out years of disciplined investing. Indians under-insure by 70% on average — making insurance the most-skipped yet most-important pillar of personal finance.</p>

      <h2>Term Insurance — The Cheapest, Smartest Life Cover</h2>
      <p>A <strong>term plan</strong> is pure life cover with no investment component, which is exactly why its premium is the lowest in the industry. A 30-year-old non-smoker can get <strong>₹1 crore cover for as little as ₹600/month</strong>.</p>
      <ul>
        <li><strong>How much cover?</strong> 10–15× your annual income, plus all outstanding loans.</li>
        <li><strong>Tenure?</strong> Up to age 60–65 (your retirement age).</li>
        <li><strong>Riders to add:</strong> critical illness, accidental death, waiver of premium on disability.</li>
        <li><strong>Look for:</strong> Claim Settlement Ratio (CSR) of 95%+, ideally with the IRDAI annual report.</li>
      </ul>
      <p>See our detailed <a href="term-insurance.html">term insurance guide</a>.</p>

      <h2>Health Insurance — One Hospital Bill Can Wipe Out Decades of Savings</h2>
      <p>Medical inflation in India runs at <strong>14% p.a.</strong> — twice general inflation. A 5-day hospitalisation for a heart attack can cost ₹4–8 lakh in a metro. Don't rely solely on your employer's group cover — it ends the moment you change or leave the job.</p>
      <table>
        <tr><th>Profile</th><th>Recommended Cover</th><th>Approx. Premium</th></tr>
        <tr><td>Single, age 25, metro</td><td>₹10–15 Lakh</td><td>₹6,000–₹10,000/yr</td></tr>
        <tr><td>Family of 4, age 30–35</td><td>₹15–25 Lakh floater</td><td>₹18,000–₹28,000/yr</td></tr>
        <tr><td>Senior citizen, age 60+</td><td>₹10–20 Lakh</td><td>₹35,000–₹70,000/yr</td></tr>
      </table>
      <p>Plus enjoy a <strong>₹75,000 tax deduction</strong> under Section 80D (₹25k self &amp; family + ₹50k senior parents). Read the <a href="health-insurance.html">health insurance details</a>.</p>

      <h2>Travel Insurance — Mandatory for Visa, Smart for Every Trip</h2>
      <p><strong>Travel insurance</strong> protects you from medical emergencies abroad (which can cost ₹50 lakh+ in the US), lost passport, baggage delay, trip cancellation and Covid-19 hospitalisation. Compulsory for Schengen and many other visas. Premium is just <strong>₹400–₹2,000 per trip</strong> depending on duration and destination. <a href="travel-insurance.html">Buy travel insurance</a> right after booking your flight.</p>

      <h2>Life Insurance for Savings &amp; Goals (ULIP, Endowment, Money-Back)</h2>
      <p>Beyond pure protection, life insurance plans like <strong>ULIPs, endowments and money-back policies</strong> combine guaranteed savings with life cover. They are ideal for risk-averse savers who want a fixed corpus for child education, marriage or retirement. Tax benefits under Section 80C (premium) and 10(10D) (maturity) make these popular among professionals. Explore <a href="life-insurance.html">life insurance options</a>.</p>

      <h2>How to Save on Insurance Premium — Insider Tips</h2>
      <ol>
        <li><strong>Buy young, buy long.</strong> Premium for term &amp; health insurance is lowest in your 20s and locks in for the entire policy term.</li>
        <li><strong>Compare 8+ insurers.</strong> Premium for the same cover can vary by ₹3,000–₹6,000/year. We compare for you free.</li>
        <li><strong>Disclose honestly.</strong> Hidden conditions = rejected claim. Transparency is non-negotiable.</li>
        <li><strong>Pay annually, not monthly.</strong> Annual premium typically saves 5% over monthly mode.</li>
        <li><strong>Top-up over re-buy.</strong> A super top-up health plan costs 30–50% less than a fresh higher-cover plan.</li>
      </ol>

      <h2>Why Buy Through GroMoney Capital?</h2>
      <ul>
        <li><strong>IRDA registered</strong> referral partner — fully compliant.</li>
        <li><strong>Compare 8+ insurers</strong> in minutes, no spam calls.</li>
        <li><strong>Lifetime claim assistance</strong> — we file the claim with the insurer for you.</li>
        <li><strong>Paperless purchase</strong> with eKYC and eSign.</li>
        <li><strong>Zero cost</strong> — we earn from the insurer, not you.</li>
      </ul>
      <p>Ready? <a href="https://sales.gromo.in/gp-website/g/0E9yO8aWdbur0QPHJaqDY" target="_blank" rel="noopener"><strong>Get a free quote</strong></a> or <a href="contact.html">book a free consultation</a>.</p>
    </article>
  </div>
</section>
"""
}

count = 0
for slug, html in ARTICLES.items():
    path = ROOT / slug
    s = path.read_text(encoding="utf-8")
    if MARKER in s:
        print(f"  skip {slug} (already has article)")
        continue
    # Insert before the first cta-banner section
    insertion = f"\n{MARKER}\n{html}\n"
    new_s, n = re.subn(
        r"(<section class=\"container\">\s*<div class=\"cta-banner\">)",
        insertion + r"\1",
        s, count=1
    )
    if n == 0:
        # fallback: insert before <footer>
        new_s = s.replace("<footer", insertion + "<footer", 1)
    path.write_text(new_s, encoding="utf-8")
    print(f"  inserted SEO article into {slug}")
    count += 1

print(f"Done. {count} pages got new articles.")
