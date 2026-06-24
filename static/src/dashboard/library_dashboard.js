/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

export class LibraryDashboard extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.state = useState({
            kpis: {},
        });

        onWillStart(async () => {
            this.state.kpis = await this.rpc("/library/dashboard/data", {});
        });
    }
}

LibraryDashboard.template = "QLTV.LibraryDashboard";

registry.category("actions").add("library_dashboard", LibraryDashboard);
