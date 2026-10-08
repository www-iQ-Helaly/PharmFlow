import type { IconName } from '../lib/icons';

export type Lang = 'ar' | 'en';

export interface LanguageMeta {
  label: string;
  htmlLang: string;
  dir: 'rtl' | 'ltr';
  ogLocale: string;
  localeDate: string;
}

export const languages: Record<Lang, LanguageMeta> = {
  ar: { label: 'العربية', htmlLang: 'ar', dir: 'rtl', ogLocale: 'ar_AR', localeDate: 'ar-EG' },
  en: { label: 'English', htmlLang: 'en', dir: 'ltr', ogLocale: 'en_US', localeDate: 'en-US' },
};

export interface NavItem {
  label: string;
  href: string;
}

export interface IconLink {
  href: string;
  icon: IconName;
  label: string;
}

export interface IconTitle {
  icon: IconName;
  title: string;
}

export interface GalleryTab {
  id: string;
  label: string;
  icon: IconName;
}

export interface FooterLink {
  label: string;
  href: string | null;
}

export interface ShowcaseItem {
  id: string;
  kicker: string;
  title: string;
  intro: string;
  bullets: string[];
  icon: IconName;
  flip?: boolean;
}

export type FeatureStatus = 'completed' | 'current' | 'planned' | 'roadmap' | 'unknown';

export interface Translations {
  meta: { title: string; description: string };
  layout: { skipToContent: string };
  header: {
    brandAria: string;
    navAria: string;
    langSwitcherLabel: string;
    download: string;
    openMenu: string;
    closeMenu: string;
    nav: NavItem[];
  };
  hero: {
    badge: string;
    title: string;
    intro: string;
    introNote: string;
    ctaPrimary: string;
    ctaSecondary: string;
    chips: IconLink[];
    windowTitle: string;
    screenshotLabel: string;
    screenshotNote: string;
  };
  productIntro: {
    kicker: string;
    title: string;
    lead: string;
    audiences: Array<IconTitle & { text: string }>;
  };
  features: {
    kicker: string;
    title: string;
    lead: string;
    itemNote: string;
    details: string;
    items: IconLink[];
  };
  howItWorks: {
    kicker: string;
    title: string;
    lead: string;
    stepLabel: (index: number) => string;
    stepNote: string;
    stepCount: number;
  };
  whatsNew: {
    kicker: string;
    title: string;
    lead: string;
    versionFallback: string;
    placeholderLabel: string;
    placeholderNote: string;
    fullPagePrefix: string;
    soon: string;
  };
  gallery: {
    kicker: string;
    title: string;
    lead: string;
    tablistAria: string;
    screenshot: (label: string) => string;
    tabs: GalleryTab[];
  };
  video: {
    kicker: string;
    title: string;
    lead: string;
    chaptersTitle: string;
    chapters: { id: string; label: string }[];
    featuresTitle: string;
    features: { icon: IconName; title: string; text: string; note?: string }[];
  };
  showcase: {
    bullet: string;
    screenshot: (title: string) => string;
    items: ShowcaseItem[];
  };
  explainer: {
    kicker: string;
    title: string;
    lead: string;
    tabOverview: string;
    tabPos: string;
    tabInventory: string;
    tabFefo: string;
    tabTechnology: string;
    tabWorkflow: string;
    overview: {
      title: string;
      subtitle: string;
      description: string;
      cardProducts: { title: string; content: string };
      cardBatches: { title: string; content: string };
      cardInvoices: { title: string; content: string };
      cardBranches: { title: string; content: string };
      securityNote: { title: string; content: string };
    };
    pos: {
      title: string;
      subtitle: string;
      description: string;
      scanning: { title: string; item1: string; item2: string; item3: string };
      cart: { title: string; item1: string; item2: string; item3: string; item4: string };
      engine: { title: string; item1: string; item2: string; item3: string };
      suspended: { title: string; content: string };
    };
    inventory: {
      title: string;
      subtitle: string;
      description: string;
      cardStock: { title: string; content: string };
      cardReconciliation: { title: string; content: string };
      exports: { title: string; formats: string[] };
    };
    fefo: {
      title: string;
      subtitle: string;
      description: string;
      principle: string;
      steps: { add: string; addDesc: string; allocate: string; allocateDesc: string; validate: string; validateDesc: string };
      alerts: {
        healthy: string;
        healthyDesc: string;
        warning: string;
        warningDesc: string;
        blocked: string;
        blockedDesc: string;
      };
      test: { title: string; content: string };
    };
    technology: {
      title: string;
      subtitle: string;
      description: string;
      cardDatabase: { title: string; content: string; techs: string[] };
      cardSecurity: { title: string; items: string[] };
      cardOffline: { title: string; content: string; techs: string[] };
      cardLanguages: { title: string; content: string };
    };
    workflow: {
      title: string;
      subtitle: string;
      description: string;
      steps: Array<{ title: string; description: string; details?: string[] }>;
      note: { title: string; content: string };
    };
    contentRequiredAria?: string;
  };
  technology: {
    kicker: string;
    title: string;
    lead: string;
    cards: Array<{ title: string; content: string; items: string[] }>;
  };
  cta: {
    title: string;
    lead: string;
    ctaPrimary: string;
    ctaSecondary: string;
    downloadTitle: string;
    downloadLead: string;
    androidLabel: string;
    androidHint: string;
    windowsLabel: string;
    windowsHint: string;
    sizeLabel: string;
    checksumLabel: string;
    email: string;
    phone: string;
  };
  footer: {
    brandAria: string;
    about: string;
    note: string;
    productTitle: string;
    resourcesTitle: string;
    supportTitle: string;
    productLinks: FooterLink[];
    resourceLinks: FooterLink[];
    supportLinks: FooterLink[];
    contactEmail: string;
    contactPhone: string;
    soon: string;
    copyright: string;
    tagline: string;
  };
  status: Record<FeatureStatus, string>;
  contentRequiredAria: string;
}

