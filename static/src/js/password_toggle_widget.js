/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

class PasswordToggleField extends Component {
    setup() {
        this.state = useState({ showPassword: false });
    }

    get type() {
        return this.state.showPassword ? "text" : "password";
    }

    get iconClass() {
        return this.state.showPassword ? "fa fa-eye-slash" : "fa fa-eye";
    }

    togglePassword() {
        this.state.showPassword = !this.state.showPassword;
    }

    get currentValue() {
        return this.props.record.data[this.props.name] || "";
    }

    onInput(ev) {
        this.props.record.update({ [this.props.name]: ev.target.value });
    }
}

PasswordToggleField.template = "QLTV.PasswordToggleField";
PasswordToggleField.supportedTypes = ["char"];

registry.category("fields").add("password_toggle", PasswordToggleField);
