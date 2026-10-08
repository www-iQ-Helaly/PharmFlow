import type { Lang } from '../i18n/translations';
import type { IconName } from '../lib/icons';

// Copy for the "admin device + team devices" infographic (first explainer
// section). Every claim maps to a shipped app behaviour:
// - join code with a preset role, never the raw license (Milestones 90/92)
// - per-device sales breakdown from the cloud (Milestone 89)
// - revoke a device, staff directory, daily email/Telegram report (88/93/91)
// - offline-first outbox, sent automatically on reconnect (48/52)
// - cashier: sell only (no price change, no returns) — PermissionEngine
// - pharmacist: returns, restock, create products, can add a cashier
// - private per-pharmacy cloud space (RLS), shared product definitions
// - daily encrypted backup of the admin device (M-A2)

export type StaffId = 'pharmacist' | 'cashier' | 'desk';

export interface NodeDetail {
  title: string;
  body: string;
  items: string[];
}

export interface TeamNetworkCopy {
  kicker: string;
  title: string;
  lead: string;
  admin: {
    title: string;
    sub: string;
    licenseChip: string;
    salesLabel: string;
    invoicesLabel: string;
    onlineLabel: string;
    perDevice: string;
    feedTitle: string;
    feedEmpty: string;
  };
  hub: { title: string; sub: string };
  staff: { id: StaffId; kind: 'phone' | 'desktop'; role: string; name: string }[];
  status: { waiting: string; linked: string; offline: string; queued: string };
  packets: { join: string; sale: string; ret: string; stock: string };
  feed: { sale: string; ret: string; stock: string; from: string };
  products: { name: string; price: number }[];
  steps: { join: string; live: string; offline: string; back: string; still: string };
  controls: { pause: string; play: string; replay: string; demoNote: string; tapHint: string };
  details: Record<'admin' | 'hub' | StaffId, NodeDetail>;
  legend: { icon: IconName; title: string; text: string }[];
}

