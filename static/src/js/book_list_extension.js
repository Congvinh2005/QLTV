/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListController } from "@web/views/list/list_controller";
import { onWillStart, useState } from "@odoo/owl";
import "@web/views/list/list_view";

export class LibraryListController extends ListController {
    setup() {
        super.setup();
        this.dashboardState = useState({
            kpis: {},
            modelName: this.props.resModel,
        });
        const model = this.props.resModel;
        if (model && model.startsWith("library.")) {
            onWillStart(async () => {
                const data = await this.rpc("/library/dashboard/data", {});
                this.dashboardState.kpis = data;
            });
        }
    }
}

LibraryListController.template = "QLTV.LibraryListView";

const listView = registry.category("views").get("list");
registry.category("views").add("list", {
    ...listView,
    Controller: LibraryListController,
}, { force: true });
