/*
  Clínica Estética — Kit Config
  Contrato entre o briefing da Skill /criar-site e o kit.
  Paleta, ornamentos e tipografia são variáveis do briefing — defaults fortes.
*/

export type PaletteDef = {
  name: string;
  label: string;
  bg: string;
  deep: string;
  mid: string;
  accent: string;
};

export const clinicaEsteticaKit = {
  id: 'clinica-estetica',
  archetype: 'Wellness editorial — serif curvilinear romântica + paleta muted quente + retratos humanos + ornamentos orgânicos. Ritmo respirado.',

  /*  Variáveis editáveis pelo briefing.  */
  editableTokens: {
    palette: {
      type: 'enum',
      default: 'sage',
      rule: 'Tudo muted/dessaturado. Se briefing pedir saturado, redirecionar pra Portfolio Editorial.',
      presets: [
        { name: 'sage',       label: 'Sage (default — mais testado)',      bg: '#F5EEE6', deep: '#2E3A2E', mid: '#E5D5C8', accent: '#B8923D' },
        { name: 'rose-taupe', label: 'Rose-taupe (warm romantic)',         bg: '#F8F2EC', deep: '#6B4E48', mid: '#EFD5C3', accent: '#B8923D' },
        { name: 'sand',       label: 'Sand/Desert (terracotta)',           bg: '#F5EFE4', deep: '#8C5A3C', mid: '#D9C7A8', accent: '#B8923D' },
        { name: 'warm-nude',  label: 'Warm nude (pearl chocolate)',        bg: '#F9F2EA', deep: '#3E2A1F', mid: '#D4BFA8', accent: '#B8923D' },
      ] as PaletteDef[],
    },
    displayFont: {
      type: 'font-stack',
      default: 'fraunces',
      source: 'google-fonts',
      options: {
        'fraunces':         { stack: `'Fraunces', 'Bodoni Moda', Georgia, serif`,           label: 'Fraunces (default — serif expressiva variável)',    googleFamily: 'Fraunces:ital,opsz,wght@0,9..144,400..900;1,9..144,400..900' },
        'bodoni-moda':      { stack: `'Bodoni Moda', 'Fraunces', Georgia, serif`,           label: 'Bodoni Moda (didone alta, luxuosa)',                googleFamily: 'Bodoni+Moda:ital,opsz,wght@0,6..96,400..900;1,6..96,400..900' },
        'playfair-display': { stack: `'Playfair Display', 'Bodoni Moda', Georgia, serif`,   label: 'Playfair Display (editorial clássico)',             googleFamily: 'Playfair+Display:ital,wght@0,400..900;1,400..900' },
        'cormorant-garamond': { stack: `'Cormorant Garamond', 'Fraunces', Georgia, serif`,  label: 'Cormorant Garamond (alta, etérea)',                 googleFamily: 'Cormorant+Garamond:ital,wght@0,300..700;1,300..700' },
        'dm-serif-display': { stack: `'DM Serif Display', 'Fraunces', Georgia, serif`,      label: 'DM Serif Display (fashion poster)',                 googleFamily: 'DM+Serif+Display:ital@0;1' },
      },
    },
    bodyFont: {
      type: 'font-stack',
      default: 'inter',
      source: 'google-fonts',
      options: {
        'inter':   { stack: `'Inter', system-ui, sans-serif`,            label: 'Inter (sans humanista neutra)', googleFamily: 'Inter:wght@300..800' },
        'dm-sans': { stack: `'DM Sans', 'Inter', system-ui, sans-serif`, label: 'DM Sans (geométrica clean)',    googleFamily: 'DM+Sans:opsz,wght@9..40,300..800' },
        'manrope': { stack: `'Manrope', 'Inter', system-ui, sans-serif`, label: 'Manrope (humanista moderna)',   googleFamily: 'Manrope:wght@300..800' },
      },
    },
    ornamentStyle: {
      type: 'enum',
      default: 'botanical-line',
      description: 'Estilo de ornamento decorativo. Sugerir conforme briefing; se rejeitar botânico, oferecer abstrato/minimal.',
      options: {
        'botanical-line':  { label: 'Linhas onduladas botânicas (default)' },
        'abstract-organic':{ label: 'Formas abstratas orgânicas (blobs, curvas)' },
        'minimal-circle':  { label: 'Círculos concêntricos e pontos (leveza/paz)' },
        'none':            { label: 'Sem ornamentos — só tipografia + espaço' },
      },
    },
  },

  /*  Variantes de componentes.  */
  componentVariants: {
    hero: ['split-portrait', 'fullbleed-blur', 'collage-polaroid'],
    servicesGrid: ['3-col-icons', '4-col-icons', 'list-horizontal'],
    header: ['logo-center', 'logo-left-simple'],
  },

  /*  Envelope — atributos que FOGEM do DNA deste kit.
      ADVISORY, não bloqueio: um briefing que pede item desta lista + o resto alinhado
      sugere MISTURA (DNA híbrido). Ver feedback_kits_hibridizaveis em memory.  */
  rejects: [
    'grotesque-condensed-display',  // isso é Portfolio Editorial
    'saturated-accent',             // idem
    'rectangular-buttons',          // idem — aqui é pill
    'no-human-portrait',            // kit EXIGE retrato humano em algum lugar
    'dark-mode-primary',            // Clínica é sempre light warm
    'product-floating-hero',        // Tech Apple-ish
  ],

  /*  Defaults estruturais.  */
  structuralDefaults: {
    sectionOrder: [
      'Hero split',
      'Mission centered',
      'Services grid',
      'Space gallery',
      'Testimonials carousel',
      'Booking CTA',
    ],
    buttonStyle: 'pill',
    navLayout: 'logo-center-minimal',
    requirePortrait: true, // kit exige pelo menos UMA imagem com retrato humano
  },
} as const;

export type ClinicaEsteticaKit = typeof clinicaEsteticaKit;
