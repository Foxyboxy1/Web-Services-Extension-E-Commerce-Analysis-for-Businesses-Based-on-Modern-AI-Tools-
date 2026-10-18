# Superstore Analytics

لوحة تحليلات مبيعات وذكاء أعمال (BI Dashboard) مبنية بـ Flask + pandas، وواجهة ثنائية اللغة (عربي / English).
A sales & business-intelligence dashboard built with Flask + pandas, with a bilingual UI (Arabic RTL / English LTR).

---


### قبل ما تبدأ — المتطلبات
- **Python 3.10 أو أحدث** (نزّله من python.org وعلّم على "Add Python to PATH" وقت التثبيت).
- أي متصفح حديث (Chrome / Edge / Firefox).
- النت مش مطلوب للبرنامج نفسه، بس محتاج نت أول مرة بس لتثبيت المكتبات.

### خطوات التشغيل (Windows)
افتح PowerShell جوه فولدر المشروع واكتب:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

### خطوات التشغيل (macOS / Linux)

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

هتلاقي رسالة `Running on http://127.0.0.1:5000`. افتح اللينك ده في المتصفح.

### الدخول
| | |
|---|---|
| الإيميل | `admin@superstore.com` |
| الباسورد | `Superstore123!` |

### إزاي تستخدم اللوحة
1. **فلتر التواريخ** — اختار "من تاريخ" و"لتاريخ" واضغط تطبيق.
2. **الفلترات** — المنطقة / الفئة / نوع العميل / بحث في المنتجات، و"إعادة تعيين" لرجوع كل حاجة.
3. **الكروت والأشكال** — بتتحدّث لوحدها مع كل فلتر.
4. **الجدول** — فلتر سريع فوقه، وزر تصدير CSV تحته.
5. **اللغة** — زر AR/EN فوق على اليمين، لغة الصفحة بتتحفظ معاك.
6. **الخروج** — من آخر الشريط الجانبي.

### إعدادات اختيارية (متغيرات البيئة)
```powershell
$env:SUPERSTORE_SECRET_KEY = "مفتاح-سري-طويل"
$env:SUPERSTORE_ADMIN_EMAIL = "you@example.com"
$env:SUPERSTORE_ADMIN_PASSWORD = "كلمة-سر-قوية"
$env:FLASK_DEBUG = "1"   # للتطوير بس
```

### ملاحظات مهمة للريبو
- **ما ترفعش** مجلد `.venv` ولا `__pycache__` — ضيفهم في `.gitignore`.
- البيانات في `data/Sample-Superstore.csv` (9994 صف) وهي بيانات الديمو، تقدر تبدّلها بأي ملف بنفس أسماء الأعمدة.

### شكل المشروع
```
app.py            نقطة التشغيل والمسارات
analytics.py      قراءة البيانات والحسابات
translations.py   نصوص العربي والإنجليزي
templates/        صفحات HTML (login / dashboard / error)
static/           CSS + JS + Chart.js (مستضاف محلياً)
data/             ملف البيانات
```

### لو حصلت مشكلة
- **`ERR_CONNECTION_REFUSED`** → السيرفر مقفول، شغّل `app.py` تاني وسيب الترمنال مفتوح.
- **`python` مش معروف** → Python مش متثبت أو مش مضاف للـ PATH.
- **الخطوط أو الأيقونات مش ظاهرة** → البرنامج شغال أوفلاين، بس نضّف الكاش (Ctrl + F5).

---

## 🇬🇧 English

### Requirements
- **Python 3.10+** (check "Add Python to PATH" during installation).
- A modern browser (Chrome / Edge / Firefox).
- Internet is only needed once, to install the dependencies.

### Setup (Windows)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

### Setup (macOS / Linux)

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Then open **http://127.0.0.1:5000**.

### Sign in
| | |
|---|---|
| Email | `admin@superstore.com` |
| Password | `Superstore123!` |

### Using the dashboard
1. **Date range** — pick "from" and "to", then apply.
2. **Filters** — region / category / segment / product search; use reset to clear everything.
3. **KPI cards & charts** — they react to every filter automatically.
4. **Table** — quick filter above it, CSV export below it.
5. **Language** — the AR/EN switch in the header; your choice is remembered.
6. **Logout** — bottom of the sidebar.

### Optional environment variables
```powershell
$env:SUPERSTORE_SECRET_KEY = "a-long-random-secret"
$env:SUPERSTORE_ADMIN_EMAIL = "you@example.com"
$env:SUPERSTORE_ADMIN_PASSWORD = "a-strong-password"
$env:FLASK_DEBUG = "1"   # development only
```

### Notes for the repository
- **Do not commit** `.venv` or `__pycache__` — add them to `.gitignore`.
- Demo data lives in `data/Sample-Superstore.csv` (9,994 rows); replace it with any file using the same column names.

### Project layout
```
app.py            entry point, routes, session auth
analytics.py      data loading & calculations
translations.py   Arabic / English strings
templates/        HTML pages (login / dashboard / error)
static/           CSS + JS + locally hosted Chart.js
data/             the dataset
```

### Troubleshooting
- **`ERR_CONNECTION_REFUSED`** → the server is stopped; run `app.py` again and keep the terminal open.
- **`python` is not recognised** → Python is missing or not on PATH.
- **Fonts or icons look wrong** → the app works offline; just hard-refresh with Ctrl + F5.
