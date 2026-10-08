// مسارات تعمل على السيرفر (الجذر "/") وعلى GitHub Pages (المسار الفرعي
// "/PharmFlow/") من نفس الكود: BASE_URL يضبطه astro.config من BASE_PATH.

const base = import.meta.env.BASE_URL.replace(/\/$/, '');

/** يضيف مسار القاعدة لأي مسار يبدأ بـ "/" (لا للروابط الخارجية ولا "#..."). */
export const withBase = (path: string): string =>
  path.startsWith('/') && !path.startsWith('//') ? `${base}${path}` : path;

// ملفات التثبيت لا تُحفظ في git (حجمها): على GitHub Pages تُخدم من GitHub
// Releases عبر PUBLIC_DOWNLOAD_BASE، وعلى السيرفر من /downloads محلياً.
const downloadBase = (import.meta.env.PUBLIC_DOWNLOAD_BASE as string | undefined)?.replace(/\/$/, '');

export const downloadHref = (file: string): string =>
  downloadBase ? `${downloadBase}/${file.split('/').pop()}` : withBase(file);
