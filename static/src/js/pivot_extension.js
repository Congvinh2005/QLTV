/** @odoo-module **/

import { registry } from "@web/core/registry";
import { onWillStart, useState } from "@odoo/owl";
import { PivotController } from "@web/views/pivot/pivot_controller";
import "@web/views/pivot/pivot_view";

export class LibraryPivotController extends PivotController {
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
                    console.error("QLTV Dashboard pivot load error:", e);
                }
            });
        }
    }
}

LibraryPivotController.template = "QLTV.LibraryPivotView";

const pivotView = registry.category("views").get("pivot");
registry.category("views").add("pivot", {
    ...pivotView,
    Controller: LibraryPivotController,
}, { force: true });
