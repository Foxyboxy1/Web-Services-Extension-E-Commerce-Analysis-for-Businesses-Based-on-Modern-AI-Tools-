/* ==========================================================================
   Superstore Analytics — dashboard behaviour
   Renders the Chart.js charts from the server-provided JSON payload and
   wires the interactive elements of the dashboard (table filter, sidebar,
   notifications and toasts). No data is generated on the client.
   ========================================================================== */
(function () {
    "use strict";

    var dataElement = document.getElementById("dashboard-data");
    var configElement = document.getElementById("dashboard-config");

    var data = dataElement ? JSON.parse(dataElement.textContent) : null;
    var config = configElement ? JSON.parse(configElement.textContent) : {};

    var numberLocale = config.numberLocale || "en-US";
    var displayLocale = config.locale || numberLocale;
    var currencySymbol = config.currency || "";

    var COLORS = {
        sales: "#2563eb",
        profit: "#60a5fa",
        grid: "rgba(148, 163, 184, 0.25)",
        ticks: "#64748b",
        palette: ["#2563eb", "#60a5fa", "#93c5fd", "#bfdbfe", "#dbeafe"]
    };

    /* ------------------------------------------------------------------ format */
    function formatCurrency(value) {
        return currencySymbol + new Intl.NumberFormat(numberLocale, {
            maximumFractionDigits: 0
        }).format(value);
    }

    function formatNumber(value) {
        return new Intl.NumberFormat(numberLocale, {
            maximumFractionDigits: 0
        }).format(value);
    }

    function compactCurrency(value) {
        return currencySymbol + new Intl.NumberFormat(numberLocale, {
            notation: "compact",
            maximumFractionDigits: 1
        }).format(value);
    }

    function monthLabel(key) {
        var parts = String(key).split("-");
        var date = new Date(Number(parts[0]), Number(parts[1]) - 1, 1);
        return new Intl.DateTimeFormat(displayLocale, {
            month: "short",
            year: "2-digit"
        }).format(date);
    }

    /* ------------------------------------------------------------------ charts */
    function showEmpty(canvasId) {
        var canvas = document.getElementById(canvasId);
        if (!canvas) {
            return;
        }
        canvas.hidden = true;
        var empty = canvas.parentElement.querySelector(".chart-empty");
        if (empty) {
            empty.hidden = false;
        }
    }

    function baseScales() {
        return {
            x: {
                grid: { display: false },
                border: { display: false },
                ticks: { color: COLORS.ticks, font: { size: 11 } }
            },
            y: {
                beginAtZero: true,
                grid: { color: COLORS.grid },
                border: { display: false },
                ticks: {
                    color: COLORS.ticks,
                    font: { size: 11 },
                    callback: function (value) {
                        return compactCurrency(value);
                    }
                }
            }
        };
    }

    function baseOptions() {
        return {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: "index", intersect: false },
            plugins: {
                legend: { display: false },
                tooltip: {
                    padding: 10,
                    callbacks: {
                        label: function (context) {
                            var label = context.dataset.label || "";
                            var value = context.parsed.y !== undefined
                                ? context.parsed.y
                                : context.parsed;
                            return label
                                ? label + ": " + formatCurrency(value)
                                : formatCurrency(value);
                        }
                    }
                }
            },
            scales: baseScales()
        };
    }

    function buildCharts() {
        if (typeof Chart === "undefined" || !data) {
            ["trend-chart", "category-chart", "region-chart", "segment-chart"].forEach(showEmpty);
            return;
        }

        Chart.defaults.font.family =
            getComputedStyle(document.body).fontFamily || "sans-serif";

        /* -------- Sales & Profit trend (line) -------- */
        if (data.trend && data.trend.length) {
            new Chart(document.getElementById("trend-chart"), {
                type: "line",
                data: {
                    labels: data.trend.map(function (point) {
                        return monthLabel(point.month);
                    }),
                    datasets: [
                        {
                            label: config.sales,
                            data: data.trend.map(function (point) {
                                return point.sales;
                            }),
                            borderColor: COLORS.sales,
                            backgroundColor: "rgba(37, 99, 235, 0.12)",
                            fill: true,
                            tension: 0.35,
                            borderWidth: 2.5,
                            pointRadius: 0,
                            pointHoverRadius: 4
                        },
                        {
                            label: config.profit,
                            data: data.trend.map(function (point) {
                                return point.profit;
                            }),
                            borderColor: COLORS.profit,
                            backgroundColor: "rgba(96, 165, 250, 0.12)",
                            fill: true,
                            tension: 0.35,
                            borderWidth: 2.5,
                            pointRadius: 0,
                            pointHoverRadius: 4
                        }
                    ]
                },
                options: baseOptions()
            });
        } else {
            showEmpty("trend-chart");
        }

        /* -------- Sales by category (doughnut) -------- */
        if (data.categories && data.categories.length) {
            new Chart(document.getElementById("category-chart"), {
                type: "doughnut",
                data: {
                    labels: data.categories.map(function (item) {
                        return item.label;
                    }),
                    datasets: [
                        {
                            data: data.categories.map(function (item) {
                                return item.value;
                            }),
                            backgroundColor: COLORS.palette,
                            borderColor: "#ffffff",
                            borderWidth: 2,
                            hoverOffset: 6
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: "72%",
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            padding: 10,
                            callbacks: {
                                label: function (context) {
                                    return context.label + ": " + formatCurrency(context.parsed);
                                }
                            }
                        }
                    }
                }
            });
        } else {
            showEmpty("category-chart");
        }

        /* -------- Sales by region (bar) -------- */
        if (data.regions && data.regions.length) {
            new Chart(document.getElementById("region-chart"), {
                type: "bar",
                data: {
                    labels: data.regions.map(function (item) {
                        return item.label;
                    }),
                    datasets: [
                        {
                            label: config.sales,
                            data: data.regions.map(function (item) {
                                return item.value;
                            }),
                            backgroundColor: COLORS.sales,
                            borderRadius: 8,
                            maxBarThickness: 46
                        }
                    ]
                },
                options: baseOptions()
            });
        } else {
            showEmpty("region-chart");
        }

        /* -------- Sales vs profit by segment (grouped bar) -------- */
        if (data.segments && data.segments.length) {
            new Chart(document.getElementById("segment-chart"), {
                type: "bar",
                data: {
                    labels: data.segments.map(function (item) {
                        return item.label;
                    }),
                    datasets: [
                        {
                            label: config.sales,
                            data: data.segments.map(function (item) {
                                return item.sales;
                            }),
                            backgroundColor: COLORS.sales,
                            borderRadius: 8,
                            maxBarThickness: 34
                        },
                        {
                            label: config.profit,
                            data: data.segments.map(function (item) {
                                return item.profit;
                            }),
                            backgroundColor: COLORS.profit,
                            borderRadius: 8,
                            maxBarThickness: 34
                        }
                    ]
                },
                options: baseOptions()
            });
        } else {
            showEmpty("segment-chart");
        }
    }

    /* ------------------------------------------------------------------- table */
    function wireTableFilter() {
        var input = document.getElementById("table-filter");
        var body = document.getElementById("product-rows");
        var empty = document.getElementById("table-empty");

        if (!input || !body) {
            return;
        }

        input.addEventListener("input", function () {
            var term = input.value.trim().toLowerCase();
            var rows = body.querySelectorAll("tr");
            var visible = 0;

            Array.prototype.forEach.call(rows, function (row) {
                var haystack = row.getAttribute("data-search") || "";
                var match = !term || haystack.indexOf(term) !== -1;
                row.hidden = !match;
                if (match) {
                    visible += 1;
                }
            });

            if (empty) {
                empty.hidden = visible !== 0;
            }
        });
    }

    /* ------------------------------------------------------------------ sidebar */
    function wireSidebar() {
        var sidebar = document.getElementById("sidebar");
        var scrim = document.getElementById("sidebar-scrim");
        var toggle = document.querySelector(".sidebar-toggle");

        if (!sidebar) {
            return;
        }

        function setOpen(open) {
            sidebar.classList.toggle("is-open", open);
            if (scrim) {
                scrim.classList.toggle("is-visible", open);
            }
            if (toggle) {
                toggle.setAttribute("aria-expanded", open ? "true" : "false");
            }
        }

        if (toggle) {
            toggle.addEventListener("click", function () {
                setOpen(!sidebar.classList.contains("is-open"));
            });
        }

        if (scrim) {
            scrim.addEventListener("click", function () {
                setOpen(false);
            });
        }

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                setOpen(false);
            }
        });

        Array.prototype.forEach.call(
            document.querySelectorAll("[data-nav]"),
            function (link) {
                link.addEventListener("click", function () {
                    setOpen(false);
                    Array.prototype.forEach.call(
                        document.querySelectorAll(".nav-link"),
                        function (item) {
                            item.classList.remove("is-active");
                        }
                    );
                    link.classList.add("is-active");
                });
            }
        );
    }

    /* -------------------------------------------------------------------- toast */
    function wireToasts() {
        var toast = document.getElementById("toast");
        var toastTitle = document.getElementById("toast-title");
        var toastDesc = document.getElementById("toast-desc");
        var timer = null;

        if (!toast) {
            return;
        }

        function show(title, description) {
            if (toastTitle) {
                toastTitle.textContent = title || "";
            }
            if (toastDesc) {
                toastDesc.textContent = description || "";
            }
            toast.classList.add("is-visible");
            window.clearTimeout(timer);
            timer = window.setTimeout(function () {
                toast.classList.remove("is-visible");
            }, 3200);
        }

        document.addEventListener("click", function (event) {
            var trigger = event.target.closest("[data-toast-title]");
            if (!trigger) {
                return;
            }

            show(
                trigger.getAttribute("data-toast-title"),
                trigger.getAttribute("data-toast-desc")
            );

            // Links that navigate away: let the toast appear before leaving.
            var href = trigger.getAttribute("href");
            if (href && !href.startsWith("#")) {
                event.preventDefault();
                window.setTimeout(function () {
                    window.location.href = href;
                }, 350);
            }
        });
    }

    /* --------------------------------------------------------------------- init */
    function init() {
        buildCharts();
        wireTableFilter();
        wireSidebar();
        wireToasts();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
