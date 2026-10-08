# دليل النشر على VPS

الموقع **ثابت بالكامل (static)**: الناتج مجلد `dist/` يخدمه nginx مباشرة، ولا يحتاج Node.js على السيرفر.

## ما تحتاجه
- VPS بنظام Ubuntu/Debian ووصول SSH (مفتاح SSH، لا كلمة مرور).
- نطاق (domain) موجَّه بسجل `A` إلى عنوان الـ VPS.
- على جهازك: Node.js 22.12 أو أحدث، و`rsync` (أو أي أداة نسخ).

## 1) تجهيز السيرفر (مرة واحدة)
```bash
sudo apt update && sudo apt install -y nginx certbot python3-certbot-nginx
sudo mkdir -p /var/www/pharmflow
sudo chown -R $USER:$USER /var/www/pharmflow
```

انسخ [deploy/nginx.conf.template](deploy/nginx.conf.template) إلى `/etc/nginx/sites-available/pharmflow`، واستبدل `YOUR_DOMAIN` بنطاقك، ثم:
```bash
sudo ln -s /etc/nginx/sites-available/pharmflow /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d YOUR_DOMAIN -d www.YOUR_DOMAIN   # شهادة HTTPS مجانية وتجديد تلقائي
```

## 2) بناء الموقع ورفعه (كل تحديث)
من جذر المشروع على جهازك:
```bash
SITE_URL=https://YOUR_DOMAIN \
VPS_HOST=عنوان_السيرفر VPS_USER=اسم_المستخدم VPS_PATH=/var/www/pharmflow \
./deploy/deploy.sh
```
السكربت يُنفّذ `npm ci` ثم `npm run check` ثم `npm run build` ثم يرفع `dist/` بـ rsync. لا يخزّن أي كلمة مرور.

بدون rsync: نفّذ `SITE_URL=https://YOUR_DOMAIN npm run build` ثم انسخ **محتويات** `dist/` إلى `/var/www/pharmflow/` بأي أداة (scp / SFTP).

## ملفات التحميل (Android وWindows)
ملفا التثبيت كبيران (≈140MB) فلا يُحفظان في git، لكنهما يُنسخان مع الموقع عند البناء:
1. ضع الملفين في `public/downloads/` بالاسمين `PharmFlow-<الإصدار>-Android.apk` و`PharmFlow-Setup-<الإصدار>-Windows.exe`.
2. شغّل `python deploy/update-downloads.py` لتحديث الحجم وبصمة SHA-256 المعروضتين في الموقع.
3. ابنِ وارفع كالمعتاد (`./deploy/deploy.sh`). يرفع rsync الملفين مع `dist/`.

بيانات التواصل (البريد والهاتف) في `src/data/contact.json`.

## 3) الصفحات بعد النشر
| المسار | المحتوى |
|---|---|
| `/` | الموقع بالعربية |
| `/en/` | النسخة الإنكليزية |
| `/docs/` | دليل الصيدلية (عربي) |
| `/slides/` | العرض التقديمي |

## 4) تحديث "ما الجديد"
أضف ملف `.mdx` في `src/content/releases/ar/` وآخر مطابقاً في `en/` (الحقول: `title`, `date`, `version`, `status`) ثم أعد البناء والرفع. تظهر أحدث ثلاثة إصدارات.

## ملاحظات
- يجب ضبط `SITE_URL` عند البناء لتكون الروابط المطلقة صحيحة.
- إن وضعت الموقع في مسار فرعي (مثل `/pharmflow/`) فأضف `base` في [astro.config.mjs](astro.config.mjs).
- ملف `.github/workflows/deploy.yml.disabled` كان لـ GitHub Pages وتم تعطيله.
