from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "replace-this-with-a-long-random-secret-key"

# Temporary demo credentials
DEMO_EMAIL = "admin@superstore.com"
DEMO_PASSWORD = "Superstore123!"

TRANSLATIONS = {
    "en": {
        "app_name": "Superstore Analytics",
        "login_title": "Welcome back",
        "login_subtitle": "Sign in to continue to your analytics dashboard.",
        "email": "Email address",
        "password": "Password",
        "email_placeholder": "admin@superstore.com",
        "password_placeholder": "Enter your password",
        "login_button": "Sign in",
        "invalid_credentials": "Invalid email or password.",
        "dashboard": "Dashboard",
        "overview": "Overview",
        "sales": "Sales",
        "profit": "Profit",
        "orders": "Orders",
        "profit_margin": "Profit margin",
        "logout": "Log out",
        "language": "العربية",
        "language_code": "ar",
    },
    "ar": {
        "app_name": "تحليلات المتجر",
        "login_title": "أهلاً بعودتك",
        "login_subtitle": "سجّل الدخول لمتابعة لوحة التحليلات.",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "email_placeholder": "admin@superstore.com",
        "password_placeholder": "أدخل كلمة المرور",
        "login_button": "تسجيل الدخول",
        "invalid_credentials": "البريد الإلكتروني أو كلمة المرور غير صحيحة.",
        "dashboard": "لوحة التحكم",
        "overview": "نظرة عامة",
        "sales": "المبيعات",
        "profit": "الأرباح",
        "orders": "الطلبات",
        "profit_margin": "هامش الربح",
        "logout": "تسجيل الخروج",
        "language": "English",
        "language_code": "en",
    },
}


@app.before_request
def set_language():
    """Use the language saved in the session; default to English."""
    language = session.get("language", "en")
    if language not in TRANSLATIONS:
        language = "en"
    # Expose these values to every Jinja template.
    request.language = language
    request.direction = "rtl" if language == "ar" else "ltr"
    request.translations = TRANSLATIONS[language]


@app.context_processor
def inject_language_settings():
    return {
        "lang": getattr(request, "language", "en"),
        "direction": getattr(request, "direction", "ltr"),
        "t": getattr(request, "translations", TRANSLATIONS["en"]),
    }


@app.route("/set-language/<language>")
def set_language_route(language):
    if language in TRANSLATIONS:
        session["language"] = language

    # Return to the page the user was on, with a safe local fallback.
    next_url = request.args.get("next", "")
    if next_url.startswith("/") and not next_url.startswith("//"):
        return redirect(next_url)
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if email == DEMO_EMAIL and password == DEMO_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))

        error = t("invalid_credentials")

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))


def t(key):
    language = session.get("language", "en")
    return TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(key, key)


if __name__ == "__main__":
    app.run(debug=True)
