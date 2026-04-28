/*
  Tech Apple-ish — Kit Config
  DNA: Apple-like product showcase — produto flutuante + sans geométrica bold +
  paleta fria + period no final de títulos + light/dark variant.
*/

export type AccentDef = {
  name: string;
  label: string;
  value: string;
};

export const techAppleKit = {
  id: 'tech-apple',
  archetype: 'Apple-like product showcase — produto flutuante como herói, sans geométrica bold com periods, paleta fria neutra, precisão cinematic.',

  editableTokens: {
    mode: {
      type: 'enum',
      default: 'light',
      options: {
        'light':    { label: 'Light mode (default)' },
        'dark':     { label: 'Dark mode (variante nativa)' },
        'alternating': { label: 'Alternating — seções intercaladas light/dark' },
      },
      description: 'Kit suporta ambos os modos como variante nativa. Briefing escolhe ritmo.',
    },
    accent: {
      type: 'color',
      default: 'apple-blue',
      rule: 'Accent único por site. Neutro frio sempre — nunca warm/cream (rompe o arquétipo).',
      presets: [
        { name: 'apple-blue',      value: '#0071E3', label: 'Apple blue (default)' },
        { name: 'startup-purple',  value: '#6C5CE7', label: 'Startup purple' },
        { name: 'hardware-green',  value: '#30D158', label: 'Hardware green' },
        { name: 'gaming-red',      value: '#FF453A', label: 'Gaming red' },
        { name: 'creator-orange',  value: '#FF6B35', label: 'Creator orange' },
        { name: 'ai-cyan',         value: '#64D2FF', label: 'AI cyan' },
      ] as AccentDef[],
    },
    displayFont: {
      type: 'font-stack',
      default: 'inter',
      source: 'google-fonts',
      options: {
        'inter':            { stack: `'Inter', system-ui, -apple-system, sans-serif`,                       label: 'Inter (default — SF Pro-like)',                           googleFamily: 'Inter:wght@300..900' },
        'space-grotesk':    { stack: `'Space Grotesk', 'Inter', system-ui, sans-serif`,                      label: 'Space Grotesk (tech-ish, mais carregado)',                googleFamily: 'Space+Grotesk:wght@300..700' },
        'bricolage-grotesque': { stack: `'Bricolage Grotesque', 'Inter', system-ui, sans-serif`,             label: 'Bricolage Grotesque (Apple-ish display)',                 googleFamily: 'Bricolage+Grotesque:opsz,wght@12..96,200..800' },
        'plus-jakarta-sans': { stack: `'Plus Jakarta Sans', 'Inter', system-ui, sans-serif`,                 label: 'Plus Jakarta Sans (cleaner, SaaS)',                       googleFamily: 'Plus+Jakarta+Sans:wght@300..800' },
        'manrope':          { stack: `'Manrope', 'Inter', system-ui, sans-serif`,                            label: 'Manrope (humanista moderna)',                              googleFamily: 'Manrope:wght@300..800' },
      },
    },
    bodyFont: {
      type: 'font-stack',
      default: 'inter',
      source: 'google-fonts',
      note: 'Default é Inter — displayFont e bodyFont podem ser a mesma família (Apple style).',
      options: {
        'inter':   { stack: `'Inter', system-ui, sans-serif`,            label: 'Inter (default)',               googleFamily: 'Inter:wght@300..900' },
        'dm-sans': { stack: `'DM Sans', 'Inter', system-ui, sans-serif`, label: 'DM Sans',                       googleFamily: 'DM+Sans:opsz,wght@9..40,300..800' },
        'manrope': { stack: `'Manrope', 'Inter', system-ui, sans-serif`, label: 'Manrope',                       googleFamily: 'Manrope:wght@300..800' },
      },
    },
    monoFont: {
      type: 'font-stack',
      default: null,        // opt-in via briefing
      optIn: true,
      source: 'google-fonts',
      description: 'Monospace usado em labels/specs/stats. Opt-in pra sites AI/dev/data — forçar em todo site tech quebra Apple-ness.',
      options: {
        'jetbrains-mono': { stack: `'JetBrains Mono', ui-monospace, monospace`,  label: 'JetBrains Mono',  googleFamily: 'JetBrains+Mono:wght@400..700' },
        'ibm-plex-mono':  { stack: `'IBM Plex Mono', ui-monospace, monospace`,   label: 'IBM Plex Mono',   googleFamily: 'IBM+Plex+Mono:wght@300..700' },
        'geist-mono':     { stack: `'Geist Mono', ui-monospace, monospace`,      label: 'Geist Mono',      googleFamily: 'Geist+Mono:wght@300..700' },
      },
    },
  },

  componentVariants: {
    hero: ['product-floating', 'product-lifestyle', 'dark-cinematic'],
    highlights: ['video-carousel', 'static-grid', 'stat-grid'],
    buyCTA: ['split-financing', 'centered-simple', 'sticky-pill'],
  },

  /*  Envelope — atributos que FOGEM do DNA deste kit.
      ADVISORY, não bloqueio: briefing que pede item desta lista + resto alinhado sugere
      MISTURA (DNA híbrido). Ver feedback_kits_hibridizaveis em memory.  */
  rejects: [
    'warm-palette',           // cream/sage — pertence à Clínica
    'serif-expressive',       // idem
    'grotesque-condensed',    // pertence ao Portfolio
    'saturated-accent',       // Portfolio — aqui accent é neutro frio
    'asymmetric-grid',        // Portfolio — aqui é centralizado puro
    'human-portrait-hero',    // Clínica — aqui é produto
    'botanical-ornament',     // Clínica — aqui é zero ornamento
  ],

  structuralDefaults: {
    sectionOrder: [
      'Hero (product-floating)',
      'Get the highlights (carousel)',
      'Take a closer look (close-ups)',
      'Feature cards',
      'Specs/benchmarks',
      'Buy CTA',
    ],
    buttonStyle: 'pill-apple',  // pill preto ou accent
    navLayout: 'apple-top-small',
    productIsHero: true,         // kit exige produto flutuante em algum momento
    periodInTitles: true,        // signature — títulos terminam em period
  },
} as const;

export type TechAppleKit = typeof techAppleKit;
