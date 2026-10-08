import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';

// SITE_URL: public origin of the VPS deployment, e.g. https://pharmflow.example.com
const site = process.env.SITE_URL ?? 'https://example.com';
// BASE_PATH: "/" على السيرفر، "/PharmFlow/" على GitHub Pages.
const base = process.env.BASE_PATH ?? '/';

// https://astro.build/config
export default defineConfig({
  site,
  base,
  i18n: {
    defaultLocale: 'ar',
    locales: ['ar', 'en'],
    fallback: { en: 'ar' },
  },
  integrations: [mdx()],
  vite: {
    plugins: [tailwindcss()],
  },
});