/** @odoo-module **/

import { registry } from "@web/core/registry";
import { onWillStart, useState } from "@odoo/owl";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import "@web/views/kanban/kanban_view";

export class LibraryKanbanController extends KanbanController {
    setup() {
        super.setup();
        this.dashboardState = useState({
            kpis: {},
            modelName: this.props.resModel,
        });
        const model = this.props.resModel;
        if (model && model.startsWith("library.")) {
            onWillStart(async () => {
                try {
                    const data = await this.env.services.rpc("/library/dashboard/data", {});
                    this.dashboardState.kpis = data.kpis;
                } catch (e) {
                    console.error("QLTV Dashboard kanban load error:", e);
                }
            });
        }
    }
}

LibraryKanbanController.template = "QLTV.LibraryKanbanView";

const kanbanView = registry.category("views").get("kanban");
registry.category("views").add("kanban", {
    ...kanbanView,
    Controller: LibraryKanbanController,
}, { force: true });
