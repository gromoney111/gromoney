/* GroMoney Capital - main.js */

document.addEventListener('DOMContentLoaded', () => {

  /* ---- Mobile menu toggle ---- */
  const toggle = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('active');
      navLinks.classList.toggle('open');
    });
    // Sub-menu toggle on mobile
    document.querySelectorAll('.nav-links .has-sub > a').forEach(a => {
      a.addEventListener('click', (e) => {
        if (window.innerWidth <= 720) {
          e.preventDefault();
          a.parentElement.classList.toggle('open');
        }
      });
    });
  }

  /* ---- FAQ accordion ---- */
  document.querySelectorAll('.faq-q').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.parentElement.classList.toggle('open');
    });
  });

  /* ---- Tabs ---- */
  document.querySelectorAll('.tabs').forEach(tabs => {
    const buttons = tabs.querySelectorAll('.tab-btn');
    const container = tabs.parentElement;
    buttons.forEach(b => b.addEventListener('click', () => {
      buttons.forEach(x => x.classList.remove('active'));
      b.classList.add('active');
      container.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      const pane = container.querySelector('#' + b.dataset.target);
      if (pane) pane.classList.add('active');
    }));
  });

  /* ---- Contact form (mailto fallback - works without backend) ---- */
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const data = new FormData(contactForm);
      const subject = encodeURIComponent('Enquiry from ' + (data.get('name') || 'Website'));
      const body = encodeURIComponent(
        'Name: ' + (data.get('name') || '') + '\n' +
        'Email: ' + (data.get('email') || '') + '\n' +
        'Phone: ' + (data.get('phone') || '') + '\n' +
        'Service: ' + (data.get('service') || '') + '\n\n' +
        'Message:\n' + (data.get('message') || '')
      );
      window.location.href = 'mailto:contact@gromoneycapital.com?subject=' + subject + '&body=' + body;
      const ok = document.getElementById('formOk');
      if (ok) ok.style.display = 'block';
    });
  }

  /* ---- Calculators ---- */
  initSIPCalc();
  initLumpsumCalc();
  initEMICalc();
  initGoalCalc();

  /* ---- Active link highlight ---- */
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href');
    if (href && href === path) a.classList.add('active');
  });

  /* ---- Footer year ---- */
  const yr = document.getElementById('year');
  if (yr) yr.textContent = new Date().getFullYear();
});

/* ===== Helpers ===== */
function fmtINR(n) {
  if (!isFinite(n)) return '₹0';
  return '₹' + Math.round(n).toLocaleString('en-IN');
}
function bindRange(rangeId, valueId, suffix = '') {
  const r = document.getElementById(rangeId);
  const v = document.getElementById(valueId);
  if (!r || !v) return;
  const update = () => v.textContent = Number(r.value).toLocaleString('en-IN') + suffix;
  r.addEventListener('input', update);
  update();
}

/* ===== SIP Calculator ===== */
function initSIPCalc() {
  const form = document.getElementById('sipCalc');
  if (!form) return;
  bindRange('sipAmount', 'sipAmountVal');
  bindRange('sipYears', 'sipYearsVal', ' yr');
  bindRange('sipReturn', 'sipReturnVal', '%');
  const calc = () => {
    const P = +document.getElementById('sipAmount').value;
    const yrs = +document.getElementById('sipYears').value;
    const r = +document.getElementById('sipReturn').value / 100 / 12;
    const n = yrs * 12;
    const fv = P * (((Math.pow(1 + r, n) - 1) / r) * (1 + r));
    const invested = P * n;
    document.getElementById('sipFV').textContent = fmtINR(fv);
    document.getElementById('sipInv').textContent = fmtINR(invested);
    document.getElementById('sipGain').textContent = fmtINR(fv - invested);
  };
  form.addEventListener('input', calc);
  calc();
}

/* ===== Lumpsum Calculator ===== */
function initLumpsumCalc() {
  const form = document.getElementById('lumpsumCalc');
  if (!form) return;
  bindRange('lsAmount', 'lsAmountVal');
  bindRange('lsYears', 'lsYearsVal', ' yr');
  bindRange('lsReturn', 'lsReturnVal', '%');
  const calc = () => {
    const P = +document.getElementById('lsAmount').value;
    const n = +document.getElementById('lsYears').value;
    const r = +document.getElementById('lsReturn').value / 100;
    const fv = P * Math.pow(1 + r, n);
    document.getElementById('lsFV').textContent = fmtINR(fv);
    document.getElementById('lsInv').textContent = fmtINR(P);
    document.getElementById('lsGain').textContent = fmtINR(fv - P);
  };
  form.addEventListener('input', calc);
  calc();
}

