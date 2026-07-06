/** @odoo-module **/

import { registry } from "@web/core/registry";
import { onWillStart, useState } from "@odoo/owl";
import { GraphController } from "@web/views/graph/graph_controller";
import "@web/views/graph/graph_view";

export class LibraryGraphController extends GraphController {
    setup() {
        super.setup();
        this.dashboardState = useState({
            kpis: {},
            modelName: this.props.resModel,
        });
        const model = this.props.resModel;
        if (model && ["library.book", "library.reader", "library.loan"].includes(model)) {
            onWillStart(async () => {
                try {
                    const data = await this.env.services.rpc("/library/dashboard/data", {});
                    this.dashboardState.kpis = data.kpis;
                } catch (e) {
                    console.error("QLTV Dashboard graph load error:", e);
                }
            });
        }
    }
}

LibraryGraphController.template = "QLTV.LibraryGraphView";

const graphView = registry.category("views").get("graph");
registry.category("views").add("graph", {
    ...graphView,
    Controller: LibraryGraphController,
}, { force: true });
