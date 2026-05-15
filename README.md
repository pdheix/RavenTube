<div dir="rtl">

# 🐦‍⬛ RavenTube | ریون تیوب

### دانلودر خودکار یوتیوب با قابلیت جستجو — کاملاً رایگان | Automated YouTube Downloader with Search — Completely Free

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-RavenTube-blue)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## ✨ امکانات | Features

| فارسی | English |
|-------|---------|
| 🎬 دانلود با کیفیت 4K، 1080p، 720p، 480p | 📹 Download up to 4K quality |
| 🎵 استخراج فقط صدا (MP3) | 🎵 Audio-only extraction (MP3) |
| 🔍 جستجوی مستقیم در یوتیوب | 🔍 Direct YouTube search |
| 📝 زیرنویس فارسی + انگلیسی | 📝 Persian + English subtitles |
| 🔒 رمزگذاری فایل ZIP | 🔒 ZIP password protection |
| ⚡ بدون نیاز به VPN | ⚡ No VPN required |
| 📂 اسپلیت خودکار (بخش‌های ۹۵ مگابایتی) | 📂 Auto-split (95 MB parts) |
| 🌙 کار در شب (اجرای خودکار) | 🌙 Runs 24/7 automatically |

---

## 🚀 چگونه استفاده کنیم؟ | How to Use

### ۱. مخزن را Fork کنید | Fork the repository

### ۲. به Actions بروید | Go to Actions tab

### ۳. روی "Run workflow" کلیک کنید | Click "Run workflow"

### ۴. اطلاعات را وارد کنید | Enter your data

| فیلد | توضیح |
|------|-------|
| **video_urls** | لینک یوتیوب یا عبارت جستجو (مثال: `آموزش پایتون` یا `ytsearch5:music`) |
| **quality** | کیفیت: `best` / `2160` / `1080` / `720` / `480` / `audio` |
| **download_subtitles** | `true` یا `false` — دانلود زیرنویس |
| **password** | رمز دلخواه برای ZIP (اختیاری) |

### ۵. منتظر بمانید | Wait for completion

فایل‌ها در پوشه `videos/` قرار می‌گیرند. هر ویدیو در پوشه جداگانه با تصویر و README مخصوص.

Files appear in `videos/` folder. Each video in its own folder with thumbnail and README.

---

## 🔍 مثال‌های جستجو | Search Examples

```bash
# فارسی | Persian
آموزش پایتون
ytsearch5:بهترین آهنگ‌های جدید
ytsearch3:آموزش وردپرس حرفه‌ای

# انگلیسی | English
ytsearch10:best coding tutorials 2024
machine learning course
ytsearch2:podcast AI

# ترکیبی | Mixed
https://youtu.be/abc123 ytsearch3:music
```

---

📁 ساختار خروجی | Output Structure

```
videos/
├── نام-ویدیو/
│   ├── نام-ویدیو.mp4        (یا فایل‌های .z01, .z02 در صورت بزرگ بودن)
│   ├── thumbnail.jpg
│   ├── subtitle.zip          (اگر فعال شده باشد)
│   └── README.md             (لینک دانلود مستقیم)
└── README.md                 (فهرست همه ویدیوها)
```

فایل‌های بزرگتر از ۹۵ مگابایت به چند بخش تقسیم می‌شوند. همه بخش‌ها را دانلود کرده و فایل اصلی .zip را باز کنید.

Files larger than 95 MB are split into multiple parts. Download all parts and open the main .zip file.

---

🛠️ ابزارهای کمکی | Helper Tools

Workflow کاربرد
cleaner.yml حذف تمام ویدیوها از مخزن
history_cleaner.yml پاکسازی تاریخچه گیت و کاهش حجم مخزن

---

⚠️ توجه قانونی | Legal Notice

· این ابزار فقط برای استفاده شخصی و آموزشی است | For personal and educational use only
· مسئولیت استفاده از محتوای دانلودی بر عهده کاربر است | User is responsible for downloaded content
· رعایت قوانین کپی رایت کشور خود الزامی است | Respect your country's copyright laws

---

📞 ارتباط | Contact

· مستندات کامل | Full documentation
· گزارش مشکل | Report issue
· پیشنهادات | Suggestions

---

ساخته شده با ❤️ برای جامعه فارسی‌زبان | Built with ❤️ for Persian community

</div>
