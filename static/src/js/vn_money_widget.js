/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

class VnMoneyField extends Component {
    setup() {
        this.state = useState({
            hasFocus: false,
            displayValue: "",
        });
    }

    get formattedValue() {
        if (this.state.hasFocus) {
            return this.state.displayValue;
        }
        const value = this.props.record.data[this.props.name];
        if (!value) {
            return "0đ";
        }
        const num = Math.round(Number(value));
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".") + " đ";
    }

    onFocus() {
        this.state.hasFocus = true;
        const value = this.props.record.data[this.props.name];
        this.state.displayValue = value ? String(Math.round(Number(value))) : "";
    }

    onInput(ev) {
        const raw = ev.target.value.replace(/[^0-9]/g, "");
        this.state.displayValue = raw;
        this.props.record.update({ [this.props.name]: raw ? parseInt(raw, 10) : false });
    }

    onBlur() {
        this.state.hasFocus = false;
    }
}

VnMoneyField.template = "QLTV.VnMoneyField";
VnMoneyField.supportedTypes = ["monetary"];

registry.category("fields").add("vn_money", VnMoneyField);
