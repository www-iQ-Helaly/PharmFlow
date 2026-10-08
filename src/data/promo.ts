import type { Lang } from '../i18n/translations';

// عرض الجمعة السوداء + هوية الشركة المالكة (طلب المالك 2026-10-08).
// السعران كما حدّدهما المالك حرفياً؛ لا مدة عرض لأن المالك لم يحددها.

export interface PromoCopy {
  badge: string;
  title: string;
  lead: string;
  oldPrice: string;
  newPrice: string;
  discount: string;
  saveLabel: string;
  cta: string;
  ctaHint: string;
  whatsappText: string;
  company: string;
  companyLine: string;
  whatsappLabel: string;
}

export const promo: Record<Lang, PromoCopy> = {
  ar: {
    badge: 'عرض الجمعة السوداء',
    title: 'خصم ⁦50%⁩ على PharmFlow',
    lead: 'نظام إدارة الصيدلية الكامل — البيع بالباركود، المخزون والصلاحية، فريق العمل، والنسخ الاحتياطي السحابي — بنصف السعر.',
    oldPrice: '$1200',
    newPrice: '$600',
    discount: '-50%',
    saveLabel: 'وفّر ⁦$600⁩',
    cta: 'جرّب البرنامج عبر واتساب',
    ctaHint: 'راسلنا لتحصل على نسخة تجريبية وتفاصيل العرض',
    whatsappText: 'مرحباً، أرغب بتجربة PharmFlow والاستفادة من عرض الجمعة السوداء.',
    company: 'شركة جانا للتطوير البرمجي',
    companyLine: 'PharmFlow أحد منتجات شركة جانا للتطوير البرمجي',
    whatsappLabel: 'واتساب للتواصل وتجربة البرنامج',
  },
  en: {
    badge: 'Black Friday offer',
    title: '50% off PharmFlow',
    lead: 'The complete pharmacy management system — barcode sales, stock and expiry, your team, and cloud backup — at half price.',
    oldPrice: '$1200',
    newPrice: '$600',
    discount: '-50%',
    saveLabel: 'Save $600',
    cta: 'Try it on WhatsApp',
    ctaHint: 'Message us for a trial copy and the offer details',
    whatsappText: 'Hello, I would like to try PharmFlow with the Black Friday offer.',
    company: 'Jana Software Development',
    companyLine: 'PharmFlow is a product of Jana Software Development',
    whatsappLabel: 'WhatsApp for contact and a trial',
  },
};

export const whatsappLink = (base: string, text: string) => `${base}?text=${encodeURIComponent(text)}`;
