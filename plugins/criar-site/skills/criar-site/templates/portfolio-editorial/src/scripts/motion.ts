/*
  Portfolio Editorial — motion system.
  GSAP + ScrollTrigger + Lenis. Respeita prefers-reduced-motion.

  Signatures do kit:
  - .reveal                — fade + translate-up ao entrar
  - .stagger-children      — filhos em sequência stagger 80ms
  - [data-parallax="0.3"]  — parallax vertical scrubbed
  - [data-split-word]      — split word reveal (hero monumental)
  - [data-reveal-mask]     — clip-path image reveal
*/
import Lenis from 'lenis';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
  // ── Lenis smooth scroll ──
  const lenis = new Lenis({
    duration: 1.2,
    easing: (t: number) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    wheelMultiplier: 1,
    touchMultiplier: 2,
  });

  function raf(time: number) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }
  requestAnimationFrame(raf);

  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);

  // ── Reveal fade + translate ──
  gsap.utils.toArray<HTMLElement>('.reveal').forEach((el) => {
    gsap.fromTo(
      el,
      { opacity: 0, y: 28 },
      {
        opacity: 1,
        y: 0,
        duration: 0.9,
        ease: 'expo.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 88%',
          toggleActions: 'play none none reverse',
        },
      }
    );
  });

  // ── Stagger children ──
  gsap.utils.toArray<HTMLElement>('.stagger-children').forEach((container) => {
    const kids = Array.from(container.children) as HTMLElement[];
    gsap.fromTo(
      kids,
      { opacity: 0, y: 20 },
      {
        opacity: 1,
        y: 0,
        duration: 0.7,
        ease: 'expo.out',
        stagger: 0.08,
        scrollTrigger: {
          trigger: container,
          start: 'top 85%',
          toggleActions: 'play none none reverse',
        },
      }
    );
  });

  // ── Parallax ──
  gsap.utils.toArray<HTMLElement>('[data-parallax]').forEach((el) => {
    const speed = parseFloat(el.dataset.parallax || '0.3');
    gsap.to(el, {
      yPercent: -speed * 30,
      ease: 'none',
      scrollTrigger: {
        trigger: el.parentElement || el,
        start: 'top bottom',
        end: 'bottom top',
        scrub: true,
      },
    });
  });

  // ── Split word reveal (signature Portfolio monumental-word hero) ──
  gsap.utils.toArray<HTMLElement>('[data-split-word]').forEach((el) => {
    const text = el.textContent ?? '';
    el.innerHTML = text
      .split(/\s+/)
      .map((w) => `<span class="word"><span>${w}</span></span>`)
      .join(' ');
    const spans = el.querySelectorAll<HTMLElement>('.word > span');
    gsap.fromTo(
      spans,
      { yPercent: 110 },
      {
        yPercent: 0,
        duration: 1.1,
        ease: 'expo.out',
        stagger: 0.06,
        scrollTrigger: {
          trigger: el,
          start: 'top 85%',
          toggleActions: 'play none none reverse',
        },
      }
    );
  });

  // ── Image reveal mask ──
  gsap.utils.toArray<HTMLElement>('[data-reveal-mask]').forEach((el) => {
    gsap.fromTo(
      el,
      { clipPath: 'inset(100% 0 0 0)' },
      {
        clipPath: 'inset(0% 0 0 0)',
        duration: 1.4,
        ease: 'expo.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 85%',
          toggleActions: 'play none none reverse',
        },
      }
    );
  });

  // ── Magnetic cards (Portfolio signature) ──
  // <el data-magnetic="0.08"> — card "puxa" levemente o cursor
  gsap.utils.toArray<HTMLElement>('[data-magnetic]').forEach((el) => {
    const strength = parseFloat(el.dataset.magnetic || '0.1');
    el.addEventListener('mousemove', (e: MouseEvent) => {
      const rect = el.getBoundingClientRect();
      const dx = e.clientX - rect.left - rect.width / 2;
      const dy = e.clientY - rect.top - rect.height / 2;
      gsap.to(el, {
        x: dx * strength,
        y: dy * strength,
        duration: 0.5,
        ease: 'power2.out',
      });
    });
    el.addEventListener('mouseleave', () => {
      gsap.to(el, { x: 0, y: 0, duration: 0.8, ease: 'expo.out' });
    });
  });

  // ── Scramble text on scroll-in ──
  // <el data-scramble>TEXTO FINAL</el>
  // Chars desordenadas → texto real. Uma vez por view.
  const scrambleChars = '!<>-_\\/[]{}—=+*^?#________';
  gsap.utils.toArray<HTMLElement>('[data-scramble]').forEach((el) => {
    const original = (el.textContent ?? '').trim();
    el.dataset.scrambleOriginal = original;
    el.textContent = original.replace(/./g, () => scrambleChars[Math.floor(Math.random() * scrambleChars.length)]);

    const scramble = () => {
      let iteration = 0;
      const len = original.length;
      const intervalId = window.setInterval(() => {
        el.textContent = original
          .split('')
          .map((c, i) => {
            if (i < iteration) return original[i];
            if (c === ' ') return ' ';
            return scrambleChars[Math.floor(Math.random() * scrambleChars.length)];
          })
          .join('');
        iteration += 1 / 2;
        if (iteration >= len) {
          clearInterval(intervalId);
          el.textContent = original;
        }
      }, 45);
    };

    ScrollTrigger.create({
      trigger: el,
      start: 'top 85%',
      onEnter: scramble,
      once: true,
    });
  });

  // ── Marquee intro (hero monumental word rolling in) ──
  // <el data-marquee-intro>BRAND</el>
  gsap.utils.toArray<HTMLElement>('[data-marquee-intro]').forEach((el) => {
    gsap.fromTo(
      el,
      { xPercent: 30, opacity: 0 },
      {
        xPercent: 0,
        opacity: 1,
        duration: 1.8,
        ease: 'expo.out',
        delay: 0.1,
      }
    );
  });

  // ── Hover counter (slot machine em marker ao hover do card pai) ──
  // <span data-counter-hover>01</span> dentro de um .group
  gsap.utils.toArray<HTMLElement>('[data-counter-hover]').forEach((el) => {
    const original = (el.textContent ?? '').trim();
    const parent = el.closest<HTMLElement>('.group') ?? el.parentElement;
    if (!parent) return;
    let intervalId: number | null = null;

    parent.addEventListener('mouseenter', () => {
      if (intervalId) clearInterval(intervalId);
      let cycles = 0;
      intervalId = window.setInterval(() => {
        el.textContent = String(Math.floor(Math.random() * 100)).padStart(2, '0');
        cycles++;
        if (cycles > 9) {
          if (intervalId) clearInterval(intervalId);
          el.textContent = original;
        }
      }, 50);
    });

    parent.addEventListener('mouseleave', () => {
      if (intervalId) clearInterval(intervalId);
      el.textContent = original;
    });
  });
}
