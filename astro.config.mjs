// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://eloo.digital',
  build: {
    // single-page marketing site: inline all CSS so the built index.html
    // is self-contained (no separate /_astro/*.css request needed)
    inlineStylesheets: 'always',
  },
});
