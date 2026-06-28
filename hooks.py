from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    currency = env["res.currency"].search([("name", "=", "VND")], limit=1)
    if not currency:
        company = env["res.company"].search([], limit=1)
        currency = company.currency_id if company else env["res.currency"].search([], limit=1)
    if currency:
        env["library.loan"].search([("currency_id", "=", False)]).write({"currency_id": currency.id})
    # Cấu hình VND: 0 số thập phân, hiển thị "đ" phía sau
    vnd = env["res.currency"].search([("name", "=", "VND")], limit=1)
    if vnd:
        vnd.write({
            "decimal_places": 0,
            "position": "after",
        })