export const teamNetwork: Record<Lang, TeamNetworkCopy> = {
  ar: {
    kicker: 'صيدلية واحدة، فريق كامل',
    title: 'جهاز المدير يقود الصيدلية، وأجهزة الفريق تغذّيه بالبيانات',
    lead:
      'المدير يملك الترخيص ويضيف كل جهاز برمز انضمام ودور محدد. الصيدلاني والكاشير يبيعان على أجهزتهما — حتى بلا إنترنت — فتصل الفواتير والمرتجعات وحركات المخزون إلى سحابة صيدليتك الخاصة، ويراها المدير مقسّمة حسب كل جهاز.',
    admin: {
      title: 'جهاز المدير',
      sub: 'مالك الترخيص',
      licenseChip: 'الترخيص',
      salesLabel: 'مبيعات اليوم',
      invoicesLabel: 'فواتير',
      onlineLabel: 'أجهزة متصلة',
      perDevice: 'المبيعات حسب الجهاز',
      feedTitle: 'آخر ما وصل',
      feedEmpty: 'بانتظار ربط الأجهزة…',
    },
    hub: { title: 'سحابة صيدليتك', sub: 'خاصة ومعزولة عن أي صيدلية أخرى' },
    staff: [
      { id: 'pharmacist', kind: 'phone', role: 'صيدلاني', name: 'هاتف الصيدلاني' },
      { id: 'cashier', kind: 'phone', role: 'كاشير', name: 'هاتف الكاشير' },
      { id: 'desk', kind: 'desktop', role: 'كاشير', name: 'كاونتر Windows' },
    ],
    status: {
      waiting: 'بانتظار الربط',
      linked: 'متصل',
      offline: 'بلا إنترنت — يبيع ويحفظ',
      queued: 'بانتظار الإرسال',
    },
    packets: { join: 'رمز انضمام', sale: 'فاتورة', ret: 'مرتجع', stock: 'مخزون' },
    feed: { sale: 'فاتورة', ret: 'مرتجع', stock: 'استلام مخزون', from: 'من' },
    products: [
      { name: 'Augmentin 1g', price: 12000 },
      { name: 'Panadol Extra', price: 2500 },
      { name: 'Vitamin D3 1000IU', price: 7500 },
      { name: 'Brufen 400mg', price: 1500 },
      { name: 'Ventolin Inhaler', price: 6500 },
      { name: 'Amoxil 500mg', price: 5000 },
    ],
    steps: {
      join: 'المدير يُصدر رمز انضمام بدور «{role}» — يمسحه الجهاز فيرتبط بالصيدلية',
      live: 'كل عملية على أي جهاز تصل إلى سحابة الصيدلية، ثم تظهر في لوحة المدير',
      offline: 'انقطع الإنترنت عن كاونتر Windows — البيع لا يتوقف، والعمليات تُحفظ على الجهاز',
      back: 'عاد الاتصال — تُرسَل العمليات المؤجَّلة تلقائياً دون تدخل أحد',
      still: 'المدير يرى مبيعات كل جهاز من الفريق في لوحة واحدة',
    },
    controls: {
      pause: 'إيقاف مؤقت',
      play: 'تشغيل',
      replay: 'إعادة العرض',
      demoNote: 'عرض توضيحي بأرقام افتراضية',
      tapHint: 'اضغط أي جهاز لمعرفة دوره',
    },
    details: {
      admin: {
        title: 'جهاز المدير — مالك الترخيص',
        body: 'يحمل رمز الترخيص ويقود الصيدلية كلها.',
        items: [
          'يضيف الأجهزة برمز انضمام ويحدد دور كل جهاز',
          'يرى المبيعات مقسّمة حسب كل جهاز، ودليل الموظفين',
          'يوقف أي جهاز مفقود أو غير مرغوب',
          'تقرير يومي بالبريد أو تيليجرام، ونسخة احتياطية يومية مشفّرة',
        ],
      },
      hub: {
        title: 'سحابة صيدليتك',
        body: 'مساحة خاصة بصيدليتك وحدها: أجهزة أي صيدلية أخرى لا ترى بياناتك.',
        items: [
          'تجمع ما ترسله أجهزة الفريق',
          'تشارك تعريفات الأصناف بين أجهزة الصيدلية',
          'تحفظ النسخ الاحتياطية المشفّرة لجهاز المدير',
        ],
      },
      pharmacist: {
        title: 'هاتف الصيدلاني',
        body: 'يبيع ويدير المخزون ضمن صلاحياته.',
        items: [
          'يبيع ويُصدر المرتجعات',
          'يستلم المخزون ويضيف الأصناف',
          'يمكنه إضافة كاشير برمز انضمام',
          'يرسل: الفواتير، المرتجعات، حركات المخزون',
        ],
      },
      cashier: {
        title: 'هاتف الكاشير',
        body: 'شاشة بيع سريعة بصلاحية البيع فقط.',
        items: [
          'يمسح الباركود ويبيع',
          'لا يغيّر الأسعار ولا يُصدر مرتجعات',
          'يرسل: الفواتير وحركات المخزون الناتجة عنها',
        ],
      },
      desk: {
        title: 'كاونتر Windows',
        body: 'نفس البرنامج على حاسوب نقطة البيع.',
        items: [
          'نفس الصيدلية ونفس المزامنة',
          'يعمل بلا إنترنت ويُرسل عند عودة الاتصال',
          'مناسب لكاونتر البيع الثابت',
        ],
      },
    },
    legend: [
      {
        icon: 'key',
        title: 'ترخيص واحد عند المدير',
        text: 'رمز الترخيص يبقى على جهاز المدير. الموظف ينضم برمز مؤقت يحدد دوره، ولا يصله الترخيص أبداً.',
      },
      {
        icon: 'wifi-off',
        title: 'البيع لا يتوقف بلا إنترنت',
        text: 'كل جهاز يحفظ عملياته في قاعدة مشفّرة على الجهاز، ويرسلها تلقائياً عند عودة الاتصال.',
      },
      {
        icon: 'activity',
        title: 'المدير يرى كل جهاز',
        text: 'مبيعات كل جهاز على حدة، وإيقاف أي جهاز مفقود، وتقرير يومي بالبريد أو تيليجرام.',
      },
    ],
  },
  en: {
    kicker: 'One pharmacy, one whole team',
    title: 'The admin device runs the pharmacy, and the team devices feed it data',
    lead:
      'The admin holds the license and adds every device with a join code and a set role. Pharmacists and cashiers sell on their own devices — even offline — and invoices, returns and stock movements reach your pharmacy’s private cloud, where the admin sees them broken down by device.',
    admin: {
      title: 'Admin device',
      sub: 'License holder',
      licenseChip: 'License',
      salesLabel: 'Sales today',
      invoicesLabel: 'Invoices',
      onlineLabel: 'Devices online',
      perDevice: 'Sales by device',
      feedTitle: 'Latest received',
      feedEmpty: 'Waiting for devices to link…',
    },
    hub: { title: 'Your pharmacy cloud', sub: 'Private, isolated from every other pharmacy' },
    staff: [
      { id: 'pharmacist', kind: 'phone', role: 'Pharmacist', name: 'Pharmacist phone' },
      { id: 'cashier', kind: 'phone', role: 'Cashier', name: 'Cashier phone' },
      { id: 'desk', kind: 'desktop', role: 'Cashier', name: 'Windows counter' },
    ],
    status: {
      waiting: 'Waiting to link',
      linked: 'Online',
      offline: 'Offline — still selling',
      queued: 'waiting to send',
    },
    packets: { join: 'Join code', sale: 'Invoice', ret: 'Return', stock: 'Stock' },
    feed: { sale: 'Invoice', ret: 'Return', stock: 'Stock received', from: 'from' },
    products: [
      { name: 'Augmentin 1g', price: 12000 },
      { name: 'Panadol Extra', price: 2500 },
      { name: 'Vitamin D3 1000IU', price: 7500 },
      { name: 'Brufen 400mg', price: 1500 },
      { name: 'Ventolin Inhaler', price: 6500 },
      { name: 'Amoxil 500mg', price: 5000 },
    ],
    steps: {
      join: 'The admin issues a join code with the “{role}” role — the device scans it and links to the pharmacy',
      live: 'Every operation on any device reaches the pharmacy cloud, then shows up on the admin dashboard',
      offline: 'The Windows counter lost internet — selling never stops, and operations are kept on the device',
      back: 'Back online — queued operations are sent automatically, no one has to do anything',
      still: 'The admin sees every team device’s sales on one dashboard',
    },
    controls: {
      pause: 'Pause',
      play: 'Play',
      replay: 'Replay',
      demoNote: 'Illustrative demo with sample figures',
      tapHint: 'Tap any device to see its role',
    },
    details: {
      admin: {
        title: 'Admin device — license holder',
        body: 'Holds the license code and runs the whole pharmacy.',
        items: [
          'Adds devices with a join code and sets each one’s role',
          'Sees sales broken down by device, plus the staff directory',
          'Stops any lost or unwanted device',
          'Daily report by email or Telegram, and a daily encrypted backup',
        ],
      },
      hub: {
        title: 'Your pharmacy cloud',
        body: 'A space for your pharmacy alone: devices of any other pharmacy cannot see your data.',
        items: [
          'Collects what the team devices send',
          'Shares product definitions across the pharmacy’s devices',
          'Keeps the admin device’s encrypted backups',
        ],
      },
      pharmacist: {
        title: 'Pharmacist phone',
        body: 'Sells and manages stock within its permissions.',
        items: [
          'Sells and issues returns',
          'Receives stock and adds products',
          'Can add a cashier with a join code',
          'Sends: invoices, returns, stock movements',
        ],
      },
      cashier: {
        title: 'Cashier phone',
        body: 'A fast sales screen with selling rights only.',
        items: [
          'Scans barcodes and sells',
          'Cannot change prices or issue returns',
          'Sends: invoices and the stock movements they create',
        ],
      },
      desk: {
        title: 'Windows counter',
        body: 'The same app on the point-of-sale computer.',
        items: [
          'Same pharmacy, same sync',
          'Works offline and sends when the connection returns',
          'Suited to a fixed sales counter',
        ],
      },
    },
    legend: [
      {
        icon: 'key',
        title: 'One license, on the admin device',
        text: 'The license code stays on the admin device. Staff join with a temporary code that sets their role — the license never reaches them.',
      },
      {
        icon: 'wifi-off',
        title: 'Selling never stops offline',
        text: 'Every device keeps its operations in an encrypted on-device database and sends them automatically when back online.',
      },
      {
        icon: 'activity',
        title: 'The admin sees every device',
        text: 'Sales per device, stopping any lost device, and a daily report by email or Telegram.',
      },
    ],
  },
};
