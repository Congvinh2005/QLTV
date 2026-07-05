from odoo import models, fields


class DongNghiep(models.Model):
    _name = 'res.dongnghiep'
    _description = 'Đồng nghiệp'

    name = fields.Char(string='Tên', required=True)
