/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onMounted, onWillStart, useState } from "@odoo/owl";

export class LibraryDashboard extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.actionService = useService("action");
        this.state = useState({
            kpis: {},
            bookCategories: [],
            loanTrend: { labels: [], borrowed: [], returned: [] },
            topBooks: [],
            latestLoans: [],
            latestReaders: [],
        });
        this.chartInstances = { pie: null, line: null };

        onWillStart(async () => {
            try {
                const data = await this.rpc("/library/dashboard/data", {});
                this.state.kpis = data.kpis || {};
                this.state.bookCategories = data.bookCategories || [];
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

    renderCharts() {
        if (typeof Chart === "undefined") {
            console.warn("Chart.js không được nạp, vui lòng kiểm tra asset.");
            return;
        }
        const pieCanvas = document.getElementById("dashboardPieChart");
        const lineCanvas = document.getElementById("dashboardLineChart");

        if (pieCanvas && this.state.bookCategories.length) {
            if (this.chartInstances.pie) {
                this.chartInstances.pie.destroy();
            }
            const pieCtx = pieCanvas.getContext("2d");
            const pieData = {
                labels: this.state.bookCategories.map((item) => item.name),
                datasets: [{
                    data: this.state.bookCategories.map((item) => item.value),
                    backgroundColor: this.state.bookCategories.map((item) => item.color),
                    borderColor: "#FFFFFF",
                    borderWidth: 2,
                }],
            };
            this.chartInstances.pie = new Chart(pieCtx, {
                type: "pie",
                data: pieData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false,
                        },
                        tooltip: {
                            callbacks: {
                                label: (context) => {
                                    const value = context.parsed || 0;
                                    const total = context.dataset.data.reduce((sum, item) => sum + item, 0);
                                    const percent = total ? Math.round((value / total) * 100) : 0;
                                    return `${context.label}: ${value} (${percent}%)`;
                                },
                            },
                        },
                    },
                },
            });
        }

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
        return new Intl.NumberFormat("en-US").format(value || 0);
    }
}

LibraryDashboard.template = "QLTV.LibraryDashboard";
registry.category("actions").add("library_dashboard", LibraryDashboard);
