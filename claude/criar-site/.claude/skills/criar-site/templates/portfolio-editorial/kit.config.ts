/*
  Portfolio Editorial — Kit Config
  Contrato entre o briefing da Skill /criar-site e o kit.
  A Skill lê este arquivo pra saber o que é editável, o que é envelope, e o que rejeita.
  Defaults são fortes — quem não responder nada ainda sai com site coerente.
*/

export type KitAccent = {
  name: string;
  value: string;
  label: string;
};

export const portfolioEditorialKit = {
  id: 'portfolio-editorial',
  archetype: 'Studio criativo editorial — tipografia é a atração, mídia é o prop, 1 cor saturada é a pontuação',

  /*  Variáveis editáveis pelo briefing.
      A Skill injeta estes valores no tokens.css antes do build.  */
  editableTokens: {
    accent: {
      type: 'color',
      envelope: 'saturated',
      default: '#1E2BFF',
      presets: [
        { name: 'royal-blue',   value: '#1E2BFF', label: 'Royal blue (Kuya, Glided)' },
        { name: 'cadmium-red',  value: '#E23B1E', label: 'Cadmium red (Glided, magazines)' },
        { name: 'cad-yellow',   value: '#F5C528', label: 'Cad yellow (Glided, editorial)' },
        { name: 'electric-green', value: '#00E676', label: 'Electric green' },
        { name: 'magenta',      value: '#FF1493', label: 'Magenta (punk editorial)' },
      ] as KitAccent[],
      rule: 'Usar apenas UMA cor accent por site. Nunca cream/pewter/muted.',
    },
    displayFont: {
      type: 'font-stack',
      default: 'anton',
      source: 'google-fonts',
      options: {
        // Grotesque condensed (tonicidade DNA principal)
        'anton':                { stack: `'Anton', 'Impact', system-ui, sans-serif`,           label: 'Anton (default — grotesque condensed)',        googleFamily: 'Anton' },
        'bebas-neue':           { stack: `'Bebas Neue', 'Anton', 'Impact', system-ui, sans-serif`, label: 'Bebas Neue (condensed, clean)',             googleFamily: 'Bebas+Neue' },
        'archivo-black':        { stack: `'Archivo Black', 'Impact', system-ui, sans-serif`,   label: 'Archivo Black (black, not condensed)',         googleFamily: 'Archivo+Black' },
        'big-shoulders-display':{ stack: `'Big Shoulders Display', 'Anton', system-ui, sans-serif`, label: 'Big Shoulders Display (variable wght)',  googleFamily: 'Big+Shoulders+Display:wght@400..900' },
        'oswald':               { stack: `'Oswald', 'Bebas Neue', system-ui, sans-serif`,      label: 'Oswald (condensed, corporate)',                googleFamily: 'Oswald:wght@400..700' },
        // Serif expressive (variante DNA — usar quando briefing pede editorial literário)
        'fraunces':             { stack: `'Fraunces', 'Bodoni Moda', Georgia, serif`,          label: 'Fraunces (serif expressive variant)',          googleFamily: 'Fraunces:ital,opsz,wght@0,9..144,400..900;1,9..144,400..900' },
        'bodoni-moda':          { stack: `'Bodoni Moda', 'Fraunces', Georgia, serif`,          label: 'Bodoni Moda (didone contrast)',                googleFamily: 'Bodoni+Moda:ital,opsz,wght@0,6..96,400..900;1,6..96,400..900' },
        'playfair-display':     { stack: `'Playfair Display', 'Bodoni Moda', Georgia, serif`,  label: 'Playfair Display (editorial classic)',         googleFamily: 'Playfair+Display:ital,wght@0,400..900;1,400..900' },
        'dm-serif-display':     { stack: `'DM Serif Display', 'Fraunces', Georgia, serif`,     label: 'DM Serif Display (fashion poster)',            googleFamily: 'DM+Serif+Display:ital@0;1' },
      },
    },
    bodyFont: {
      type: 'font-stack',
      default: 'inter',
      source: 'google-fonts',
      options: {
        'inter':    { stack: `'Inter', system-ui, sans-serif`,       label: 'Inter (default — sans neutra)',     googleFamily: 'Inter:wght@300..800' },
        'dm-sans':  { stack: `'DM Sans', 'Inter', system-ui, sans-serif`, label: 'DM Sans (geométrica clean)',   googleFamily: 'DM+Sans:opsz,wght@9..40,300..800' },
        'manrope':  { stack: `'Manrope', 'Inter', system-ui, sans-serif`, label: 'Manrope (humanista moderna)',  googleFamily: 'Manrope:wght@300..800' },
      },
    },
    foundationLightness: {
      type: 'enum',
      default: 'off-white',
      options: {
        'off-white':   { bg: '#F5F4F0', label: 'Off-white (default, editorial)' },
        'near-white':  { bg: '#FAFAF8', label: 'Near-white (clean)' },
        'warm-grey':   { bg: '#EDEAE3', label: 'Warm grey (arquivista)' },
      },
    },
    displayContrastRatio: {
      type: 'number',
      min: 8,
      max: 20,
      default: 12,
      description: 'Ratio display-to-body — maior = mais escultural, menor = mais editorial-magazine',
    },
  },

  /*  Props de variação nos componentes de seção.
      A Skill passa estas escolhas via props do Astro no index.astro gerado.  */
  componentVariants: {
    hero: ['monumental-word', 'editorial-phrase'],
    workGrid: ['3-col', 'stacked', 'masonry'],
    marker: ['alphabetic', 'numeric', 'mixed'],  // (A)(B)  vs  (01)(02)  vs  (01/03)
  },

  /*  Envelope — atributos que FOGEM do DNA deste kit.
      IMPORTANTE: rejects são ADVISORY, não bloqueio absoluto.
      Se um briefing pede algo daqui mas o restante é consistente com o kit, isso
      indica **mistura** (DNA híbrido) — não contradição. O engine pode compor um
      preamble híbrido primary=portfolio-editorial + secondary={outro-kit} com proporção
      declarada (ex: 80/20). Ver feedback_kits_hibridizaveis em memory.

      Só bloqueia quando a mistura resulta em contradição coerente (ex: 100% puro
      serif romântica + tagline SF Pro Bold com periods).  */
  rejects: [
    'warm-palette',           // caminha pra Clínica (mistura possível)
    'humanistic-serif',       // caminha pra Clínica (mistura possível)
    'pill-buttons',           // caminha pra Clínica ou Tech
    'centered-only-grid',     // caminha pra Tech Apple-ish
    'product-floating-hero',  // caminha pra Tech Apple-ish
    'dark-mode-default',      // caminha pra Tech Apple-ish (variante nativa do Tech)
  ],

  /*  Defaults estruturais — recomendação padrão se briefing não especificar.  */
  structuralDefaults: {
    sectionOrder: [
      'Hero monumental',
      'Editorial pitch',
      'Work grid',
      'Case study preview',
      'Clients marquee',
      'Contact CTA',
    ],
    buttonStyle: 'rectangular-minimal',
    navLayout: 'tri-partite', // logo-left + nav-center + cta-right
  },
} as const;

export type PortfolioEditorialKit = typeof portfolioEditorialKit;
