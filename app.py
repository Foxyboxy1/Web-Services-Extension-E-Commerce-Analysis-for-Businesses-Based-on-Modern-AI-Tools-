"""Superstore Analytics — single Flask entry point.

This module consolidates the previous ``app.py`` and ``app_i18n.py`` into one
application. It owns routing, session-based authentication, the bilingual
context and the bridge to the data layer in :mod:`analytics`.

Run it with::

    python app.py

or, for development with auto-reload::

    flask --app app run --debug
"""

from __future__ import annotations

import csv
import hmac
import io
import logging
import os
import secrets
from datetime import date

from flask import (
    Flask,
    Response,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import analytics
from translations import (
    LANGUAGES,
    get_direction,
    get_language,
    get_translations,
)

app = Flask(__name__)

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
# A secret key is required to sign the session cookie. Prefer the environment
# variable; fall back to a random per-process key so that no secret is ever
# committed to the repository. The fallback invalidates sessions on restart,
# which is acceptable for local use and is logged as a warning below.
app.secret_key = os.environ.get("SUPERSTORE_SECRET_KEY") or secrets.token_hex(32)
if not os.environ.get("SUPERSTORE_SECRET_KEY"):
    logging.getLogger(__name__).warning(
        "SUPERSTORE_SECRET_KEY is not set; using a random key for this process. "
        "Sessions will not survive a restart."
    )

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    JSON_SORT_KEYS=False,
)

# Demonstration credentials for the university presentation. They are kept
# only so the project remains runnable out of the box and can be overridden
# through environment variables in any real deployment.
DEMO_EMAIL = os.environ.get("SUPERSTORE_ADMIN_EMAIL", "admin@superstore.com")
DEMO_PASSWORD = os.environ.get("SUPERSTORE_ADMIN_PASSWORD", "Superstore123!")

DEFAULT_ROWS = 8


# --------------------------------------------------------------------------- #
# Localisation plumbing
# --------------------------------------------------------------------------- #
def current_language() -> str:
    return getattr(g, "language", None) or get_language(session.get("language"))


@app.before_request
def load_language() -> None:
    """Resolve the active language once per request and expose it on ``g``."""
    language = get_language(session.get("language"))
    g.language = language
    g.direction = get_direction(language)
    g.translations = get_translations(language)
    g.locale = LANGUAGES[language]["locale"]


@app.context_processor
def inject_globals() -> dict:
    """Values available to every template without repeating them per route."""
    language = current_language()
    return {
        "lang": language,
        "direction": get_direction(language),
        "languages": LANGUAGES,
        "t": get_translations(language),
        "current_year": date.today().year,
        # Translate raw dataset values (used by the filter dropdowns and the
        # share strip) inside the templates.
        "translation_region": lambda key: data_label("region", key),
        "translation_category": lambda key: data_label("cat", key),
        "translation_segment": lambda key: data_label("segment", key),
    }


def t(key: str, **values: object) -> str:
    """Translate ``key`` in the active language, with optional placeholders."""
    text = get_translations(current_language()).get(key, key)
    return text.format(**values) if values else text


# --------------------------------------------------------------------------- #
# Template filters (consistent number / currency formatting)
# --------------------------------------------------------------------------- #
@app.template_filter("currency")
def currency_filter(value: object, decimals: int = 0) -> str:
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        number = 0.0
    symbol = get_translations(current_language()).get("currency_symbol", "$")
    return f"{symbol}{number:,.{decimals}f}"


@app.template_filter("number")
def number_filter(value: object, decimals: int = 0) -> str:
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        number = 0.0
    return f"{number:,.{decimals}f}"


@app.template_filter("percent")
def percent_filter(value: object, decimals: int = 1) -> str:
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        number = 0.0
    return f"{number:,.{decimals}f}%"


def data_label(prefix: str, key: str) -> str:
    """Translate a dataset value such as a category, region or segment."""
    return get_translations(current_language()).get(f"{prefix}_{key}", key)


# --------------------------------------------------------------------------- #
# View-model helpers
# --------------------------------------------------------------------------- #
def read_filters() -> dict:
    """Filters currently requested through the query string."""
    return analytics.normalise_filters(
        {
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date"),
            "region": request.args.get("region"),
            "category": request.args.get("category"),
            "segment": request.args.get("segment"),
            "search": request.args.get("search"),
        }
    )


def chart_payload(data: dict) -> dict:
    """Translate and reshape aggregations into the structure Chart.js expects."""
    return {
        "trend": [
            {"month": point["month"], "sales": point["sales"], "profit": point["profit"]}
            for point in data["trend"]
        ],
        "categories": [
            {
                "label": data_label("cat", item["key"]),
                "value": item["sales"],
                "share": round(item["share"], 1),
            }
            for item in data["categories"]
        ],
        "regions": [
            {
                "label": data_label("region", item["key"]),
                "value": item["sales"],
                "profit": item["profit"],
            }
            for item in data["regions"]
        ],
        "segments": [
            {
                "label": data_label("segment", item["key"]),
                "sales": item["sales"],
                "profit": item["profit"],
            }
            for item in data["segments"]
        ],
    }