export const translations: Record<Lang, Translations> = {
  ar: {
    meta: {
      title: 'PharmFlow — نظام إدارة الصيدليات ونقاط البيع',
      description: 'الموقع الرسمي لمنتج PharmFlow لإدارة الصيدليات ونقاط البيع (POS).',
    },
    layout: { skipToContent: 'تخطَّ إلى المحتوى الرئيسي' },
    header: {
      brandAria: 'PharmFlow — الصفحة الرئيسية',
      navAria: 'التنقل الرئيسي',
      langSwitcherLabel: 'اختر اللغة',
      download: 'تحميل',
      openMenu: 'فتح القائمة',
      closeMenu: 'إغلاق القائمة',
      nav: [
        { label: 'المنتج', href: '#intro' },
        { label: 'المميزات', href: '#pos' },
        { label: 'طريقة العمل', href: '#explainer' },
        { label: 'الجديد', href: '#whats-new' },
        { label: 'المعرض', href: '#gallery' },
        { label: 'التقنية', href: '#technology' },
        { label: 'الشروحات والدليل', href: '/docs/' },
        { label: 'العرض التجاري', href: '/slides/' },
      ],
    },
    hero: {
      badge: 'يعمل بلا إنترنت · Android و Windows',
      title: 'نظام إدارة الصيدليات ونقاط البيع',
      intro: 'بيع بالباركود، ومخزون بدقة الدفعة، وتنبيهات صلاحية تلقائية، في برنامج واحد يواصل العمل حتى عند انقطاع الإنترنت.',
      introNote: 'الإصدار الحالي ‪0.6.0+7‬.',
      ctaPrimary: 'تعرّف على PharmFlow',
      ctaSecondary: 'شاهد البرنامج',
      chips: [
        { href: '#offline', icon: 'wifi-off', label: 'العمل دون اتصال' },
        { href: '#pos', icon: 'receipt', label: 'نقاط البيع' },
        { href: '#security', icon: 'lock', label: 'الأمان والصلاحيات' },
      ],
      windowTitle: 'PharmFlow',
      screenshotLabel: 'لقطة حقيقية',
      screenshotNote: 'لقطات حقيقية من التطبيق (الإصدار ‪0.6.0+7‬).',
    },
    productIntro: {
      kicker: 'مقدمة المنتج',
      title: 'ما هو PharmFlow؟',
      lead: 'برنامج لإدارة الصيدلية اليومية: بيع سريع، ومخزون مفصّل على مستوى الدفعة، ومنع تلقائي لبيع الدواء المنتهي. يحفظ بياناته مشفّرة على جهازك، ويزامنها اختيارياً بين أجهزة الفرع.',
      audiences: [
        { icon: 'users', title: 'أصحاب الصيدليات', text: 'تقرير يومي مجدول يصلك عبر البريد أو تيليجرام، وأرشيف فواتير كامل، وإدارة للفريق والأجهزة والصلاحيات، وترخيص مرتبط بالفرع.' },
        { icon: 'user', title: 'الصيادلة', text: 'مخزون بدقة الدفعة وتاريخ الانتهاء، وتنبيهات قرب الانتهاء ونقص الكمية، وإدخال بضاعة جديدة بالجملة من ملف أو صورة فاتورة، ومعالجة الإرجاع.' },
        { icon: 'users', title: 'فريق الصيدلية', text: 'شاشة بيع واحدة: امسح الباركود، راجع السلة، اختر طريقة الدفع، وأتمّ البيع ثم اطبع الإيصال بأقل عدد من الخطوات.' },
      ],
    },
    features: {
      kicker: 'المميزات',
      title: 'ماذا يقدم PharmFlow؟',
      lead: 'ست قدرات أساسية في برنامج واحد: البيع، والمخزون، والباركود، والفواتير، والأمان، والعمل دون اتصال.',
      itemNote: 'التفاصيل في الأقسام التالية.',
      details: 'التفاصيل',
      items: [
        { href: '#pos', icon: 'receipt', label: 'نقاط البيع والمبيعات' },
        { href: '#inventory', icon: 'package', label: 'إدارة المخزون' },
        { href: '#barcode', icon: 'scanner', label: 'قراءة الباركود و QR' },
        { href: '#transactions', icon: 'activity', label: 'الفواتير والإرجاع' },
        { href: '#security', icon: 'lock', label: 'الأمان والصلاحيات' },
        { href: '#offline', icon: 'wifi-off', label: 'العمل دون اتصال' },
        { href: '#technology', icon: 'cpu', label: 'بنية تقنية حديثة' },
      ],
    },
    howItWorks: {
      kicker: 'طريقة العمل',
      title: 'كيف يعمل PharmFlow؟',
      lead: 'خطوات تشغيل البرنامج من التثبيت إلى العمل اليومي: التسجيل، إضافة المنتجات، مسح الباركود، وإتمام الفاتورة.',
      stepLabel: (index) => 'الخطوة ' + ['الأولى', 'الثانية', 'الثالثة', 'الرابعة'][index],
      stepNote: 'خطوة من مسار العمل الفعلي داخل التطبيق.',
      stepCount: 4,
    },
    whatsNew: {
      kicker: 'ما الجديد',
      title: 'آخر التحديثات والإصدارات',
      lead: 'أبرز ما أُضيف إلى PharmFlow في الإصدارات الأخيرة.',
      versionFallback: 'تحديث',
      placeholderLabel: 'سجل الإصدارات',
      placeholderNote: 'سيظهر سجل الإصدارات هنا.',
      fullPagePrefix: '',
      soon: '',
    },
    gallery: {
      kicker: 'المعرض',
      title: 'لمحات من البرنامج',
      lead: 'لقطات حقيقية من البرنامج أثناء العمل.',
      tablistAria: 'أقسام المعرض',
      screenshot: (label) => label,
      tabs: [
        { id: 'g-pos', label: 'نقاط البيع', icon: 'receipt' },
        { id: 'g-inv', label: 'المخزون', icon: 'package' },
        { id: 'g-barcode', label: 'الباركود و QR', icon: 'scanner' },
        { id: 'g-trans', label: 'الفواتير', icon: 'activity' },
        { id: 'g-sec', label: 'الأمان', icon: 'lock' },
      ],
    },
    video: {
      kicker: 'فيديو تعريفي',
      title: 'شاهد PharmFlow أثناء العمل',
      lead: 'جولة مسجَّلة من التطبيق نفسه: بيع بالباركود، إدخال ذكي من ملف، توليد ملصقات الباركود، وغيرها.',
      chaptersTitle: 'فصول الفيديو',
      chapters: [
        { id: 'ch1', label: 'البيع السريع بالباركود' },
        { id: 'ch2', label: 'الإدخال الذكي: استيراد ملف' },
        { id: 'ch3', label: 'الإدخال الذكي بالذكاء الاصطناعي' },
        { id: 'ch4', label: 'توليد الباركود والملصقات' },
        { id: 'extra', label: 'وأكثر: كوديا وتصوير العلبة' },
      ],
      featuresTitle: 'ميزات الإدخال الذكي',
      features: [
        {
          icon: 'scanner',
          title: 'قراءة ملصقات كوديا',
          text: 'امسح رمز QR المطبوع على عبوة الدواء العراقية فتُعبَّأ بياناته تلقائياً: الاسم التجاري والعلمي والشكل الدوائي ورقم الدفعة وتاريخ الانتهاء، مع تنبيه عند ظهور دواء موقوف.',
          note: 'يحتاج اتصالاً بالإنترنت، واختياري: لا يمنع الإدخال اليدوي.',
        },
        {
          icon: 'cpu',
          title: 'تصوير العلبة بالذكاء الاصطناعي',
          text: 'صوّر العلبة فيستخرج الذكاء الاصطناعي اسم المنتج والشركة المصنِّعة، وكذلك الاسم العلمي والتركيز إن كانا مطبوعين. يترك الحقل فارغاً بدل التخمين، وتُعلَّم الحقول المعبّأة لتراجعها.',
          note: 'يحتاج اتصالاً ومفتاح Gemini.',
        },
        {
          icon: 'package',
          title: 'الإدخال الذكي بالجملة',
          text: 'أرفق فاتورة المورّد صورةً أو PDF فتتحول إلى صفوف تراجعها قبل الاعتماد، أو استورد ملف Excel/CSV مباشرة بلا ذكاء اصطناعي مع ربط تلقائي للأعمدة. يُصنَّف كل صف: منتج جديد أو إعادة تخزين.',
        },
        {
          icon: 'receipt',
          title: 'توليد الباركود بذكاء',
          text: 'للمنتج بلا باركود يولّد التطبيق كوداً محلياً صالحاً بضغطة واحدة، ويُنتج ملصقات جاهزة للطباعة بملف PDF، وتُعبَّأ من آخر دفعة إدخال تلقائياً. ولا يُنشئ ملصقاً لمنتج يحمل باركوداً حقيقياً.',
        },
      ],
    },
    showcase: {
      bullet: '',
      screenshot: (title) => title,
      items: [
        {
          id: 'offline',
          kicker: 'ميزة',
          title: 'العمل دون اتصال',
          icon: 'wifi-off',
          intro: 'كل ما يحتاجه الكاشير والصيدلاني يعمل من الجهاز نفسه، فلا يتوقف العمل عند انقطاع الإنترنت.',
          bullets: [
            'البيع والمخزون والفواتير وتنبيهات الصلاحية تعمل دون أي اتصال.',
            'مزامنة اختيارية مع السحابة عند توفر الإنترنت لربط أجهزة الفرع الواحد.',
            'ما ينتظر الإرسال يُحفظ في طابور ويُعاد إرساله تلقائياً عند عودة الاتصال.',
          ],
        },
        {
          id: 'pos',
          kicker: 'نقاط البيع',
          title: 'نقاط البيع والمبيعات',
          icon: 'receipt',
          flip: true,
          intro: 'شاشة بيع واحدة بأقل خطوات: امسح أو ابحث، راجع السلة، اختر طريقة الدفع وأتمّ البيع.',
          bullets: [
            'مسح بالكاميرا، أو إدخال الباركود يدوياً، أو البحث بالاسم.',
            'سلة متعددة الأصناف، وخصم يدوي، ودفع نقداً أو بطاقة أو آجل، مع تعديل سعر السطر للصيدلاني والمدير فقط.',
            'تعليق السلة واستئنافها لاحقاً، وإيصال PDF بمقاس A4 أو حراري 80 أو 58 مم.',
          ],
        },
        {
          id: 'inventory',
          kicker: 'المخزون',
          title: 'إدارة المخزون',
          icon: 'package',
          intro: 'مخزون مفصّل على مستوى الدفعة: لكل دفعة رقمها وتاريخ انتهائها وكميتها، وحالة ملوّنة لكل منتج.',
          bullets: [
            'أربعة تبويبات: الكل، والمنخفض، وقريب الانتهاء، والمنتهي، مع بحث فوري.',
            'إدخال بضاعة بالجملة من ملف Excel/CSV أو من صورة فاتورة المورّد، مع مراجعة قبل الاعتماد.',
            'سجل لتغييرات الأسعار، وتقرير مطابقة يقارن مخزون أجهزة الفرع.',
          ],
        },
        {
          id: 'barcode',
          kicker: 'الباركود و QR',
          title: 'قراءة الباركود و QR',
          icon: 'scanner',
          flip: true,
          intro: 'الكاميرا هي الماسح الضوئي، فلا حاجة لجهاز مسح منفصل.',
          bullets: [
            'يقرأ ‪QR · DataMatrix · EAN-13 · EAN-8 · Code 128 · Code 39 · UPC-A‬.',
            'قراءة ملصقات كوديا العراقية لتعبئة بيانات الدواء تلقائياً (اختياري ويحتاج اتصالاً).',
            'توليد كود محلي للمنتج الذي بلا باركود، وطباعة ملصقاته على ورقة L7160 بملف PDF.',
          ],
        },
        {
          id: 'transactions',
          kicker: 'الفواتير',
          title: 'الفواتير والإرجاع',
          icon: 'activity',
          intro: 'كل بيع يُحفظ فاتورة مرقّمة لا تتغير، والإرجاع عملية منفصلة مرتبطة بها.',
          bullets: [
            'فواتير مرقّمة بأصنافها وطريقة الدفع، مع أرشيف للمدير.',
            'إرجاع كامل أو جزئي يعيد الكمية إلى دفعتها الأصلية دون تعديل الفاتورة الأصلية.',
            'تقرير يومي مجدول يصل عبر البريد الإلكتروني أو تيليجرام.',
          ],
        },
        {
          id: 'security',
          kicker: 'الأمان',
          title: 'الأمان والصلاحيات',
          icon: 'lock',
          flip: true,
          intro: 'بيانات الصيدلية مشفّرة على الجهاز، والصلاحيات موزّعة حسب الدور.',
          bullets: [
            'قاعدة البيانات مشفّرة بـ SQLCipher، ورمز PIN محفوظ بتجزئة Argon2id.',
            'ثلاثة أدوار: كاشير وصيدلاني ومدير، ويرى كل دور الأزرار المسموحة له فقط.',
            'ترخيص موقّع رقمياً (Ed25519) مرتبط بالفرع، وإدارة للأجهزة المسجلة.',
          ],
        },
      ],
    },
    technology: {
      kicker: 'التقنية',
      title: 'التقنيات المستخدمة في PharmFlow',
      lead: 'ما وراء البرنامج: قاعدة بيانات محلية مشفّرة، وأمان على مستوى الدخول والترخيص، وعمل دون اتصال، وواجهة عربية وإنجليزية.',
      cards: [
        {
          title: 'قاعدة بيانات محلية مشفّرة',
          content: 'تُحفظ المبيعات والمخزون والفواتير في قاعدة SQLite على الجهاز بتشفير SQLCipher، وتُؤخذ نسخة احتياطية تلقائية قبل كل ترقية للتطبيق.',
          items: ['SQLCipher', 'Drift', 'SQLite', 'نسخ احتياطي قبل الترقية'],
        },
        {
          title: 'أمان من الأساس',
          content: 'رمز PIN بتجزئة Argon2id، وترخيص موقّع بـ Ed25519 مرتبط بالفرع، والأسرار محفوظة في التخزين الآمن للنظام.',
          items: ['Argon2id', 'Ed25519', 'تخزين آمن', 'كاشير · صيدلاني · مدير'],
        },
        {
          title: 'يعمل دون اتصال',
          content: 'كل العمليات تعمل محلياً، وتُزامَن مع السحابة (Supabase) اختيارياً عبر طابور إرسال يعيد المحاولة تلقائياً.',
          items: ['Offline-First', 'Supabase', 'طابور إرسال', 'إعادة محاولة تلقائية'],
        },
        {
          title: 'عربي وإنجليزي',
          content: 'واجهة بالعربية والإنجليزية مع اتجاه RTL كامل، تعمل على Android و Windows.',
          items: ['RTL', 'العربية', 'English', 'Android · Windows'],
        },
      ],
    },
    cta: {
      title: 'جاهز لاستكشاف PharmFlow؟',
      lead: 'تعرّف على المنتج، أو شاهد البرنامج أثناء العمل، أو تواصل مع فريق PharmFlow.',
      ctaPrimary: 'تعرّف على PharmFlow',
      ctaSecondary: 'شاهد البرنامج',
      downloadTitle: 'تحميل البرنامج',
      downloadLead: 'الإصدار ‪0.6.0‬: نسخة Android ونسخة Windows.',
      androidLabel: 'تحميل لنظام Android',
      androidHint: 'ملف APK. بعد التنزيل اسمح للمتصفح بتثبيت التطبيقات من هذا المصدر عند طلب النظام ذلك.',
      windowsLabel: 'تحميل لنظام Windows',
      windowsHint: 'مثبّت لنظام Windows 10 أو أحدث بمعمارية 64 بت.',
      sizeLabel: 'الحجم',
      checksumLabel: 'بصمة SHA-256',
      email: 'البريد الإلكتروني',
      phone: 'الهاتف',
    },
    footer: {
      brandAria: 'PharmFlow — الصفحة الرئيسية',
      about: 'PharmFlow: نظام إدارة الصيدليات ونقاط البيع.',
      note: 'معلومات هذا الموقع مأخوذة من التطبيق نفسه.',

      productTitle: 'المنتج',
      resourcesTitle: 'الموارد',
      supportTitle: 'الدعم والتواصل',
      productLinks: [
        { label: 'ما هو PharmFlow', href: '#intro' },
        { label: 'المميزات', href: '#pos' },
        { label: 'طريقة العمل', href: '#explainer' },
        { label: 'التقنية', href: '#technology' },
      ],
      resourceLinks: [
        { label: 'دليل المستخدم', href: '/docs/' },
        { label: 'الإصدارات والجديد', href: '#whats-new' },
        { label: 'عرض تقديمي', href: '/slides/' },
      ],
      supportLinks: [
        { label: 'تواصل معنا', href: '#cta' },
      ],
      contactEmail: 'البريد الإلكتروني',
      contactPhone: 'الهاتف',
      soon: 'قريبًا',
      copyright: '© 2026 PharmFlow. جميع الحقوق محفوظة.',
      tagline: 'نظام إدارة الصيدليات ونقاط البيع',
    },
    status: {
      completed: 'مكتمل',
      current: 'متاح حاليًا',
      planned: 'قيد التخطيط',
      roadmap: 'مقترح',
      unknown: 'قيد التأكيد',
    },
    contentRequiredAria: 'محتوى بانتظار التأكيد',
    explainer: {
      kicker: 'تعرّف على المنتج',
      title: 'كيف يعمل PharmFlow بالضبط؟',
      lead: 'استكشف النظام من البيع والمسح إلى المخزون وانتهاء الصلاحية، وما وراءه من تقنية.',
      tabOverview: 'نظرة عامة',
      tabPos: 'نقطة البيع',
      tabInventory: 'المخزون',
      tabFefo: 'انتهاء الصلاحية',
      tabTechnology: 'التقنية',
      tabWorkflow: 'خطوات العمل',
      overview: {
        title: 'نظرة عامة على النظام',
        subtitle: 'ما الذي يديره PharmFlow',
        description: 'PharmFlow برنامج صيدلية يعمل دون إنترنت على Android و Windows (الإصدار ‪0.6.0+7‬). يحفظ بياناته في قاعدة مشفّرة على الجهاز، وينظّم البيع والمخزون وانتهاء الصلاحية والتقارير.',
        cardProducts: { title: 'المنتجات', content: 'الاسم والوحدة والباركود وسعر التجزئة، بإدخال يدوي أو جماعي.' },
        cardBatches: { title: 'الدفعات', content: 'لكل دفعة رقم وتاريخ انتهاء وكمية، فيُتتبَّع المخزون بدقة الدفعة.' },
        cardInvoices: { title: 'الفواتير', content: 'كل بيع يُحفظ فاتورة مرقّمة بأصنافها وطريقة الدفع.' },
        cardBranches: { title: 'الفرع والفريق', content: 'ربط أجهزة الفرع الواحد بمزامنة اختيارية، مع إدارة الفريق والأجهزة.' },
        securityNote: { title: 'الأمان من الأساس', content: 'قاعدة البيانات مشفّرة بـ SQLCipher، ورمز PIN محفوظ بتجزئة Argon2id، والترخيص موقّع بـ Ed25519.' },
      },
      pos: {
        title: 'نقطة البيع',
        subtitle: 'كيف تتم عملية البيع',
        description: 'من شاشة واحدة: امسح الباركود بالكاميرا أو أدخله يدوياً أو ابحث بالاسم، وراجع السلة، ثم أتمّ البيع. إن لم يكن الباركود معروفاً يظهر زر "أضف هذا المنتج".',
        scanning: {
          title: 'المسح والبحث',
          item1: 'كاميرا الجهاز هي الماسح، بلا حاجة لجهاز منفصل.',
          item2: 'يقرأ ‪QR · DataMatrix · EAN-13 · EAN-8 · Code 128 · Code 39 · UPC-A‬.',
          item3: 'إدخال الباركود يدوياً والبحث بالاسم متاحان كبديل.',
        },
        cart: {
          title: 'سلة البيع',
          item1: 'أصناف متعددة بكميات تزيدها أو تنقصها بزر.',
          item2: 'تنبيه فوري إذا اقتربت الدفعة المختارة من الانتهاء.',
          item3: 'خصم يدوي على الفاتورة، وتعديل سعر السطر للصيدلاني والمدير فقط.',
          item4: 'دفع نقداً أو بطاقة أو آجل، ثم إيصال PDF.',
        },
        engine: {
          title: 'ما يحدث تلقائياً',
          item1: 'اختيار الدفعة الأقرب انتهاءً (FEFO) عند كل إضافة.',
          item2: 'منع بيع الدفعات المنتهية.',
          item3: 'خصم الكمية من الدفعة نفسها وتسجيل حركة المخزون.',
        },
        suspended: {
          title: 'تعليق السلة',
          content: 'علّق السلة لخدمة زبون آخر ثم استأنفها لاحقاً من قائمة السلات المعلّقة، وتبقى محفوظة على الجهاز.',
        },
      },
      inventory: {
        title: 'المخزون',
        subtitle: 'تحكّم بالكميات والدفعات',
        description: 'شاشة حالة المخزون تعرض كل منتج بكميته وحالته الملوّنة في أربعة تبويبات: الكل، والمنخفض، وقريب الانتهاء، والمنتهي.',
        cardStock: { title: 'حالة المخزون', content: 'بحث فوري بالاسم، وتفاصيل المنتج وسعره وسجل تغييرات السعر.' },
        cardReconciliation: { title: 'مطابقة المخزون', content: 'تقرير يقارن مخزون الأجهزة المرتبطة ويكشف أي فرق بينها.' },
        exports: { title: 'الإدخال والطباعة', formats: ['استيراد Excel / CSV', 'فاتورة المورّد (صورة / PDF)', 'ملصقات الباركود PDF', 'إيصال PDF'] },
      },
      fefo: {
        title: 'انتهاء الصلاحية (FEFO)',
        subtitle: 'الأقرب انتهاءً يُباع أولاً',
        description: 'عند إضافة منتج إلى السلة يختار النظام تلقائياً الدفعة الأقرب انتهاءً، فتُباع الدفعات الأقدم أولاً ولا يُباع دواء منتهٍ.',
        principle: 'FEFO: First Expired, First Out، أي أن الأقرب انتهاءً يخرج أولاً.',
        steps: {
          add: 'إضافة دفعة',
          addDesc: 'رقم الدفعة وتاريخ الانتهاء والكمية',
          allocate: 'اختيار تلقائي',
          allocateDesc: 'تُختار الدفعة الأقرب انتهاءً',
          validate: 'فحص الصلاحية',
          validateDesc: 'تحذير عند القرب، ومنع عند الانتهاء',
        },
        alerts: {
          healthy: 'سليمة (أكثر من 90 يوماً)',
          healthyDesc: 'لا تنبيه',
          warning: 'قريبة الانتهاء (حتى 90 يوماً)',
          warningDesc: 'تنبيه متدرج: أصفر حتى 90 يوماً، وبرتقالي حتى 60، وأحمر حتى 30',
          blocked: 'منتهية',
          blockedDesc: 'محظورة من البيع',
        },
        test: {
          title: 'مغطّى باختبارات آلية',
          content: 'منطق اختيار الدفعة مغطّى باختبارات آلية تتأكد أن الدفعة الأقرب انتهاءً تُختار دائماً عند تعدد الدفعات.',
        },
      },
      technology: {
        title: 'البنية التقنية',
        subtitle: 'ما الذي يجعل النظام موثوقاً',
        description: 'مبني بـ Flutter مع قاعدة SQLite محلية مشفّرة بـ SQLCipher. كل العمليات تعمل دون إنترنت، مع مزامنة اختيارية بالسحابة.',
        cardDatabase: {
          title: 'قاعدة البيانات',
          content: 'SQLite محلية مشفّرة، مع نسخة احتياطية تلقائية قبل كل ترقية.',
          techs: ['Drift', 'SQLite', 'SQLCipher'],
        },
        cardSecurity: {
          title: 'الأمان',
          items: [
            'SQLCipher: تشفير قاعدة البيانات المحلية',
            'Argon2id: تجزئة رمز PIN',
            'Ed25519: توقيع الترخيص',
            'تخزين آمن للأسرار على الجهاز',
            'أدوار: كاشير وصيدلاني ومدير',
          ],
        },
        cardOffline: {
          title: 'العمل دون اتصال',
          content: 'يعمل بالكامل بلا إنترنت، وتُرسل التغييرات إلى السحابة عند عودة الاتصال عبر طابور يعيد المحاولة تلقائياً.',
          techs: ['Offline-First', 'Supabase', 'طابور إرسال'],
        },
        cardLanguages: {
          title: 'عربي وإنجليزي',
          content: 'واجهة عربية وإنجليزية باتجاه RTL كامل.',
        },
      },
      workflow: {
        title: 'خطوات عملية البيع',
        subtitle: 'من المسح إلى الإيصال',
        description: 'مسار البيع الفعلي داخل التطبيق خطوة بخطوة.',
        steps: [
          {
            title: 'المسح أو البحث',
            description: 'أضف الصنف بمسح الباركود، أو إدخاله يدوياً، أو البحث بالاسم.',
            details: [
              'الكاميرا تقرأ الباركود فوراً دون ضغط زر',
              'للمنتج غير المعروف يظهر زر "أضف هذا المنتج"',
              'إضافة منتج جديد متاحة للصيدلاني والمدير',
            ],
          },
          {
            title: 'اختيار الدفعة (FEFO)',
            description: 'يختار النظام الدفعة الأقرب انتهاءً تلقائياً.',
            details: [
              'دون إدخال يدوي',
              'تحذير ملوّن إذا اقترب الانتهاء',
              'لا تُباع الدفعات المنتهية',
            ],
          },
          {
            title: 'مراجعة السلة',
            description: 'عدّل الكمية أو احذف سطراً، وأضف خصماً يدوياً عند الحاجة.',
            details: [
              'زيادة الكمية أو إنقاصها بزر',
              'حذف السطر يطلب تأكيداً كي لا يُمحى بالخطأ',
              'تعديل السعر للصيدلاني والمدير فقط',
            ],
          },
          {
            title: 'الدفع والإتمام',
            description: 'اختر نقداً أو بطاقة أو آجل ثم أتمّ البيع.',
            details: [
              'تُحفظ فاتورة مرقّمة بأصنافها',
              'تُخصم الكمية من الدفعة المختارة',
              'اطبع الإيصال أو شاركه بملف PDF',
            ],
          },
        ],
        note: {
          title: 'ملاحظة',
          content: 'الإرجاع عملية منفصلة لا تعدّل الفاتورة الأصلية، وتعيد الكمية إلى دفعتها الأصلية.',
        },
      },
      contentRequiredAria: 'محتوى بانتظار التأكيد',
    },
  },
  en: {
    meta: {
      title: 'PharmFlow — Pharmacy Management & POS System',
      description: 'The official website of the PharmFlow product for pharmacy management and point-of-sale (POS).',
    },
    layout: { skipToContent: 'Skip to main content' },
    header: {
      brandAria: 'PharmFlow — Home',
      navAria: 'Main navigation',
      langSwitcherLabel: 'Select language',
      download: 'Download',
      openMenu: 'Open menu',
      closeMenu: 'Close menu',
      nav: [
        { label: 'Product', href: '#intro' },
        { label: 'Features', href: '#pos' },
        { label: 'How it works', href: '#explainer' },
        { label: "What's new", href: '#whats-new' },
        { label: 'Gallery', href: '#gallery' },
        { label: 'Technology', href: '#technology' },
        { label: 'Documentation (Arabic)', href: '/docs/' },
        { label: 'Business Deck', href: '/slides/' },
      ],
    },
    hero: {
      badge: 'Works offline · Android and Windows',
      title: 'Pharmacy Management & Point-of-Sale System',
      intro: 'Barcode sales, batch-level stock and automatic expiry alerts in one program that keeps working even when the internet is down.',
      introNote: 'Current version 0.6.0+7.',
      ctaPrimary: 'Discover PharmFlow',
      ctaSecondary: 'Watch the software',
      chips: [
        { href: '#offline', icon: 'wifi-off', label: 'Offline mode' },
        { href: '#pos', icon: 'receipt', label: 'Point of sale' },
        { href: '#security', icon: 'lock', label: 'Security & permissions' },
      ],
      windowTitle: 'PharmFlow',
      screenshotLabel: 'Real screenshot',
      screenshotNote: 'Real screenshots from the app (version 0.6.0+7).',
    },
    productIntro: {
      kicker: 'Product introduction',
      title: 'What is PharmFlow?',
      lead: 'A program for running the pharmacy day to day: fast sales, batch-level stock and automatic blocking of expired medicine. It keeps its data encrypted on your device and can optionally sync it between the devices of a branch.',
      audiences: [
        { icon: 'users', title: 'Pharmacy owners', text: 'A scheduled daily report by email or Telegram, a full invoice archive, management of the team, devices and permissions, and a license tied to the branch.' },
        { icon: 'user', title: 'Pharmacists', text: 'Stock by batch and expiry date, alerts for near-expiry and low quantity, bulk entry of new stock from a file or an invoice photo, and returns handling.' },
        { icon: 'users', title: 'Pharmacy staff', text: 'One sales screen: scan the barcode, review the cart, choose the payment method, complete the sale and print the receipt in as few steps as possible.' },
      ],
    },
    features: {
      kicker: 'Features',
      title: 'What does PharmFlow offer?',
      lead: 'Six core capabilities in one program: sales, stock, barcodes, invoices, security and offline work.',
      itemNote: 'Details in the sections below.',
      details: 'Details',
      items: [
        { href: '#pos', icon: 'receipt', label: 'Point of sale & sales' },
        { href: '#inventory', icon: 'package', label: 'Inventory management' },
        { href: '#barcode', icon: 'scanner', label: 'Barcode & QR reading' },
        { href: '#transactions', icon: 'activity', label: 'Invoices & returns' },
        { href: '#security', icon: 'lock', label: 'Security & permissions' },
        { href: '#offline', icon: 'wifi-off', label: 'Offline mode' },
        { href: '#technology', icon: 'cpu', label: 'Modern technical architecture' },
      ],
    },
    howItWorks: {
      kicker: 'How it works',
      title: 'How does PharmFlow work?',
      lead: 'From installation to daily work: sign-in, adding products, scanning barcodes and completing the invoice.',
      stepLabel: (index) => 'Step ' + ['One', 'Two', 'Three', 'Four'][index],
      stepNote: 'A step from the real workflow inside the app.',
      stepCount: 4,
    },
    whatsNew: {
      kicker: "What's new",
      title: 'Latest updates & releases',
      lead: 'The most notable additions to PharmFlow in recent releases.',
      versionFallback: 'Update',
      placeholderLabel: 'Release log',
      placeholderNote: 'The release log will appear here.',
      fullPagePrefix: '',
      soon: '',
    },
    gallery: {
      kicker: 'Gallery',
      title: 'Product previews',
      lead: 'Real screenshots of the software at work.',
      tablistAria: 'Gallery sections',
      screenshot: (label) => label,
      tabs: [
        { id: 'g-pos', label: 'Point of sale', icon: 'receipt' },
        { id: 'g-inv', label: 'Inventory', icon: 'package' },
        { id: 'g-barcode', label: 'Barcode & QR', icon: 'scanner' },
        { id: 'g-trans', label: 'Invoices', icon: 'activity' },
        { id: 'g-sec', label: 'Security', icon: 'lock' },
      ],
    },
    video: {
      kicker: 'Intro video',
      title: 'Watch PharmFlow in action',
      lead: 'A recorded tour of the app itself: barcode sales, smart file import, barcode label generation and more.',
      chaptersTitle: 'Video chapters',
      chapters: [
        { id: 'ch1', label: 'Fast barcode sale' },
        { id: 'ch2', label: 'Smart entry: file import' },
        { id: 'ch3', label: 'Smart entry with AI' },
        { id: 'ch4', label: 'Barcode and label generation' },
        { id: 'extra', label: 'And more: Gudea and box photo' },
      ],
      featuresTitle: 'Smart entry features',
      features: [
        {
          icon: 'scanner',
          title: 'Gudea label reading',
          text: 'Scan the QR code printed on an Iraqi drug pack and its data is filled in automatically: trade and generic name, dosage form, batch number and expiry date, with a warning when a drug is blocked.',
          note: 'Needs an internet connection; optional, it never blocks manual entry.',
        },
        {
          icon: 'cpu',
          title: 'AI pack photo',
          text: 'Photograph the pack and AI extracts the product name and manufacturer, plus the generic name and strength when printed. It leaves a field empty rather than guessing, and marks filled fields for review.',
          note: 'Needs a connection and a Gemini key.',
        },
        {
          icon: 'package',
          title: 'Smart bulk entry',
          text: 'Attach a supplier invoice as an image or PDF and it becomes rows you review before committing, or import an Excel/CSV file directly with no AI and automatic column mapping. Each row is classed as a new product or a restock.',
        },
        {
          icon: 'receipt',
          title: 'Smart barcode generation',
          text: 'For a product without a barcode the app generates a valid local code in one tap, produces print-ready labels as a PDF, and fills them from the last bulk entry automatically. It never creates a label for a product that already has a real barcode.',
        },
      ],
    },
    showcase: {
      bullet: '',
      screenshot: (title) => title,
      items: [
        {
          id: 'offline',
          kicker: 'Feature',
          title: 'Offline mode',
          icon: 'wifi-off',
          intro: 'Everything a cashier and pharmacist need runs on the device itself, so work does not stop when the internet drops.',
          bullets: [
            'Sales, stock, invoices and expiry alerts work with no connection at all.',
            'Optional cloud sync when the internet is available, to link the devices of one branch.',
            'Whatever is waiting to be sent is queued and re-sent automatically when the connection returns.',
          ],
        },
        {
          id: 'pos',
          kicker: 'Point of sale',
          title: 'Point of sale & sales',
          icon: 'receipt',
          flip: true,
          intro: 'One sales screen with as few steps as possible: scan or search, review the cart, pick the payment method and complete the sale.',
          bullets: [
            'Scan with the camera, type the barcode, or search by name.',
            'Multi-item cart, manual discount, and cash, card or credit payment, with line-price editing for pharmacists and admins only.',
            'Hold a cart and resume it later, and a PDF receipt in A4 or 80 mm / 58 mm thermal size.',
          ],
        },
        {
          id: 'inventory',
          kicker: 'Inventory',
          title: 'Inventory management',
          icon: 'package',
          intro: 'Stock tracked per batch: each batch has its own number, expiry date and quantity, and every product shows a colored status.',
          bullets: [
            'Four tabs: all, low, near expiry and expired, with instant search.',
            'Bulk stock entry from an Excel/CSV file or a supplier invoice photo, reviewed before it is committed.',
            'A price-change log and a reconciliation report that compares stock across branch devices.',
          ],
        },
        {
          id: 'barcode',
          kicker: 'Barcode & QR',
          title: 'Barcode & QR reading',
          icon: 'scanner',
          flip: true,
          intro: 'The camera is the scanner, so no separate scanning device is needed.',
          bullets: [
            'Reads QR, DataMatrix, EAN-13, EAN-8, Code 128, Code 39 and UPC-A.',
            'Reads Iraqi Gudea labels to fill in drug details automatically (optional, needs a connection).',
            'Generates a local code for a product with no barcode and prints its labels on an L7160 sheet as a PDF.',
          ],
        },
        {
          id: 'transactions',
          kicker: 'Invoices',
          title: 'Invoices & returns',
          icon: 'activity',
          intro: 'Every sale is saved as a numbered invoice that does not change, and a return is a separate operation linked to it.',
          bullets: [
            'Numbered invoices with their items and payment method, with an archive for the admin.',
            'Full or partial returns put the quantity back into its original batch without editing the original invoice.',
            'A scheduled daily report delivered by email or Telegram.',
          ],
        },
        {
          id: 'security',
          kicker: 'Security',
          title: 'Security & permissions',
          icon: 'lock',
          flip: true,
          intro: 'Pharmacy data is encrypted on the device, and permissions are split by role.',
          bullets: [
            'The database is encrypted with SQLCipher, and the PIN is stored using an Argon2id hash.',
            'Three roles: cashier, pharmacist and admin, and each role sees only the buttons it is allowed to use.',
            'A digitally signed license (Ed25519) tied to the branch, and management of the registered devices.',
          ],
        },
      ],
    },
    technology: {
      kicker: 'Technology',
      title: 'Technologies behind PharmFlow',
      lead: 'Behind the program: an encrypted local database, security at sign-in and licensing, offline work, and an Arabic and English interface.',
      cards: [
        {
          title: 'Encrypted local database',
          content: 'Sales, stock and invoices are kept in a SQLite database on the device with SQLCipher encryption, and an automatic backup is taken before every app upgrade.',
          items: ['SQLCipher', 'Drift', 'SQLite', 'Backup before upgrade'],
        },
        {
          title: 'Secure by design',
          content: 'PIN hashed with Argon2id, a license signed with Ed25519 and tied to the branch, and secrets kept in the operating system secure storage.',
          items: ['Argon2id', 'Ed25519', 'Secure storage', 'Cashier · Pharmacist · Admin'],
        },
        {
          title: 'Works offline',
          content: 'Every operation runs locally and optionally syncs with the cloud (Supabase) through a send queue that retries automatically.',
          items: ['Offline-First', 'Supabase', 'Send queue', 'Automatic retry'],
        },
        {
          title: 'Arabic and English',
          content: 'An Arabic and English interface with full RTL layout, running on Android and Windows.',
          items: ['RTL', 'Arabic', 'English', 'Android · Windows'],
        },
      ],
    },
    cta: {
      title: 'Ready to explore PharmFlow?',
      lead: 'Get to know the product, watch the software at work, or contact the PharmFlow team.',
      ctaPrimary: 'Discover PharmFlow',
      ctaSecondary: 'Watch the software',
      downloadTitle: 'Download',
      downloadLead: 'Version 0.6.0: Android and Windows builds.',
      androidLabel: 'Download for Android',
      androidHint: 'An APK file. After downloading, allow your browser to install apps from this source when the system asks.',
      windowsLabel: 'Download for Windows',
      windowsHint: 'An installer for Windows 10 or later, 64-bit.',
      sizeLabel: 'Size',
      checksumLabel: 'SHA-256 checksum',
      email: 'Email',
      phone: 'Phone',
    },
    footer: {
      brandAria: 'PharmFlow — Home',
      about: 'PharmFlow: pharmacy management and point-of-sale system.',
      note: "This site's information is taken from the app itself.",

      productTitle: 'Product',
      resourcesTitle: 'Resources',
      supportTitle: 'Support & contact',
      productLinks: [
        { label: 'What is PharmFlow', href: '#intro' },
        { label: 'Features', href: '#pos' },
        { label: 'How it works', href: '#explainer' },
        { label: 'Technology', href: '#technology' },
      ],
      resourceLinks: [
        { label: 'User guide (Arabic)', href: '/docs/' },
        { label: 'Releases & news', href: '#whats-new' },
        { label: 'Business deck', href: '/slides/' },
      ],
      supportLinks: [
        { label: 'Contact us', href: '#cta' },
      ],
      contactEmail: 'Email',
      contactPhone: 'Phone',
      soon: 'Coming soon',
      copyright: '© 2026 PharmFlow. All rights reserved.',
      tagline: 'Pharmacy management and point-of-sale system',
    },
    status: {
      completed: 'Completed',
      current: 'Currently available',
      planned: 'Planned',
      roadmap: 'Proposed',
      unknown: 'Pending confirmation',
    },
    contentRequiredAria: 'Content pending confirmation',
    explainer: {
      kicker: 'Get to know the product',
      title: 'How exactly does PharmFlow work?',
      lead: 'Explore the system from sales and scanning to stock and expiry, and the technology behind it.',
      tabOverview: 'Overview',
      tabPos: 'Point of sale',
      tabInventory: 'Inventory',
      tabFefo: 'Expiry',
      tabTechnology: 'Technology',
      tabWorkflow: 'Workflow',
      overview: {
        title: 'System overview',
        subtitle: 'What PharmFlow manages',
        description: 'PharmFlow is an offline-first pharmacy program for Android and Windows (version 0.6.0+7). It keeps its data in an encrypted database on the device and organizes sales, stock, expiry and reports.',
        cardProducts: { title: 'Products', content: 'Name, unit, barcode and retail price, entered one by one or in bulk.' },
        cardBatches: { title: 'Batches', content: 'Each batch has a number, an expiry date and a quantity, so stock is tracked per batch.' },
        cardInvoices: { title: 'Invoices', content: 'Every sale is saved as a numbered invoice with its items and payment method.' },
        cardBranches: { title: 'Branch and team', content: 'Devices of one branch can be linked with optional sync, with team and device management.' },
        securityNote: { title: 'Secure by design', content: 'The database is encrypted with SQLCipher, the PIN is stored using an Argon2id hash, and the license is signed with Ed25519.' },
      },
      pos: {
        title: 'Point of sale',
        subtitle: 'How a sale happens',
        description: 'From one screen: scan the barcode with the camera, type it, or search by name, review the cart, then complete the sale. If the barcode is unknown an "Add this product" button appears.',
        scanning: {
          title: 'Scanning and search',
          item1: 'The device camera is the scanner, with no separate device needed.',
          item2: 'Reads QR, DataMatrix, EAN-13, EAN-8, Code 128, Code 39 and UPC-A.',
          item3: 'Typing the barcode and searching by name are available as alternatives.',
        },
        cart: {
          title: 'Sales cart',
          item1: 'Several items, with quantities you raise or lower with a button.',
          item2: 'An immediate warning if the selected batch is close to expiry.',
          item3: 'A manual invoice discount, and line-price editing for pharmacists and admins only.',
          item4: 'Cash, card or credit payment, then a PDF receipt.',
        },
        engine: {
          title: 'What happens automatically',
          item1: 'The batch nearest to expiry (FEFO) is chosen each time you add an item.',
          item2: 'Expired batches cannot be sold.',
          item3: 'The quantity is deducted from that same batch and a stock movement is recorded.',
        },
        suspended: {
          title: 'Hold the cart',
          content: 'Hold the cart to serve another customer and resume it later from the held-carts list; it stays saved on the device.',
        },
      },
      inventory: {
        title: 'Inventory',
        subtitle: 'Control quantities and batches',
        description: 'The stock status screen shows every product with its quantity and a colored status in four tabs: all, low, near expiry and expired.',
        cardStock: { title: 'Stock status', content: 'Instant search by name, plus product details, price and the price-change log.' },
        cardReconciliation: { title: 'Stock reconciliation', content: 'A report that compares the stock of linked devices and shows any difference between them.' },
        exports: { title: 'Entry and printing', formats: ['Excel / CSV import', 'Supplier invoice (image / PDF)', 'Barcode labels PDF', 'Receipt PDF'] },
      },
      fefo: {
        title: 'Expiry management (FEFO)',
        subtitle: 'Nearest expiry is sold first',
        description: 'When a product is added to the cart the system automatically picks the batch nearest to expiry, so older batches sell first and expired medicine is never sold.',
        principle: 'FEFO: First Expired, First Out, meaning the batch nearest to expiry leaves first.',
        steps: {
          add: 'Add a batch',
          addDesc: 'Batch number, expiry date and quantity',
          allocate: 'Automatic selection',
          allocateDesc: 'The batch nearest to expiry is picked',
          validate: 'Expiry check',
          validateDesc: 'A warning when close, a block when expired',
        },
        alerts: {
          healthy: 'Healthy (over 90 days)',
          healthyDesc: 'No alert',
          warning: 'Near expiry (up to 90 days)',
          warningDesc: 'Graded alert: yellow up to 90 days, orange up to 60, red up to 30',
          blocked: 'Expired',
          blockedDesc: 'Blocked from sale',
        },
        test: {
          title: 'Covered by automated tests',
          content: 'The batch-selection logic is covered by automated tests that confirm the batch nearest to expiry is always chosen when there are several batches.',
        },
      },
      technology: {
        title: 'Technical architecture',
        subtitle: 'What makes the system dependable',
        description: 'Built with Flutter on a local SQLite database encrypted with SQLCipher. Every operation works without internet, with optional cloud sync.',
        cardDatabase: {
          title: 'Database',
          content: 'An encrypted local SQLite database, with an automatic backup before every upgrade.',
          techs: ['Drift', 'SQLite', 'SQLCipher'],
        },
        cardSecurity: {
          title: 'Security',
          items: [
            'SQLCipher: encrypts the local database',
            'Argon2id: PIN hashing',
            'Ed25519: license signature',
            'Secure on-device storage for secrets',
            'Roles: cashier, pharmacist and admin',
          ],
        },
        cardOffline: {
          title: 'Offline mode',
          content: 'Works fully without internet, and changes are sent to the cloud when the connection returns through a queue that retries automatically.',
          techs: ['Offline-First', 'Supabase', 'Send queue'],
        },
        cardLanguages: {
          title: 'Arabic and English',
          content: 'An Arabic and English interface with full RTL layout.',
        },
      },
      workflow: {
        title: 'Steps of a sale',
        subtitle: 'From scan to receipt',
        description: 'The real sales flow inside the app, step by step.',
        steps: [
          {
            title: 'Scan or search',
            description: 'Add the item by scanning the barcode, typing it, or searching by name.',
            details: [
              'The camera reads the barcode instantly, with no button press',
              'For an unknown product an "Add this product" button appears',
              'Adding a new product is available to pharmacists and admins',
            ],
          },
          {
            title: 'Batch selection (FEFO)',
            description: 'The system automatically picks the batch nearest to expiry.',
            details: [
              'No manual entry',
              'A colored warning if expiry is close',
              'Expired batches cannot be sold',
            ],
          },
          {
            title: 'Review the cart',
            description: 'Change the quantity or remove a line, and add a manual discount if needed.',
            details: [
              'Raise or lower the quantity with a button',
              'Removing a line asks for confirmation so it is not erased by mistake',
              'Price editing for pharmacists and admins only',
            ],
          },
          {
            title: 'Pay and complete',
            description: 'Choose cash, card or credit, then complete the sale.',
            details: [
              'A numbered invoice with its items is saved',
              'The quantity is deducted from the selected batch',
              'Print the receipt or share it as a PDF',
            ],
          },
        ],
        note: {
          title: 'Note',
          content: 'A return is a separate operation that does not edit the original invoice and puts the quantity back into its original batch.',
        },
      },
      contentRequiredAria: 'Content pending confirmation',
    },
  },
};

export function getTranslations(lang: Lang): Translations {
  return translations[lang];
}