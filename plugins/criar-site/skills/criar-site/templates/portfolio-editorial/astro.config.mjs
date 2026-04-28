import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
  },
  compressHTML: true,
  prefetch: {
    prefetchAll: false,
    defaultStrategy: 'hover',
  },
});
