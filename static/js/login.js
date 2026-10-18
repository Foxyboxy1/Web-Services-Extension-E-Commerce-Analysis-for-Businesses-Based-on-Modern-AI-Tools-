/* Login page behaviour: password visibility toggle and submit feedback. */
(function () {
    "use strict";

    var form = document.getElementById("login-form");
    var toggle = document.getElementById("password-toggle");
    var passwordInput = document.getElementById("password");
    var submitButton = document.getElementById("login-submit");

    if (toggle && passwordInput) {
        toggle.addEventListener("click", function () {
            var isVisible = passwordInput.type === "text";

            passwordInput.type = isVisible ? "password" : "text";
            toggle.setAttribute("aria-pressed", String(!isVisible));
            toggle.setAttribute(
                "aria-label",
                isVisible ? toggle.dataset.labelShow : toggle.dataset.labelHide
            );
            toggle.innerHTML = isVisible
                ? toggle.dataset.iconShow
                : toggle.dataset.iconHide;

            passwordInput.focus();
        });
    }

    if (form && submitButton) {
        form.addEventListener("submit", function () {
            var label = submitButton.querySelector(".btn-label");

            submitButton.disabled = true;
            submitButton.setAttribute("aria-busy", "true");
            if (label) {
                label.textContent = submitButton.dataset.labelBusy;
            }
        });
    }
})();
