/*
  Clínica Estética — motion system.
  Signature: movimento lento, orgânico, nunca agressivo.
  GSAP + ScrollTrigger + Lenis. Respeita prefers-reduced-motion.

  - .reveal                — fade + translate-up lento (900ms)
  - .stagger-children      — filhos em sequência stagger 120ms (mais lento que Portfolio)
  - [data-parallax]        — parallax vertical scrubbed em fotografia
*/
import Lenis from 'lenis';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
  const lenis = new Lenis({
    duration: 1.5,
    easing: (t: number) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    wheelMultiplier: 0.9,
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

  // Reveal fade + translate lento — skip se elemento usa data-italic-reveal
  gsap.utils.toArray<HTMLElement>('.reveal').forEach((el) => {
    if (el.hasAttribute('data-italic-reveal')) return;
    gsap.fromTo(
      el,
      { opacity: 0, y: 24 },
      {
        opacity: 1,
        y: 0,
        duration: 1.1,
        ease: 'expo.out',
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
        duration: 0.9,
        ease: 'expo.out',
        stagger: 0.12,
        scrollTrigger: {
          trigger: container,
          start: 'top 88%',
          toggleActions: 'play none none reverse',
        },
      }
    );
  });

  // Parallax em fotografia
  gsap.utils.toArray<HTMLElement>('[data-parallax]').forEach((el) => {
    const speed = parseFloat(el.dataset.parallax || '0.2');
    gsap.to(el, {
      yPercent: -speed * 20,
      ease: 'none',
      scrollTrigger: {
        trigger: el.parentElement || el,
        start: 'top bottom',
        end: 'bottom top',
        scrub: true,
      },
    });
  });

  // ── Breathing (ornaments + gallery items) ──
  // <el data-breathing data-breathing-scale="1.03" data-breathing-delay="0.5">
  gsap.utils.toArray<HTMLElement>('[data-breathing]').forEach((el) => {
    const delay = parseFloat(el.dataset.breathingDelay || '0');
    const scale = parseFloat(el.dataset.breathingScale || '1.03');
    const duration = parseFloat(el.dataset.breathingDuration || '3.5');
    const brightness = el.dataset.breathingBrightness
      ? parseFloat(el.dataset.breathingBrightness)
      : null;

    const target: gsap.TweenVars = {
      scale,
      duration,
      ease: 'sine.inOut',
      yoyo: true,
      repeat: -1,
      delay,
    };
    if (brightness !== null) {
      target.filter = `brightness(${brightness})`;
    }
    gsap.to(el, target);
  });

  // ── Italic letter reveal ──
  // <h1 data-italic-reveal>
  //   Beauty is a conversation
  //   <span class="italic-emphasis">Ours is listening first.</span>
  // </h1>
  // Split palavras em spans; italic words entram depois com delay + stagger maior.
  gsap.utils.toArray<HTMLElement>('[data-italic-reveal]').forEach((el) => {
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    const textNodes: Text[] = [];
    let n: Node | null;
    while ((n = walker.nextNode())) textNodes.push(n as Text);

    textNodes.forEach((tn) => {
      const parent = tn.parentElement;
      const isItalic = !!parent?.classList.contains('italic-emphasis');
      const words = (tn.textContent ?? '').split(/(\s+)/);
      const frag = document.createDocumentFragment();
      words.forEach((w) => {
        if (/^\s+$/.test(w)) {
          frag.appendChild(document.createTextNode(w));
        } else if (w.length) {
          const span = document.createElement('span');
          span.textContent = w;
          span.style.display = 'inline-block';
          span.classList.add('iword');
          if (isItalic) span.classList.add('iword-italic');
          frag.appendChild(span);
        }
      });
      tn.replaceWith(frag);
    });

    const roman = el.querySelectorAll<HTMLElement>('.iword:not(.iword-italic)');
    const italics = el.querySelectorAll<HTMLElement>('.iword-italic');

    gsap.set([...roman, ...italics], { opacity: 0, y: 18 });

    gsap.to(roman, {
      opacity: 1,
      y: 0,
      duration: 0.9,
      ease: 'expo.out',
      stagger: 0.05,
      scrollTrigger: {
        trigger: el,
        start: 'top 85%',
        toggleActions: 'play none none reverse',
      },
    });
    if (italics.length) {
      gsap.to(italics, {
        opacity: 1,
        y: 0,
        duration: 1.2,
        ease: 'expo.out',
        stagger: 0.09,
        delay: 0.35,
        scrollTrigger: {
          trigger: el,
          start: 'top 85%',
          toggleActions: 'play none none reverse',
        },
      });
    }
  });
}
