
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary demo credentials
DEMO_EMAIL = "admin@superstore.com"
DEMO_PASSWORD = "Superstore123!"


@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if email == DEMO_EMAIL and password == DEMO_PASSWORD:
            return redirect(url_for("dashboard"))

        error = "Invalid email or password."

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)