/* ===== EMI Calculator ===== */
function initEMICalc() {
  const form = document.getElementById('emiCalc');
  if (!form) return;
  bindRange('emiAmount', 'emiAmountVal');
  bindRange('emiYears', 'emiYearsVal', ' yr');
  bindRange('emiRate', 'emiRateVal', '%');
  const calc = () => {
    const P = +document.getElementById('emiAmount').value;
    const yrs = +document.getElementById('emiYears').value;
    const r = +document.getElementById('emiRate').value / 100 / 12;
    const n = yrs * 12;
    const emi = (P * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
    const total = emi * n;
    document.getElementById('emiVal').textContent = fmtINR(emi);
    document.getElementById('emiTotal').textContent = fmtINR(total);
    document.getElementById('emiInterest').textContent = fmtINR(total - P);
  };
  form.addEventListener('input', calc);
  calc();
}

/* ===== Goal Calculator (How much SIP needed for a goal) ===== */
function initGoalCalc() {
  const form = document.getElementById('goalCalc');
  if (!form) return;
  bindRange('goalAmount', 'goalAmountVal');
  bindRange('goalYears', 'goalYearsVal', ' yr');
  bindRange('goalReturn', 'goalReturnVal', '%');
  const calc = () => {
    const FV = +document.getElementById('goalAmount').value;
    const yrs = +document.getElementById('goalYears').value;
    const r = +document.getElementById('goalReturn').value / 100 / 12;
    const n = yrs * 12;
    const sip = FV / ((Math.pow(1 + r, n) - 1) / r * (1 + r));
    document.getElementById('goalSIP').textContent = fmtINR(sip);
    document.getElementById('goalInv').textContent = fmtINR(sip * n);
  };
  form.addEventListener('input', calc);
  calc();
}



/* ===== Scroll Reveal ===== */
(function () {
  const els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || !els.length) {
    els.forEach(e => e.classList.add('in'));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0, rootMargin: '0px 0px -10% 0px' });
  els.forEach(e => io.observe(e));
  // Safety: anything still hidden after 1.5s gets revealed (handles tall sections, low-power devices, etc.)
  setTimeout(() => {
    document.querySelectorAll('.reveal:not(.in)').forEach(e => e.classList.add('in'));
  }, 1500);
})();

/* ===== Animated Counter (count up) ===== */
(function () {
  const counters = document.querySelectorAll('[data-count]');
  if (!counters.length) return;
  const animate = (el) => {
    const target = +el.dataset.count;
    const suffix = el.dataset.suffix || '';
    const dur = 1600;
    const start = performance.now();
    const tick = (t) => {
      const p = Math.min((t - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased).toLocaleString('en-IN') + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { animate(e.target); io.unobserve(e.target); } });
    }, { threshold: 0.4 });
    counters.forEach(c => io.observe(c));
  } else counters.forEach(animate);
})();




