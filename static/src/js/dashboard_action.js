/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onMounted, onWillStart, useState } from "@odoo/owl";

const COLOR_MAP = {
    "Văn học": "#2F5DA9",
    "Công nghệ": "#3F8F47",
    "Kinh tế": "#B85A28",
    "Thiếu nhi": "#E2AC34",
    "Ngoại ngữ": "#7B4BCB",
};

const DEMO_CATEGORIES = [
    { name: "Văn học", value: 35, color: "#2F5DA9" },
    { name: "Công nghệ", value: 25, color: "#3F8F47" },
    { name: "Kinh tế", value: 18, color: "#B85A28" },
    { name: "Thiếu nhi", value: 12, color: "#E2AC34" },
    { name: "Ngoại ngữ", value: 5, color: "#7B4BCB" },
];

export class LibraryDashboard extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.actionService = useService("action");
        this.state = useState({
            kpis: {},
            bookCategories: DEMO_CATEGORIES.map(c => ({...c})),
            loanTrend: { labels: [], borrowed: [], returned: [] },
            topBooks: [],
            latestLoans: [],
            latestReaders: [],
        });
        this.chartInstances = { doughnut: null, line: null };

        onWillStart(async () => {
            try {
                const data = await this.rpc("/library/dashboard/data", {});
                this.state.kpis = data.kpis || {};
                this.state.bookCategories = (data.bookCategories || []).map(cat => ({
                    ...cat,
                    color: COLOR_MAP[cat.name] || cat.color || "#999",
                }));
                this.state.loanTrend = data.loanTrend || { labels: [], borrowed: [], returned: [] };
                this.state.topBooks = data.topBooks || [];
                this.state.latestLoans = data.latestLoans || [];
                this.state.latestReaders = data.latestReaders || [];
                this.renderCharts();
            } catch (e) {
                console.error("QLTV Dashboard load error:", e);
            }
        });

        onMounted(() => {
            this.renderCharts();
        });
    }

    openAction(action) {
        this.actionService.doAction(action);
    }

    openBook() {
        this.actionService.doAction("QLTV.action_library_book");
    }

    openReader() {
        this.actionService.doAction("QLTV.action_library_reader");
    }

    openLoan() {
        this.actionService.doAction("QLTV.action_library_loan");
    }

    openBookCopy() {
        this.actionService.doAction("QLTV.action_library_book_copy");
    }

    openCategory() {
        this.actionService.doAction("QLTV.action_library_book_category");
    }

    renderCharts() {
        if (typeof Chart === "undefined") {
            console.warn("Chart.js không được nạp, vui lòng kiểm tra asset.");
            return;
        }
        this._renderDoughnutChart();
        this._renderLineChart();
    }

    _renderDoughnutChart() {
        const canvas = document.getElementById("dashboardDoughnutChart");
        if (!canvas) return;
        const data = this.state.bookCategories;
        if (!data.length) return;
        if (this.chartInstances.doughnut) {
            this.chartInstances.doughnut.destroy();
        }
        const ctx = canvas.getContext("2d");
        this.chartInstances.doughnut = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: data.map(item => item.name),
                datasets: [{
                    data: data.map(item => item.value),
                    backgroundColor: data.map(item => item.color),
                    borderColor: "#FFFFFF",
                    borderWidth: 4,
                    hoverBorderWidth: 4,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                cutout: "58%",
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const pct = total ? Math.round((value / total) * 100) : 0;
                                return `${context.label}: ${pct}%`;
                            },
                        },
                    },
                },
                animation: {
                    animateRotate: true,
                    easing: "easeOutQuart",
                },
                hover: {
                    mode: "nearest",
                    animationDuration: 200,
                },
                elements: {
                    arc: {
                        hoverOffset: 8,
                    },
                },
            },
        });
    }

    _renderLineChart() {
        const lineCanvas = document.getElementById("dashboardLineChart");

        if (lineCanvas && this.state.loanTrend.labels.length) {
            if (this.chartInstances.line) {
                this.chartInstances.line.destroy();
            }
            const lineCtx = lineCanvas.getContext("2d");
            this.chartInstances.line = new Chart(lineCtx, {
                type: "line",
                data: {
                    labels: this.state.loanTrend.labels,
                    datasets: [
                        {
                            label: "Đã mượn",
                            data: this.state.loanTrend.borrowed,
                            borderColor: "#7C3AED",
                            backgroundColor: "rgba(124, 58, 237, 0.16)",
                            pointBackgroundColor: "#7C3AED",
                            pointBorderColor: "#FFFFFF",
                            pointRadius: 5,
                            fill: true,
                            tension: 0.35,
                        },
                        {
                            label: "Đã trả",
                            data: this.state.loanTrend.returned,
                            borderColor: "#22C55E",
                            backgroundColor: "rgba(34, 197, 94, 0.16)",
                            pointBackgroundColor: "#22C55E",
                            pointBorderColor: "#FFFFFF",
                            pointRadius: 5,
                            fill: true,
                            tension: 0.35,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: { color: "#6B7280" },
                        },
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 10,
                                color: "#6B7280",
                            },
                            grid: {
                                color: "rgba(15, 23, 42, 0.05)",
                            },
                        },
                    },
                    plugins: {
                        legend: {
                            display: false,
                        },
                        tooltip: {
                            callbacks: {
                                label: (context) => `${context.dataset.label}: ${context.parsed.y}`,
                            },
                        },
                    },
                },
            });
        }
    }

    formatNumber(value) {
        return new Intl.NumberFormat("vi-VN").format(value || 0);
    }
}

LibraryDashboard.template = "QLTV.LibraryDashboard";
registry.category("actions").add("library_dashboard", LibraryDashboard);
