/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class KanbanStatsHeader extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.state = useState({ stats: {} });
        onWillStart(async () => {
            this.state.stats = await this.rpc("/library/kanban/stats", {
                model: this.props.model,
            });
        });
    }

    get cards() {
        return this.state.stats;
    }
}

KanbanStatsHeader.template = "QLTV.KanbanStatsHeader";

registry.category("kanban_widgets").add("kanban_stats", KanbanStatsHeader);
