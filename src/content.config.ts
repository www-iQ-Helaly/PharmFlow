import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'zod';

/**
 * إصدارات المنتج — تُستخدم في قسم «ما الجديد» وصفحة الإصدارات (لاحقًا).
 * لا تُضاف أي نسخة إلا بعد تأكيد فريق المنتج.
 *
 * البنية المستقبلية للغات (كل لغة في مجلد مستقل):
 *   src/content/releases/ar/release-1.mdx
 *   src/content/releases/en/release-1.mdx
 * وتُفلتر الإدخالات حسب اللغة عبر بادئة المعرّف (id) في المكوّنات.
 */
const releases = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/releases' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    version: z.string().optional(),
    status: z.enum(['completed', 'current', 'planned', 'roadmap']).default('current'),
  }),
});

export const collections = { releases };