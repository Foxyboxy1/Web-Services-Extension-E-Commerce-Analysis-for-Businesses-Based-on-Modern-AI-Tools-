"""Bilingual (English / Arabic) interface strings.

Keeping every user-facing string in one dictionary keeps the Jinja templates
free of conditional translation logic. Add a new string by adding the same key
to both the ``en`` and ``ar`` blocks below.

The Arabic wording is deliberately short and everyday (Egyptian-flavoured) so
that the dashboard stays easy to read for a non-technical audience.
"""

from __future__ import annotations

DEFAULT_LANGUAGE = "en"

# Language metadata: text direction, display label and locale used for
# client-side number/date formatting.
LANGUAGES = {
    "en": {
        "code": "en",
        "label": "English",
        "short": "EN",
        "direction": "ltr",
        "locale": "en-US",
    },
    "ar": {
        "code": "ar",
        "label": "العربية",
        "short": "ع",
        "direction": "rtl",
        "locale": "ar-EG",
    },
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        # ---------------------------------------------------------------- brand
        "app_name": "Superstore Analytics",
        "app_version": "BI Platform v2.4",
        "app_tagline": "Make every margin count.",
        "app_description": "Sales and profit, all in one place.",
        "brand_eyebrow": "STORE INTELLIGENCE",
        # ---------------------------------------------------------------- login
        "login_eyebrow": "WELCOME BACK",
        "login_title": "Sign in",
        "login_subtitle": "Enter your details to continue.",
        "email_label": "Email",
        "email_placeholder": "you@company.com",
        "password_label": "Password",
        "password_placeholder": "Your password",
        "sign_in": "Sign in",
        "signing_in": "Signing in…",
        "show_password": "Show password",
        "hide_password": "Hide password",
        "demo_credentials": "Demo login",
        "demo_credentials_note": (
            "For the demo only. Change it with the SUPERSTORE_ADMIN_* variables."
        ),
        "error_invalid_credentials": "Wrong email or password.",
        "error_missing_fields": "Enter your email and password.",
        "error_invalid_email": "Enter a valid email address.",
        # ---------------------------------------------------------------- nav
        "nav_overview": "Overview",
        "nav_sales": "Sales",
        "nav_products": "Products",
        "nav_reports": "Export",
        "nav_section_main": "Menu",
        # ------------------------------------------------------------- header
        "page_title": "Sales Overview",
        "breadcrumb_root": "Dashboard",
        "breadcrumb_current": "Overview",
        "skip_to_content": "Skip to content",
        "search_placeholder": "Search products, customers or cities…",
        "notifications": "Alerts",
        "account_role": "Admin",
        "account_name": "Superstore Admin",
        "logout": "Log out",
        "language_switch": "العربية",
        "language_switch_title": "Switch to Arabic",
        # ---------------------------------------------------------- dashboard
        "dashboard_heading": "Performance",
        "dashboard_subheading": "Sales, profit and growth at a glance.",
        "filters_heading": "Filters",
        "filter_metrics": "Filters",
        "export_report": "Export CSV",
        "apply_filters": "Apply",
        "reset_filters": "Reset",
        "filter_start_date": "From",
        "filter_end_date": "To",
        "filter_region": "Region",
        "filter_category": "Category",
        "filter_segment": "Customer type",
        "filter_search": "Search",
        "option_all": "All",
        "active_filters": "Applied",
        "dataset_range": "Data range",
        "results_count": "{count} rows",
        # ---------------------------------------------------------------- kpi
        "kpi_total_sales": "Total Sales",
        "kpi_total_profit": "Total Profit",
        "kpi_total_orders": "Orders",
        "kpi_profit_margin": "Profit Margin",
        "kpi_vs_previous": "vs previous period",
        "kpi_previous_hint": "Add dates to compare.",
        "unit_pp": "pp",
        # -------------------------------------------------------------- charts
        "chart_trend_title": "Sales & Profit",
        "chart_category_title": "Sales by Category",
        "chart_region_title": "Sales by Region",
        "chart_segment_title": "Sales vs Profit by Customer Type",
        "series_sales": "Sales",
        "series_profit": "Profit",
        "chart_empty": "No data for these filters.",
        # --------------------------------------------------------------- table
        "table_top_products": "Top Selling Products",
        "col_product": "Product",
        "col_category": "Category",
        "col_sub_category": "Sub-category",
        "col_units": "Units",
        "col_sales": "Sales",
        "col_profit": "Profit",
        "col_margin": "Margin",
        "col_performance": "Share",
        "table_filter_placeholder": "Filter products…",
        "empty_title": "No results",
        "empty_description": "Nothing matches these filters. Widen the dates or clear a filter.",
        # -------------------------------------------------------------- toasts
        "toast_filter_title": "Filters updated",
        "toast_filter_desc": "Numbers refreshed for the new filters.",
        "toast_reset_title": "Filters cleared",
        "toast_reset_desc": "Showing the full dataset again.",
        "toast_export_title": "Export started",
        "toast_export_desc": "Preparing the table as a CSV file.",
        "toast_notifications_title": "Alerts",
        "toast_notifications_desc": "You have {count} dataset alerts.",
        "toast_language_title": "Language changed",
        "toast_language_desc": "The interface is now in {language}.",
        "toast_logout_title": "Signed out",
        "toast_logout_desc": "Your session ended.",
        # -------------------------------------------------------------- errors
        "error_dataset_title": "Dataset unavailable",
        "error_dataset_desc": (
            "Check that data/Sample-Superstore.csv exists, then restart the app."
        ),
        "error_generic_title": "Something went wrong",
        "error_generic_desc": "The request could not be completed. Please try again.",
        "back_to_login": "Back to sign in",
        # -------------------------------------------------------- data values
        "cat_Technology": "Technology",
        "cat_Furniture": "Furniture",
        "cat_Office Supplies": "Office Supplies",
        "region_Central": "Central",
        "region_East": "East",
        "region_South": "South",
        "region_West": "West",
        "segment_Consumer": "Consumer",
        "segment_Corporate": "Corporate",
        "segment_Home Office": "Home Office",
        "currency_symbol": "$",
        "footer_note": "Graduation project · Superstore Analytics",
    },
    "ar": {
        # ---------------------------------------------------------------- brand
        "app_name": "تحليلات المتجر",
        "app_version": "منصة ذكاء الأعمال ٢٫٤",
        "app_tagline": "خلّي كل جنيه محسوب.",
        "app_description": "البيع والأرباح كلها في مكان واحد.",
        "brand_eyebrow": "ذكاء المتجر",
        # ---------------------------------------------------------------- login
        "login_eyebrow": "أهلاً بيك",
        "login_title": "دخول",
        "login_subtitle": "اكتب بياناتك وخلّينا نبدأ.",
        "email_label": "الإيميل",
        "email_placeholder": "you@company.com",
        "password_label": "كلمة السر",
        "password_placeholder": "اكتب كلمة السر",
        "sign_in": "دخول",
        "signing_in": "بندخّل…",
        "show_password": "إظهار كلمة السر",
        "hide_password": "تخبية كلمة السر",
        "demo_credentials": "بيانات دخول للتجربة",
        "demo_credentials_note": (
            "للعرض بس. تغيّرها من متغيّرات SUPERSTORE_ADMIN_*."
        ),
        "error_invalid_credentials": "الإيميل أو كلمة السر غلط.",
        "error_missing_fields": "اكتب الإيميل وكلمة السر.",
        "error_invalid_email": "اكتب إيميل صحيح.",
        # ---------------------------------------------------------------- nav
        "nav_overview": "الرئيسية",
        "nav_sales": "المبيعات",
        "nav_products": "المنتجات",
        "nav_reports": "تصدير",
        "nav_section_main": "القائمة",
        # ------------------------------------------------------------- header
        "page_title": "نظرة على المبيعات",
        "breadcrumb_root": "الرئيسية",
        "breadcrumb_current": "نظرة عامة",
        "skip_to_content": "روح على المحتوى",
        "search_placeholder": "دوّر على منتج أو عميل أو مدينة…",
        "notifications": "تنبيهات",
        "account_role": "مدير",
        "account_name": "مدير المتجر",
        "logout": "خروج",
        "language_switch": "English",
        "language_switch_title": "حوّل للإنجليزي",
        # ---------------------------------------------------------- dashboard
        "dashboard_heading": "الأداء",
        "dashboard_subheading": "البيع والأرباح والنمو في نظرة واحدة.",
        "filters_heading": "الفلاتر",
        "filter_metrics": "الفلاتر",
        "export_report": "تصدير CSV",
        "apply_filters": "تطبيق",
        "reset_filters": "إلغاء",
        "filter_start_date": "من",
        "filter_end_date": "إلى",
        "filter_region": "المنطقة",
        "filter_category": "الفئة",
        "filter_segment": "نوع العميل",
        "filter_search": "بحث",
        "option_all": "الكل",
        "active_filters": "المطبّق",
        "dataset_range": "نطاق البيانات",
        "results_count": "{count} صف",
        # ---------------------------------------------------------------- kpi
        "kpi_total_sales": "إجمالي البيع",
        "kpi_total_profit": "إجمالي الأرباح",
        "kpi_total_orders": "عدد الطلبات",
        "kpi_profit_margin": "نسبة الربح",
        "kpi_vs_previous": "عن الفترة اللي قبلها",
        "kpi_previous_hint": "حدّد تواريخ للمقارنة.",
        "unit_pp": "ن.م",
        # -------------------------------------------------------------- charts
        "chart_trend_title": "المبيعات والأرباح",
        "chart_category_title": "البيع حسب الفئة",
        "chart_region_title": "البيع حسب المنطقة",
        "chart_segment_title": "المبيعات والأرباح حسب نوع العميل",
        "series_sales": "المبيعات",
        "series_profit": "الأرباح",
        "chart_empty": "مفيش بيانات للفلاتر دي.",
        # --------------------------------------------------------------- table
        "table_top_products": "أكتر المنتجات اللي بتبيع",
        "col_product": "المنتج",
        "col_category": "الفئة",
        "col_sub_category": "الفئة الفرعية",
        "col_units": "القطع",
        "col_sales": "البيع",
        "col_profit": "الربح",
        "col_margin": "الهامش",
        "col_performance": "النسبة",
        "table_filter_placeholder": "فلتر المنتجات…",
        "empty_title": "مفيش نتايج",
        "empty_description": "مفيش حاجة بالفلاتر دي. وسّع المدة أو شيل فلتر.",
        # -------------------------------------------------------------- toasts
        "toast_filter_title": "اتطبقت الفلاتر",
        "toast_filter_desc": "الأرقام اتحدّثت على الفلاتر الجديدة.",
        "toast_reset_title": "اتلغت الفلاتر",
        "toast_reset_desc": "بنعرض كل البيانات تاني.",
        "toast_export_title": "بنصدّر",
        "toast_export_desc": "بنجهّز الجدول كملف CSV.",
        "toast_notifications_title": "تنبيهات",
        "toast_notifications_desc": "عندك {count} تنبيه على البيانات.",
        "toast_language_title": "اتغيّرت اللغة",
        "toast_language_desc": "الواجهة دلوقتي بالـ {language}.",
        "toast_logout_title": "خرجت",
        "toast_logout_desc": "الجلسة اتقفلت.",
        # -------------------------------------------------------------- errors
        "error_dataset_title": "البيانات مش موجودة",
        "error_dataset_desc": (
            "اتأكد إن ملف data/Sample-Superstore.csv موجود، وبعدين شغّل البرنامج تاني."
        ),
        "error_generic_title": "حصلت مشكلة",
        "error_generic_desc": "الطلب مكملش. جرّب تاني.",
        "back_to_login": "رجوع لتسجيل الدخول",
        # -------------------------------------------------------- data values
        "cat_Technology": "تقنية",
        "cat_Furniture": "أثاث",
        "cat_Office Supplies": "مستلزمات مكتبية",
        "region_Central": "الوسط",
        "region_East": "الشرق",
        "region_South": "الجنوب",
        "region_West": "الغرب",
        "segment_Consumer": "أفراد",
        "segment_Corporate": "شركات",
        "segment_Home Office": "مكاتب منزلية",
        "currency_symbol": "$",
        "footer_note": "مشروع تخرج · تحليلات المتجر",
    },
}


def get_language(candidate: str | None) -> str:
    """Return a supported language code, falling back to the default."""
    if candidate in TRANSLATIONS:
        return candidate
    return DEFAULT_LANGUAGE


def get_translations(language: str) -> dict[str, str]:
    """Full string dictionary for ``language`` (already validated)."""
    return TRANSLATIONS[get_language(language)]


def get_direction(language: str) -> str:
    return LANGUAGES[get_language(language)]["direction"]
