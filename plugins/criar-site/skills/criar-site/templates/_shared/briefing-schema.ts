/*
  Briefing Schema — contrato agnóstico que cada projeto cunhado pela skill /criar-site preenche.

  Este schema NÃO é a config de um kit. É o briefing destilado de UM projeto que vai ser
  materializado misturando matrizes (Portfolio Editorial / Clínica Estética / Tech Apple-ish).

  O `composer.py` (Etapa D) lê uma instância deste schema e:
    1. Importa os componentes da matriz `primary`
    2. Compõe `tokens.css` mixando os 5 token modules das matrizes escolhidas
    3. Renderiza `index.astro` orquestrando os slots ativos
    4. Adiciona slots signature opt-in das matrizes que os ofereceram

  Cada briefing produz UM template único — não há mais "site Portfolio puro" a ser clonado.
  O template é a síntese desta config.
*/

export type MatrixId = 'portfolio-editorial' | 'clinica-estetica' | 'tech-apple';

export type TokenModuleId = 'palette' | 'typography' | 'spacing' | 'motion' | 'radius';

/* ────────────────────────── MATRIZ ─────────────────────────── */

export interface MatrixComposition {
  /** Matriz que define ANATOMIA (estrutura dos componentes principais). */
  primary: MatrixId;

  /** Matriz que contribui com ingredientes secundários (paleta, mood, etc). Opcional. */
  secondary?: MatrixId;

  /** Terceira matriz pra projetos com mistura mais rica. Opcional. */
  tertiary?: MatrixId;

  /** Declaração de intenção em linguagem natural. Não é fórmula, é nota descritiva.
      Ex: "60% Editorial estrutural + 30% Clínica em paleta + 10% Tech em precisão de motion" */
  intent: string;
}

/* ───────────────────────── TOKENS ──────────────────────────── */

/** Cada token module vem de UMA matriz. Skill propõe distribuição que reflete o `intent`. */
export type TokenAssignment = Record<TokenModuleId, MatrixId>;

/* ─────────────────────── SLOTS PRINCIPAIS ──────────────────── */
/* Dados agnósticos que o composer traduz pra props da matriz primary. */

export interface HeaderSlot {
  brand: string;
  italic?: string;          // só matriz Clínica usa
  logoSrc?: string;
  nav?: { label: string; href: string }[];
  cta?: { label: string; href: string };
  sticky?: boolean;
}

export interface HeroSlot {
  /** Variante interna da matriz primary. Composer valida que o style pertence à primary.
      Portfolio: 'monumental-word' | 'editorial-phrase'
      Clínica:   'split' | 'fullbleed'
      Tech:      'product-floating' | 'product-isometric' */
  style: string;

  marker?: string;
  markerLabel?: string;
  word?: string;            // Portfolio monumental
  phrase?: string;          // Portfolio editorial
  heading?: string;         // Clínica + Tech
  headingItalic?: string;   // Clínica
  lead?: string;
  subline?: string;         // Tech
  ctaLabel?: string;
  ctaHref?: string;
  mediaSrc?: string;
  mediaType?: 'image' | 'video';
  mediaAlt?: string;
  mediaPosition?: string;   // CSS object-position / background-position
  poster?: string;
  heroOverlay?: 'none' | 'radial-bg' | 'blend-difference';

  // Tech-specific
  price?: string;
  badges?: string[];
}

export interface PitchSlot {
  marker?: string;
  markerLabel?: string;
  heading: string;
  body?: string;
  bodyRight?: string;
  italic?: string;          // Clínica
}

export interface GridSlot {
  marker?: string;
  markerLabel?: string;
  heading: string;
  layout?: '3-col' | '2-col' | 'stacked' | 'single-feature' | 'masonry';
  cardAspect?: '4/5' | '3/2' | '1/1' | '3/4';
  items: GridItem[];
}

export interface GridItem {
  marker?: string;
  title: string;
  subtitle?: string;
  description?: string;
  client?: string;
  year?: string;
  services?: string[];
  mediaSrc?: string;
  mediaAlt?: string;
  href?: string;
  // Specs Tech
  price?: string;
  // Clínica services
  duration?: string;
  icon?: string;
}

