/**
 * CENTRE NOBLESSE SCHOOL — ANIMATIONS ENGINE
 * Vanilla JS integration of all 7 custom_features components:
 *  1. BlurText       → hero h1 words
 *  2. SplitText      → hero-desc paragraph words
 *  3. ScrollReveal   → stats section heading words (blur+fade scrub)
 *  4. ClickSpark     → all CTA buttons (canvas sparks on click)
 *  5. StarBorder     → pack-card animated border (CSS-driven, JS init)
 *  6. MagicBento     → gw-cards & stat-cards (mouse glow + particles)
 *  7. PillNav        → nav-links hover circle lift
 *  +  ScrollBar      → thin top progress bar
 *  +  CountUp        → stats counter numbers
 * Brand: #D1000E red | #66C0FF blue | #FFFFFF white
 */
(function () {
  'use strict';

  /* ─── Utility ──────────────────────────────────────────────────── */
  const $ = (sel, ctx) => (ctx || document).querySelector(sel);
  const $$ = (sel, ctx) => Array.from((ctx || document).querySelectorAll(sel));

  /* Respect reduced-motion */
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ════════════════════════════════════════════════════════════════
     1. SCROLL PROGRESS BAR
     ═════════════════════════════════════════════════════════════ */
  function initScrollBar() {
    const bar = document.createElement('div');
    bar.id = 'cn-scroll-bar';
    bar.setAttribute('aria-hidden', 'true');
    document.body.prepend(bar);

    function update() {
      const scrolled = window.scrollY;
      const total = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = total > 0 ? ((scrolled / total) * 100).toFixed(2) + '%' : '0%';
    }
    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  /* ════════════════════════════════════════════════════════════════
     2. BLUR TEXT  (custom_features/Blur Text)
        Splits text inside .cn-blur-target into individual
        <span class="cn-blur-word"> elements, then fires them
        in sequence once the element enters the viewport.
     ═════════════════════════════════════════════════════════════ */
  function initBlurText() {
    const targets = $$('.cn-blur-target');
    if (!targets.length) return;

    targets.forEach(el => {
      const delay = parseInt(el.dataset.blurDelay || '140', 10); // ms per word
      const direction = el.dataset.blurDir || 'top';              // top | bottom

      // Preserve original text for accessibility
      const originalHTML = el.innerHTML;

      // Split by words (preserve whitespace between)
      const html = el.innerHTML;
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = html;

      // Walk text nodes only, wrap each word
      function wrapWords(node) {
        if (node.nodeType === Node.TEXT_NODE) {
          const words = node.textContent.split(/(\s+)/);
          const frag = document.createDocumentFragment();
          words.forEach(w => {
            if (/^\s+$/.test(w) || w === '') {
              frag.appendChild(document.createTextNode(w));
            } else {
              const span = document.createElement('span');
              span.className = 'cn-blur-word';
              span.style.animationPlayState = 'paused';
              if (direction === 'bottom') {
                span.style.transform = 'translateY(20px)';
              }
              span.textContent = w;
              frag.appendChild(span);
            }
          });
          node.parentNode.replaceChild(frag, node);
        } else {
          Array.from(node.childNodes).forEach(wrapWords);
        }
      }

      wrapWords(tempDiv);
      el.innerHTML = tempDiv.innerHTML;

      const wordSpans = $$('.cn-blur-word', el);

      // IntersectionObserver fires words staggered
      const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            if (reducedMotion) {
              wordSpans.forEach(s => { s.style.opacity = '1'; s.style.filter = 'none'; s.style.transform = 'none'; });
            } else {
              wordSpans.forEach((span, i) => {
                span.style.animationDelay = `${i * delay}ms`;
                span.style.animationPlayState = 'running';
              });
            }
            observer.unobserve(el);
          }
        });
      }, { threshold: 0.15 });

      observer.observe(el);
    });
  }

  /* ════════════════════════════════════════════════════════════════
     3. SPLIT TEXT  (custom_features/Split Text)
        Words slide up with stagger on scroll entry.
        Targets elements with class .cn-split-target
     ═════════════════════════════════════════════════════════════ */
  function initSplitText() {
    const targets = $$('.cn-split-target');
    if (!targets.length) return;

    targets.forEach(el => {
      const delay = parseInt(el.dataset.splitDelay || '55', 10);

      // Split text node words
      const words = el.textContent.split(/(\s+)/);
      el.innerHTML = '';
      el.classList.add('cn-split-parent');

      words.forEach(w => {
        if (/^\s+$/.test(w) || w === '') {
          el.appendChild(document.createTextNode(w));
        } else {
          const span = document.createElement('span');
          span.className = 'cn-split-word';
          span.style.animationPlayState = 'paused';
          span.textContent = w;
          el.appendChild(span);
        }
      });

      const wordSpans = $$('.cn-split-word', el);

      const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            if (reducedMotion) {
              wordSpans.forEach(s => { s.style.opacity = '1'; s.style.transform = 'none'; });
            } else {
              wordSpans.forEach((span, i) => {
                span.style.animationDelay = `${i * delay}ms`;
                span.style.animationPlayState = 'running';
              });
            }
            observer.unobserve(el);
          }
        });
      }, { threshold: 0.2, rootMargin: '-60px' });

      observer.observe(el);
    });
  }

  /* ════════════════════════════════════════════════════════════════
     4. SCROLL REVEAL  (custom_features/Scroll Reveal)
        Words inside .cn-scroll-reveal get class is-revealed as
        user scrolls — creating a word-by-word blur unfurl.
     ═════════════════════════════════════════════════════════════ */
  function initScrollReveal() {
    const targets = $$('.cn-scroll-reveal');
    if (!targets.length) return;

    targets.forEach(el => {
      const delay = parseInt(el.dataset.srDelay || '60', 10);

      // Split into words
      const text = el.textContent;
      el.innerHTML = '';
      const words = text.split(/(\s+)/);

      words.forEach(w => {
        if (/^\s+$/.test(w) || w === '') {
          el.appendChild(document.createTextNode(w));
        } else {
          const span = document.createElement('span');
          span.className = 'cn-scroll-word';
          span.textContent = w;
          el.appendChild(span);
        }
      });

      const wordSpans = $$('.cn-scroll-word', el);
      let fired = false;

      const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting && !fired) {
            fired = true;
            if (reducedMotion) {
              wordSpans.forEach(s => s.classList.add('is-revealed'));
            } else {
              wordSpans.forEach((span, i) => {
                setTimeout(() => span.classList.add('is-revealed'), i * delay);
              });
            }
            observer.unobserve(el);
          }
        });
      }, { threshold: 0.3, rootMargin: '-80px' });

      observer.observe(el);
    });
  }

  /* ════════════════════════════════════════════════════════════════
     5. CLICK SPARK  (custom_features/Click Spark)
        Canvas overlay on every .cn-spark-host element.
        Draws radial line sparks in brand colours on click.
     ═════════════════════════════════════════════════════════════ */
  function initClickSpark() {
    if (reducedMotion) return;

    // Brand colours for sparks: red + blue alternating
    const SPARK_COLORS = ['#D1000E', '#66C0FF', '#FFFFFF', '#FF5560'];
    const SPARK_COUNT   = 10;
    const SPARK_RADIUS  = 28;
    const SPARK_SIZE    = 9;
    const DURATION      = 480; // ms

    function easeOut(t) { return t * (2 - t); }

    function createSparkCanvas(host) {
      host.classList.add('cn-spark-host');
      host.style.position = host.style.position || 'relative';

      const canvas = document.createElement('canvas');
      canvas.className = 'cn-spark-canvas';
      canvas.setAttribute('aria-hidden', 'true');
      host.appendChild(canvas);

      let sparks = [];
      let raf = null;
      let running = false;

      function resizeCanvas() {
        const rect = host.getBoundingClientRect();
        canvas.width  = (rect.width  || host.offsetWidth) + 100;
        canvas.height = (rect.height || host.offsetHeight) + 100;
        canvas.style.top = '-50px';
        canvas.style.left = '-50px';
      }

      const ro = new ResizeObserver(resizeCanvas);
      ro.observe(host);
      resizeCanvas();

      function draw(ts) {
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        sparks = sparks.filter(sp => {
          const elapsed  = ts - sp.startTime;
          if (elapsed >= DURATION) return false;

          const progress = elapsed / DURATION;
          const eased    = easeOut(progress);
          const distance = eased * SPARK_RADIUS;
          const lineLen  = SPARK_SIZE * (1 - eased);

          const x1 = sp.x + distance * Math.cos(sp.angle);
          const y1 = sp.y + distance * Math.sin(sp.angle);
          const x2 = sp.x + (distance + lineLen) * Math.cos(sp.angle);
          const y2 = sp.y + (distance + lineLen) * Math.sin(sp.angle);

          ctx.globalAlpha = 1 - eased * 0.6;
          ctx.strokeStyle = sp.color;
          ctx.lineWidth   = 2;
          ctx.lineCap     = 'round';
          ctx.beginPath();
          ctx.moveTo(x1, y1);
          ctx.lineTo(x2, y2);
          ctx.stroke();
          ctx.globalAlpha = 1;
          return true;
        });

        if (sparks.length > 0) {
          raf = requestAnimationFrame(draw);
        } else {
          running = false;
        }
      }

      host.addEventListener('click', e => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const now = performance.now();

        for (let i = 0; i < SPARK_COUNT; i++) {
          sparks.push({
            x,
            y,
            angle:     (2 * Math.PI * i) / SPARK_COUNT,
            startTime: now,
            color:     SPARK_COLORS[i % SPARK_COLORS.length]
          });
        }

        if (!running) {
          running = true;
          raf = requestAnimationFrame(draw);
        }
      });
    }

    // Apply to all CTA buttons
    const sparkTargets = $$(
      '.btn-red, .btn-explore, .btn-pack, .btn-blue, #nav-register-btn, [data-open-modal]'
    );
    sparkTargets.forEach(el => {
      // Avoid double-init
      if (!el.querySelector('.cn-spark-canvas')) {
        createSparkCanvas(el);
      }
    });
  }

  /* ════════════════════════════════════════════════════════════════
     6. MAGIC BENTO  (custom_features/Magic Bento)
        Mouse-tracking radial glow + tilt + particle burst on hover.
        Targets: .gw-card and .stat-card
     ═════════════════════════════════════════════════════════════ */
  function initMagicBento() {
    if (reducedMotion) return;

    const isMobile = window.innerWidth <= 768;
    if (isMobile) return;

    const cards = $$('.cn-bento-card');
    if (!cards.length) return;

    cards.forEach(card => {
      let particles = [];
      let hovered   = false;
      let ticking   = false;

      // ── Mouse-tracking glow ──────────────────────────────────
      card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const relX = ((e.clientX - rect.left) / rect.width)  * 100;
        const relY = ((e.clientY - rect.top)  / rect.height) * 100;

        card.style.setProperty('--glow-x', `${relX}%`);
        card.style.setProperty('--glow-y', `${relY}%`);
        card.style.setProperty('--glow-intensity', '1');

        // Subtle tilt
        if (!ticking) {
          ticking = true;
          requestAnimationFrame(() => {
            const cx = rect.width  / 2;
            const cy = rect.height / 2;
            const rotX = ((e.clientY - rect.top  - cy) / cy) * -6;
            const rotY = ((e.clientX - rect.left - cx) / cx) *  6;
            card.style.transform =
              `perspective(900px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-4px)`;
            ticking = false;
          });
        }
      });

      card.addEventListener('mouseenter', () => {
        hovered = true;
        card.style.setProperty('--glow-intensity', '0.85');
        spawnParticles(card);
      });

      card.addEventListener('mouseleave', () => {
        hovered = false;
        card.style.setProperty('--glow-intensity', '0');
        card.style.transform = '';
        clearParticles(card, particles);
        particles = [];
      });

      // Click ripple
      card.addEventListener('click', e => {
        const rect  = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const maxD = Math.max(
          Math.hypot(x, y),
          Math.hypot(x - rect.width, y),
          Math.hypot(x, y - rect.height),
          Math.hypot(x - rect.width, y - rect.height)
        );

        const ripple = document.createElement('div');
        ripple.className = 'cn-ripple';
        const d = maxD * 2;
        const glowColor = getComputedStyle(card).getPropertyValue('--glow-color').trim() || '209, 0, 14';
        ripple.style.cssText = `
          width:${d}px; height:${d}px;
          left:${x - maxD}px; top:${y - maxD}px;
          background: radial-gradient(circle,
            rgba(${glowColor},0.4) 0%,
            rgba(${glowColor},0.15) 40%,
            transparent 70%);
        `;
        card.appendChild(ripple);
        ripple.addEventListener('animationend', () => ripple.remove());
      });
    });

    // ── Particle helpers ────────────────────────────────────────
    function spawnParticles(card) {
      const rect = card.getBoundingClientRect();
      const glowColorRaw = getComputedStyle(card).getPropertyValue('--glow-color').trim() || '209, 0, 14';
      const count = 8;

      for (let i = 0; i < count; i++) {
        setTimeout(() => {
          if (!card.classList.contains('cn-bento-card')) return;

          const p = document.createElement('div');
          p.className = 'cn-particle';
          p.style.left    = Math.random() * rect.width  + 'px';
          p.style.top     = Math.random() * rect.height + 'px';
          p.style.background     = `rgba(${glowColorRaw}, 1)`;
          p.style.boxShadow      = `0 0 6px rgba(${glowColorRaw}, 0.6)`;
          p.style.opacity        = '0';
          p.style.transform      = 'scale(0)';
          p.style.transition     = 'opacity 0.3s ease, transform 0.3s ease';
          card.appendChild(p);

          requestAnimationFrame(() => {
            p.style.opacity   = '1';
            p.style.transform = 'scale(1)';
          });

          // Float animation
          let dx = (Math.random() - 0.5) * 60;
          let dy = (Math.random() - 0.5) * 60;
          let dir = 1;
          let startT = null;

          function floatStep(ts) {
            if (!startT) startT = ts;
            const t = ((ts - startT) % 3000) / 3000;
            const sin = Math.sin(t * Math.PI * 2);
            p.style.transform = `scale(1) translate(${dx * sin * 0.5}px, ${dy * sin * 0.5}px)`;
            if (card.contains(p)) requestAnimationFrame(floatStep);
          }
          requestAnimationFrame(floatStep);
        }, i * 80);
      }
    }

    function clearParticles(card) {
      $$('.cn-particle', card).forEach(p => {
        p.style.opacity   = '0';
        p.style.transform = 'scale(0)';
        setTimeout(() => p.remove(), 350);
      });
    }
  }

  /* ════════════════════════════════════════════════════════════════
     7. PILL NAV  (custom_features/Pill Nav)
        Injects hover-circle span + label-stack span into each
        .nav-link, enabling the CSS circle-expand hover effect.
     ═════════════════════════════════════════════════════════════ */
  function initPillNav() {
    const navLinks = $$('.nav-links .nav-link');
    if (!navLinks.length) return;

    navLinks.forEach(link => {
      const text = link.textContent.trim();
      link.innerHTML = '';

      // Hover circle background
      const circle = document.createElement('span');
      circle.className = 'pill-hover-circle';
      circle.setAttribute('aria-hidden', 'true');
      link.appendChild(circle);

      // Size the circle to cover the pill
      function sizePill() {
        const w = link.offsetWidth;
        const h = link.offsetHeight;
        const R = ((w * w / 4) + (h * h)) / (2 * h);
        const D = Math.ceil(2 * R) + 4;
        const delta = Math.ceil(R - Math.sqrt(Math.max(0, R * R - (w * w / 4)))) + 2;
        circle.style.width  = `${D}px`;
        circle.style.height = `${D}px`;
        circle.style.bottom = `-${delta}px`;
      }

      // Label stack
      const stack = document.createElement('span');
      stack.className = 'pill-label-stack';

      const lbl = document.createElement('span');
      lbl.className = 'pill-label-text';
      lbl.textContent = text;
      stack.appendChild(lbl);

      link.appendChild(stack);

      if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(sizePill);
      } else {
        sizePill();
      }
      window.addEventListener('resize', sizePill, { passive: true });
    });
  }

  /* ════════════════════════════════════════════════════════════════
     8. COUNT-UP  — Stats numbers animate on scroll reveal
        Replaces the existing basic count-up for smoother easing
     ═════════════════════════════════════════════════════════════ */
  function initCountUp() {
    const counters = $$('.count-up');
    if (!counters.length) return;

    function easeOutQuart(t) { return 1 - Math.pow(1 - t, 4); }

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;

        const el       = entry.target;
        const target   = parseInt(el.dataset.target, 10);
        const duration = 1800;
        const start    = performance.now();

        el.classList.add('counting');

        function step(ts) {
          const elapsed  = ts - start;
          const progress = Math.min(elapsed / duration, 1);
          const value    = Math.round(easeOutQuart(progress) * target);
          el.textContent = value.toLocaleString('fr-DZ');
          if (progress < 1) {
            requestAnimationFrame(step);
          } else {
            el.textContent = target.toLocaleString('fr-DZ');
            el.classList.remove('counting');
          }
        }

        requestAnimationFrame(step);
        observer.unobserve(el);
      });
    }, { threshold: 0.5 });

    counters.forEach(c => {
      if (reducedMotion) {
        c.textContent = parseInt(c.dataset.target, 10).toLocaleString('fr-DZ');
      } else {
        c.textContent = '0';
        observer.observe(c);
      }
    });
  }

  /* ════════════════════════════════════════════════════════════════
     9. STAR BORDER  (custom_features/Star Border)
        Wraps each .pack-card with the star-border structure:
        adds border-gradient-bottom + border-gradient-top divs,
        and the .sb-inner wrapper. Pure CSS animates them.
     ═════════════════════════════════════════════════════════════ */
  function initStarBorder() {
    const packCards = $$('.pack-card');
    if (!packCards.length) return;

    packCards.forEach(card => {
      // Already done guard
      if (card.classList.contains('star-border-container')) return;

      // Wrap existing content in .sb-inner
      const inner = document.createElement('div');
      inner.className = 'sb-inner';
      // Move children into inner
      while (card.firstChild) inner.appendChild(card.firstChild);

      // Add gradient layers
      const gradBottom = document.createElement('div');
      gradBottom.className = 'border-gradient-bottom';
      gradBottom.setAttribute('aria-hidden', 'true');

      const gradTop = document.createElement('div');
      gradTop.className = 'border-gradient-top';
      gradTop.setAttribute('aria-hidden', 'true');

      card.appendChild(gradBottom);
      card.appendChild(gradTop);
      card.appendChild(inner);
      card.classList.add('star-border-container');
    });
  }

  /* ════════════════════════════════════════════════════════════════
     10. MAGIC BENTO CLASSES — add .cn-bento-card to targets
     ═════════════════════════════════════════════════════════════ */
  function tagBentoCards() {
    $$('.gw-card').forEach(c  => c.classList.add('cn-bento-card'));
    $$('.stat-card').forEach(c => c.classList.add('cn-bento-card'));
  }

  /* ════════════════════════════════════════════════════════════════
     11. ENHANCED REVEAL — existing .reveal elements
         Slightly improved from the base implementation:
         uses IntersectionObserver with staggered delay
     ═════════════════════════════════════════════════════════════ */
  function initReveal() {
    const reveals = $$('.reveal');
    if (!reveals.length) return;

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '-40px' });

    reveals.forEach(el => observer.observe(el));
  }

  /* ════════════════════════════════════════════════════════════════
     12. ADMIN GATEWAY (Triple Click on Logo)
     ═════════════════════════════════════════════════════════════ */
  function initAdminGateway() {
    const logo = $('.logo');
    if (!logo) return;

    let clickCount = 0;
    let clickTimer = null;

    logo.addEventListener('click', (e) => {
      clickCount++;
      
      if (clickCount >= 3) {
        // Trigger the secret admin gateway on triple click
        e.preventDefault();
        e.stopPropagation();
        
        const adminModal = $('#modal-admin');
        if (adminModal) {
          adminModal.classList.add('open');
          document.body.style.overflow = 'hidden';
          setTimeout(() => {
            const input = $('#a-username');
            if (input) input.focus();
          }, 450);
        }
        
        // Reset
        clickCount = 0;
        clearTimeout(clickTimer);
      } else {
        // Normal click behavior (navigate to home) is allowed to pass through
        // unless it reaches 3 clicks within 500ms
        clearTimeout(clickTimer);
        clickTimer = setTimeout(() => {
          clickCount = 0;
        }, 500);
      }
    });

    // ── AJAX login intercept — sends FormData so Flask-WTF CSRF validates ──
    const adminForm = $('#admin-login-form');
    if (adminForm) {
      adminForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const errDiv   = $('#admin-error');
        const btn      = adminForm.querySelector('button[type="submit"]');
        const origHTML = btn.innerHTML;

        // Hide previous errors, show loading state
        errDiv.style.display = 'none';
        btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2.5" stroke-linecap="round" style="animation:spin 0.8s linear infinite;vertical-align:middle">
          <path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg> Validation…`;
        btn.disabled = true;

        // Build FormData (includes csrf_token hidden field automatically)
        const fd = new FormData(adminForm);

        try {
          const res  = await fetch(adminForm.action, {
            method:  'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            body:    fd
          });

          let data = {};
          try { data = await res.json(); } catch(_) {}

          if (res.ok && data.status === 'success') {
            // ── Success: flash green then redirect ──────────────────
            btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg> Accès Autorisé`;
            btn.style.background = 'linear-gradient(135deg, #22c55e, #16a34a)';
            btn.style.boxShadow  = '0 0 20px rgba(34,197,94,0.4)';
            setTimeout(() => { window.location.href = data.redirect; }, 500);

          } else {
            // ── Failure: show inline message ────────────────────────
            throw new Error(data.message || 'Identifiants invalides.');
          }

        } catch (err) {
          errDiv.textContent    = err.message;
          errDiv.style.display  = 'block';
          // Shake animation on the modal box
          const box = document.querySelector('#modal-admin .modal-box');
          if (box) {
            box.style.animation = 'adminShake 0.4s cubic-bezier(.36,.07,.19,.97)';
            box.addEventListener('animationend', () => { box.style.animation = ''; }, { once: true });
          }
          btn.innerHTML = origHTML;
          btn.disabled  = false;
        }
      });
    }
  }

  /* ════════════════════════════════════════════════════════════════
     INITIALISE — DOMContentLoaded
     ═════════════════════════════════════════════════════════════ */
  function init() {
    initScrollBar();
    tagBentoCards();
    initStarBorder();
    initReveal();
    initBlurText();
    initSplitText();
    initScrollReveal();
    initCountUp();
    initPillNav();
    initMagicBento();
    initClickSpark();  // last — so canvas sits on top of everything
    initAdminGateway();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
