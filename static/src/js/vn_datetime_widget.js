/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class VnDatetimeField extends Component {
    get formattedValue() {
        const value = this.props.record.data[this.props.name];
        if (!value) return "";
        const dt = new Date(value);
        const dd = String(dt.getDate()).padStart(2, "0");
        const MM = String(dt.getMonth() + 1).padStart(2, "0");
        const yyyy = dt.getFullYear();
        const HH = String(dt.getHours()).padStart(2, "0");
        const mm = String(dt.getMinutes()).padStart(2, "0");
        const ss = String(dt.getSeconds()).padStart(2, "0");
        return `${HH}:${mm}:${ss} ${dd}/${MM}/${yyyy}`;
    }
}

VnDatetimeField.template = "QLTV.VnDatetimeField";
VnDatetimeField.supportedTypes = ["datetime", "date"];

registry.category("fields").add("vn_datetime", VnDatetimeField);