export interface GallerySlot {
  marker?: string;
  markerLabel?: string;
  heading?: string;
  layout?: 'grid-2' | 'grid-3' | 'carousel' | 'masonry' | 'feature-strip';
  items: { src: string; alt?: string; caption?: string }[];
}

export interface CTASlot {
  marker?: string;
  markerLabel?: string;
  heading: string;
  headingItalic?: string;   // Clínica
  body?: string;
  email?: string;           // Portfolio
  ctaLabel: string;
  ctaHref: string;
  secondaryCtaLabel?: string;
  secondaryCtaHref?: string;
  // Tech-specific
  price?: string;
  financing?: string;
  badges?: string[];
  productSrc?: string;
}

export interface FooterSlot {
  brand: string;
  italic?: string;          // Clínica
  tagline?: string;
  groups?: { label: string; links: { label: string; href: string }[] }[];
  meta?: { key: string; value: string }[];     // Portfolio
  finePrint?: string[];                        // Tech
  colophon?: string;
  copyright?: string;
  // Clínica-only
  address?: string;
  hours?: string;
  phone?: string;
  email?: string;
  socials?: { label: string; href: string }[];
}

/* ──────────────────── SLOTS SIGNATURE OPT-IN ──────────────── */
/* Cada slot signature pertence a uma matriz mas pode ser ativado por qualquer briefing. */

export interface MarqueeSlot {
  /** Signature do Portfolio. */
  items: string[];
  separator?: string;
  tone?: 'default' | 'accent';
}

export interface TestimonialsSlot {
  /** Signature da Clínica. */
  marker?: string;
  markerLabel?: string;
  heading?: string;
  items: { quote: string; author: string; role?: string; avatar?: string }[];
}

export interface SpecsSlot {
  /** Signature do Tech. */
  marker?: string;
  heading: string;
  groups: { label: string; rows: { key: string; value: string }[] }[];
}

export interface OrnamentSlot {
  /** Signature da Clínica. */
  variant?: 'wave' | 'leaf' | 'circles' | 'dots' | 'botanical';
  width?: string;
}

/* ──────────────────────── BRIEFING ROOT ────────────────────── */

export interface Briefing {
  /** Nome do projeto, slug, idioma, etc. */
  meta: {
    name: string;             // ex: "Atelier Norte"
    slug: string;             // "mezzanine"
    language: string;         // "pt-BR" | "en-US"
    description: string;      // SEO description
  };

  /** Composição de matrizes. */
  matrix: MatrixComposition;

  /** Distribuição dos 5 token modules entre as matrizes. */
  tokens: TokenAssignment;

  /** Ordem de renderização das seções. Cada item nomeia um slot ativo. */
  sectionOrder: SlotName[];

  /** Slots principais (data por slot). Slots não usados ficam ausentes. */
  slots: {
    header?: HeaderSlot;
    hero?: HeroSlot;
    pitch?: PitchSlot;
    grid?: GridSlot;
    gallery?: GallerySlot;
    cta?: CTASlot;
    footer?: FooterSlot;
  };

  /** Slots signature opt-in. Briefing escolhe quais ativar; cada um pode vir de qualquer matriz. */
  signatureSlots?: {
    marquee?: MarqueeSlot[];     // pode ter múltiplos no fluxo (entre seções)
    testimonials?: TestimonialsSlot;
    specs?: SpecsSlot;
    ornament?: OrnamentSlot;
  };

  /** Inventário real de assets. Composer decide layout do grid baseado nisso. */
  assetInventory?: {
    realProjectCount: number;     // se 1 → grid usa 'single-feature'
    hasRealHero: boolean;
    hasRealGallery: boolean;
  };
}

export type SlotName =
  | 'header'
  | 'hero'
  | 'pitch'
  | 'grid'
  | 'gallery'
  | 'cta'
  | 'footer'
  | 'marquee'
  | 'testimonials'
  | 'specs'
  | 'ornament-divider';