/* ===== Lead-form modal (insurance enquiries) ===== */
(function () {
  const PHONE_DISPLAY = '+91 96640 19564';
  const WA = '919664019564';
  const EMAIL = 'contact@gromoneycapital.com';

  function ensureModal() {
    if (document.getElementById('leadModal')) return;
    const m = document.createElement('div');
    m.id = 'leadModal';
    m.className = 'lead-modal';
    m.setAttribute('role', 'dialog');
    m.setAttribute('aria-modal', 'true');
    m.innerHTML =
      '<div class="lm-backdrop" data-close></div>' +
      '<div class="lm-card">' +
      '<button class="lm-close" type="button" aria-label="Close" data-close>×</button>' +
      '<div id="lmBody">' +
      '<h3 id="lmTitle">Get Free Consultation</h3>' +
      '<p class="lm-sub" id="lmSub">Fill this quick form — our advisor will call you back within 1 working hour with the best premium quote.</p>' +
      '<form id="leadForm" class="lm-grid" novalidate>' +
        '<div class="full"><label for="lmName">Full Name *</label><input id="lmName" name="name" type="text" required autocomplete="name"></div>' +
        '<div><label for="lmPhone">Mobile *</label><input id="lmPhone" name="phone" type="tel" pattern="[0-9]{10}" maxlength="10" required autocomplete="tel" placeholder="10-digit number"></div>' +
        '<div><label for="lmEmail">Email</label><input id="lmEmail" name="email" type="email" autocomplete="email" placeholder="optional"></div>' +
        '<div class="full"><label for="lmInterest">Interested In *</label>' +
        '<select id="lmInterest" name="interest" required>' +
        '<option value="Life Insurance">Life Insurance</option>' +
        '<option value="Term Insurance">Term Insurance</option>' +
        '<option value="Health Insurance">Health Insurance</option>' +
        '<option value="Travel Insurance">Travel Insurance</option>' +
        '<option value="Mutual Funds / SIP">Mutual Funds / SIP</option>' +
        '<option value="General Financial Planning">General Financial Planning</option>' +
        '</select></div>' +
        '<div><label for="lmAge">Your Age</label><input id="lmAge" name="age" type="number" min="18" max="80" placeholder="optional"></div>' +
        '<div><label for="lmCallTime">Best Time to Call</label>' +
        '<select id="lmCallTime" name="callTime"><option>Any time</option><option>10 AM – 12 PM</option><option>12 PM – 3 PM</option><option>3 PM – 6 PM</option><option>6 PM – 8 PM</option></select></div>' +
        '<div class="full"><label for="lmMsg">Specific Need / Message</label><textarea id="lmMsg" name="message" placeholder="e.g. Need 1 Cr term plan for 35-yr non-smoker, family of 4..."></textarea></div>' +
        '<div class="full lm-actions">' +
        '<button type="submit" class="btn btn-primary">📨 Submit Enquiry</button>' +
        '<button type="button" class="btn btn-secondary" id="lmWhatsapp">💬 Send via WhatsApp</button>' +
        '</div>' +
        '<div class="full lm-trust">' +
        '<span>✓ <b>Free advisory</b></span>' +
        '<span>✓ <b>No spam calls</b></span>' +
        '<span>✓ <b>AMFI ARN: 270739</b></span>' +
        '<span>✓ <b>IRDA Registered</b></span>' +
        '</div>' +
      '</form>' +
      '</div></div>';
    document.body.appendChild(m);

    m.addEventListener('click', (e) => {
      if (e.target.matches('[data-close]')) closeLead();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && m.classList.contains('open')) closeLead();
    });

    document.getElementById('leadForm').addEventListener('submit', (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      if (!fd.get('name') || !/^\d{10}$/.test((fd.get('phone') || '').toString())) {
        alert('Please enter your name and a valid 10-digit mobile number.');
        return;
      }
      const subject = encodeURIComponent('Lead: ' + fd.get('interest') + ' — ' + fd.get('name'));
      const body = encodeURIComponent(buildLeadBody(fd));
      window.location.href = 'mailto:' + EMAIL + '?subject=' + subject + '&body=' + body;
      showLeadSuccess(fd.get('name'), fd.get('phone'));
    });

    document.getElementById('lmWhatsapp').addEventListener('click', () => {
      const fd = new FormData(document.getElementById('leadForm'));
      if (!fd.get('name') || !/^\d{10}$/.test((fd.get('phone') || '').toString())) {
        alert('Please enter your name and a valid 10-digit mobile number first.');
        return;
      }
      const text = encodeURIComponent(
        "Hi GroMoney Capital, I'd like a free consultation.\n\n" + buildLeadBody(fd)
      );
      window.open('https://wa.me/' + WA + '?text=' + text, '_blank');
      showLeadSuccess(fd.get('name'), fd.get('phone'));
    });
  }

  function buildLeadBody(fd) {
    return [
      'Name: ' + fd.get('name'),
      'Mobile: ' + fd.get('phone'),
      'Email: ' + (fd.get('email') || '—'),
      'Service: ' + fd.get('interest'),
      'Age: ' + (fd.get('age') || '—'),
      'Best time to call: ' + (fd.get('callTime') || 'Any time'),
      '',
      'Message:',
      (fd.get('message') || '—'),
      '',
      '(Sent from gromoneycapital.com lead form)'
    ].join('\n');
  }

  function showLeadSuccess(name, phone) {
    document.getElementById('lmBody').innerHTML =
      '<div class="lm-success">' +
        '<div class="check">✓</div>' +
        '<h3>Thank you, ' + (name || '').split(' ')[0] + '!</h3>' +
        '<p class="lm-sub">Your enquiry has been sent. Our advisor will call you on <b>+91 ' + phone + '</b> within 1 working hour.</p>' +
        '<p style="margin-top:14px;"><a href="tel:+919664019564" style="color:var(--color-primary); font-weight:600;">📞 Or call us now: ' + PHONE_DISPLAY + '</a></p>' +
        '<button class="btn btn-outline" style="margin-top:16px;" data-close>Close</button>' +
      '</div>';
  }

  function openLead(service) {
    ensureModal();
    const modal = document.getElementById('leadModal');
    const sel = document.getElementById('lmInterest');
    if (sel && service) {
      Array.from(sel.options).forEach((o) => {
        if (o.value === service || o.textContent === service) o.selected = true;
      });
    }
    const title = document.getElementById('lmTitle');
    if (title && service) title.textContent = 'Free ' + service + ' Consultation';
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
    setTimeout(() => {
      const nameEl = document.getElementById('lmName');
      if (nameEl) nameEl.focus();
    }, 200);
  }

  function closeLead() {
    const modal = document.getElementById('leadModal');
    if (!modal) return;
    modal.classList.remove('open');
    document.body.style.overflow = '';
  }

  window.openLeadForm = openLead;
  window.closeLeadForm = closeLead;

  // Auto-bind any element with [data-lead="ServiceName"]
  document.addEventListener('click', (e) => {
    const t = e.target.closest('[data-lead]');
    if (t) {
      e.preventDefault();
      openLead(t.getAttribute('data-lead'));
    }
  });
})();
