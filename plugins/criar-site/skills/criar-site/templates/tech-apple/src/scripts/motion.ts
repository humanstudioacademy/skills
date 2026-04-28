/*
  Tech Apple-ish — motion system.
  Signature: movimento preciso, cinematic. Scroll hijacking SUTIL.
  GSAP + ScrollTrigger + Lenis. Respeita prefers-reduced-motion.

  - .reveal              — fade + translate-up preciso
  - .stagger-children    — filhos em sequência 70ms
  - [data-parallax]      — parallax vertical em produto/lifestyle (0.1-0.2 Apple-style)
  - [data-pin-product]   — produto permanece enquanto texto rola (scroll hijack sutil)
*/
import Lenis from 'lenis';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
  const lenis = new Lenis({
    duration: 1.1,
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

  // Reveal fade + translate (Apple-precise: curto e nítido)
  gsap.utils.toArray<HTMLElement>('.reveal').forEach((el) => {
    gsap.fromTo(
      el,
      { opacity: 0, y: 24 },
      {
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: 'cubic.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 88%',
          toggleActions: 'play none none reverse',
        },
      }
    );
  });

  // Stagger children
  gsap.utils.toArray<HTMLElement>('.stagger-children').forEach((container) => {
    const kids = Array.from(container.children) as HTMLElement[];
    gsap.fromTo(
      kids,
      { opacity: 0, y: 20 },
      {
        opacity: 1,
        y: 0,
        duration: 0.7,
        ease: 'cubic.out',
        stagger: 0.07,
        scrollTrigger: {
          trigger: container,
          start: 'top 85%',
          toggleActions: 'play none none reverse',
        },
      }
    );
  });

  // Parallax (Apple-style sutil)
  gsap.utils.toArray<HTMLElement>('[data-parallax]').forEach((el) => {
    const speed = parseFloat(el.dataset.parallax || '0.12');
    gsap.to(el, {
      yPercent: -speed * 25,
      ease: 'none',
      scrollTrigger: {
        trigger: el.parentElement || el,
        start: 'top bottom',
        end: 'bottom top',
        scrub: 0.5,
      },
    });
  });

  // Pin product (scroll hijack sutil — Apple product pages)
  gsap.utils.toArray<HTMLElement>('[data-pin-product]').forEach((el) => {
    ScrollTrigger.create({
      trigger: el.parentElement || el,
      start: 'top 20%',
      end: 'bottom 60%',
      pin: el,
      pinSpacing: false,
    });
  });

  // Carousel controls — auto-cycle active dot
  document.querySelectorAll<HTMLElement>('.carousel-controls').forEach((controls) => {
    const dots = controls.querySelectorAll<HTMLElement>('.dot');
    if (dots.length <= 1) return;
    let idx = 0;
    setInterval(() => {
      dots.forEach((d) => d.classList.remove('active'));
      idx = (idx + 1) % dots.length;
      dots[idx].classList.add('active');
    }, 3500);
  });

  // ── Product 3D tilt (hover) ──
  // <img data-product-tilt data-product-tilt-max="8" />
  gsap.utils.toArray<HTMLElement>('[data-product-tilt]').forEach((el) => {
    const max = parseFloat(el.dataset.productTiltMax || '8');
    el.style.transformStyle = 'preserve-3d';
    const parent = el.parentElement;
    if (parent) parent.style.perspective = '1000px';

    el.addEventListener('mousemove', (e: MouseEvent) => {
      const rect = el.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      gsap.to(el, {
        rotationY: x * max * 2,
        rotationX: -y * max * 2,
        duration: 0.4,
        ease: 'power2.out',
        transformPerspective: 1000,
      });
    });
    el.addEventListener('mouseleave', () => {
      gsap.to(el, { rotationY: 0, rotationX: 0, duration: 0.8, ease: 'expo.out' });
    });
  });

  // ── Stat counter — anima 0 → valor final preservando sufixo ──
  // <span data-stat-counter>340 m³/h</span> | "$499" | "99.97%"
  gsap.utils.toArray<HTMLElement>('[data-stat-counter]').forEach((el) => {
    const original = (el.textContent ?? '').trim();
    const match = original.match(/^(\D*)([\d,.]+)(.*)$/);
    if (!match) return;
    const [, prefix, numStr, suffix] = match;
    const targetNum = parseFloat(numStr.replace(/,/g, ''));
    if (isNaN(targetNum)) return;
    const isDecimal = numStr.includes('.');
    const decimals = isDecimal ? (numStr.split('.')[1]?.length ?? 0) : 0;

    const counter = { val: 0 };
    const render = () => {
      const v = isDecimal
        ? counter.val.toFixed(decimals)
        : Math.round(counter.val).toLocaleString('en-US');
      el.textContent = `${prefix}${v}${suffix}`;
    };
    render();

    ScrollTrigger.create({
      trigger: el,
      start: 'top 85%',
      once: true,
      onEnter: () => {
        gsap.to(counter, {
          val: targetNum,
          duration: 1.6,
          ease: 'expo.out',
          onUpdate: render,
        });
      },
    });
  });

  // ── Theme reveal (dark section revela via clip-path cinematográfico) ──
  // <section data-theme-reveal>
  gsap.utils.toArray<HTMLElement>('[data-theme-reveal]').forEach((section) => {
    gsap.fromTo(
      section,
      { clipPath: 'inset(100% 0 0 0)' },
      {
        clipPath: 'inset(0% 0 0 0)',
        duration: 1.4,
        ease: 'expo.out',
        scrollTrigger: {
          trigger: section,
          start: 'top 80%',
          toggleActions: 'play none none reverse',
        },
      }
    );
  });

  // ── Scroll-driven product scale ──
  // <div data-scroll-scale data-scroll-scale-from="0.92" data-scroll-scale-to="1.08">
  gsap.utils.toArray<HTMLElement>('[data-scroll-scale]').forEach((el) => {
    const from = parseFloat(el.dataset.scrollScaleFrom || '0.92');
    const to = parseFloat(el.dataset.scrollScaleTo || '1.08');
    gsap.fromTo(
      el,
      { scale: from },
      {
        scale: to,
        ease: 'none',
        scrollTrigger: {
          trigger: el.parentElement || el,
          start: 'top bottom',
          end: 'bottom top',
          scrub: 0.6,
        },
      }
    );
  });
}
