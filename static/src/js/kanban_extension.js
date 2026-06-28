/** @odoo-module **/

import { registry } from "@web/core/registry";
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { useService } from "@web/core/utils/hooks";
import { onWillStart, useState } from "@odoo/owl";

export class LibraryKanbanRenderer extends KanbanRenderer {
    setup() {
        super.setup();
        this.state = useState({ stats: {} });
        const model = this.props.list?.model?.resModel;
        if (model && model.startsWith("library.")) {
            this.rpc = useService("rpc");
            onWillStart(async () => {
                this.state.stats = await this.rpc("/library/kanban/stats", { model });
            });
        }
    }

    get statCards() {
        const s = this.state.stats;
        return Object.entries(s).map(([key, value]) => ({
            key,
            value,
            label: this._label(key),
        }));
    }

    _label(key) {
        const labels = {
            total: "Tổng",
            available: "Có sẵn",
            borrowed: "Đang mượn",
            out_of_stock: "Hết sách",
            borrowing: "Đang mượn",
            overdue: "Quá hạn",
            returned: "Đã trả",
        };
        return labels[key] || key;
    }
}

LibraryKanbanRenderer.template = "QLTV.LibraryKanbanRenderer";

const kanbanView = registry.category("views").get("kanban");
registry.category("views").add("kanban", {
    ...kanbanView,
    Renderer: LibraryKanbanRenderer,
}, { force: true });
