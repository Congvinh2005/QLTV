#!/usr/bin/env bash
set -euo pipefail

ODOO_DIR="${ODOO_DIR:-/Users/vinhdv/odoo-dev/odoo16}"
ODOO_PYTHON="${ODOO_PYTHON:-/Users/vinhdv/miniconda3/envs/odoo16/bin/python}"
ODOO_CONFIG="${ODOO_CONFIG:-$HOME/.odoo/odoo16.conf}"
ODOO_DB="${ODOO_DB:-odoo16_db}"
MODULE_NAME="${MODULE_NAME:-QLTV}"

cd "$ODOO_DIR"

"$ODOO_PYTHON" odoo-bin \
    -c "$ODOO_CONFIG" \
    -d "$ODOO_DB" \
    -u "$MODULE_NAME" \
    --stop-after-init