def table_rows(data: dict) -> list[dict]:
    """Top products enriched with translated labels for the table."""
    highest = max((p["sales"] for p in data["top_products"]), default=0.0) or 1.0
    rows = []
    for product in data["top_products"]:
        rows.append(
            {
                **product,
                "category_label": data_label("cat", product["category"]),
                "contribution": product["sales"] / highest * 100,
            }
        )
    return rows


def active_filter_list(filters: dict) -> list[dict]:
    """Human readable summary of the filters currently applied."""
    entries = []
    if filters["start_date"]:
        entries.append(
            {"label": t("filter_start_date"), "value": filters["start_date"].isoformat()}
        )
    if filters["end_date"]:
        entries.append(
            {"label": t("filter_end_date"), "value": filters["end_date"].isoformat()}
        )
    if filters["region"]:
        entries.append({"label": t("filter_region"), "value": data_label("region", filters["region"])})
    if filters["category"]:
        entries.append({"label": t("filter_category"), "value": data_label("cat", filters["category"])})
    if filters["segment"]:
        entries.append({"label": t("filter_segment"), "value": data_label("segment", filters["segment"])})
    if filters["search"]:
        entries.append({"label": t("filter_search"), "value": filters["search"]})
    return entries


# --------------------------------------------------------------------------- #
# Routes
# --------------------------------------------------------------------------- #
@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))

    error = None

    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        password = request.form.get("password") or ""

        if not email or not password:
            error = t("error_missing_fields")
        elif "@" not in email or "." not in email.split("@")[-1]:
            error = t("error_invalid_email")
        elif hmac.compare_digest(
            email.encode("utf-8"), DEMO_EMAIL.encode("utf-8")
        ) and hmac.compare_digest(
            password.encode("utf-8"), DEMO_PASSWORD.encode("utf-8")
        ):
            # Capture the language before clearing the session so that a user
            # who switched to Arabic on the login page keeps it after signing in.
            language = current_language()
            session.clear()
            session["logged_in"] = True
            session["email"] = email
            session["language"] = language
            return redirect(url_for("dashboard"))
        else:
            error = t("error_invalid_credentials")

    return render_template(
        "login.html",
        error=error,
        demo_email=DEMO_EMAIL,
        demo_password=DEMO_PASSWORD,
    )


@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login", next=request.path))

    try:
        dataset = analytics.load_data()
    except (FileNotFoundError, ValueError) as exc:
        app.logger.error("Dataset could not be loaded: %s", exc)
        return render_template(
            "error.html",
            error_title=t("error_dataset_title"),
            error_message=t("error_dataset_desc"),
        ), 500

    filters = read_filters()
    data = analytics.build_dashboard(dataset, filters)

    bounds = analytics.date_bounds(dataset)
    options = analytics.filter_options(dataset)

    return render_template(
        "dashboard.html",
        data=data,
        charts=chart_payload(data),
        rows=table_rows(data),
        filters=filters,
        active_filters=active_filter_list(filters),
        options=options,
        bounds=bounds,
        default_rows=DEFAULT_ROWS,
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/set-language/<language>")
def set_language_route(language: str):
    language = get_language(language)
    session["language"] = language

    # Only allow internal, relative redirects to avoid open-redirect issues.
    next_url = request.args.get("next", "")
    if next_url.startswith("/") and not next_url.startswith("//"):
        return redirect(next_url)
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/export/products.csv")
def export_products():
    """Download the currently displayed product table as CSV."""
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    try:
        dataset = analytics.load_data()
    except (FileNotFoundError, ValueError) as exc:
        app.logger.error("Dataset could not be loaded for export: %s", exc)
        return redirect(url_for("dashboard"))

    data = analytics.build_dashboard(dataset, read_filters())

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            t("col_product"),
            t("col_category"),
            t("col_sub_category"),
            t("col_units"),
            t("col_sales"),
            t("col_profit"),
            t("col_margin"),
        ]
    )
    for product in data["top_products"]:
        writer.writerow(
            [
                product["name"],
                data_label("cat", product["category"]),
                product["sub_category"],
                product["quantity"],
                f"{product['sales']:.2f}",
                f"{product['profit']:.2f}",
                f"{product['margin']:.1f}%",
            ]
        )

    return Response(
        "\ufeff" + buffer.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=top-products.csv"},
    )


# --------------------------------------------------------------------------- #
# Error handling — never leak stack traces to the end user
# --------------------------------------------------------------------------- #
@app.errorhandler(404)
def not_found(_error):
    return (
        render_template(
            "error.html",
            error_title=t("error_generic_title"),
            error_message=t("error_generic_desc"),
            error_code=404,
        ),
        404,
    )


@app.errorhandler(500)
def server_error(_error):
    return (
        render_template(
            "error.html",
            error_title=t("error_generic_title"),
            error_message=t("error_generic_desc"),
            error_code=500,
        ),
        500,
    )


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")
