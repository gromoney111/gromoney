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
  }, { threshold: 0.15 });
  els.forEach(e => io.observe(e));
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
