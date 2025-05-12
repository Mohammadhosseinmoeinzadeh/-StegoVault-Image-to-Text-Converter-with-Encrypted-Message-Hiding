
# 🖼️🔐 Image & Text Converter | تبدیل متن و تصویر

## English 🇬🇧

This is a graphical Python application that lets you:
- Convert an image to a text file (with embedded encrypted message).
- Embed a message into an image and save it.
- Read an encrypted message hidden inside an image.

### ✨ Features
- Message encryption using `Fernet` (AES encryption).
- Hidden messages stored in EXIF metadata.
- Easy-to-use graphical interface (Tkinter).
- Base64 encoding to store image data in text files.

### 🛠️ Requirements
- Python 3.x
- Pillow
- cryptography
- piexif

Install dependencies:
```bash
pip install pillow cryptography piexif
```

### 🚀 Usage
Run the main application:
```bash
python img.py
```

To generate a new encryption key (optional):
```bash
python ky.py
```

---

##  🇮🇷

این برنامه‌ی گرافیکی با زبان پایتون طراحی شده تا:
- یک پیام رمزنگاری‌شده را درون یک تصویر ذخیره کند.
- از تصویر، فایل متنی بسازد که شامل پیام پنهان است.
- پیام مخفی درون تصویر را بخواند.

### ✨ امکانات
- رمزنگاری پیام‌ها با استفاده از الگوریتم `Fernet`.
- ذخیره‌سازی پیام‌ها در اطلاعات EXIF تصویر.
- رابط کاربری ساده و کاربردی با Tkinter.
- تبدیل تصویر به رشته‌ی متنی با فرمت base64.

### 🛠️ پیش‌نیازها
- Python نسخه ۳ به بالا
- کتابخانه‌های:
  - Pillow
  - cryptography
  - piexif

برای نصب پیش‌نیازها:
```bash
pip install pillow cryptography piexif
```

### 🚀 اجرا
اجرای برنامه‌ی اصلی:
```bash
python img.py
```

تولید کلید رمزنگاری جدید (اختیاری):
```bash
python ky.py
```

---

📌 **توجه:** کلید رمزنگاری به صورت ثابت در کد قرار دارد. در صورت نیاز می‌توانید با استفاده از `ky.py` یک کلید جدید ایجاد کرده و در کد جایگزین کنید.
