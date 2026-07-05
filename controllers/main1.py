from odoo import http
from odoo.addons.QLTV.controllers.main import MainController

class MainController2(MainController):

    @http.route(['/moutain','/vinh'],type='http', auth='public')
    def moutain_check(self):
        super(MainController2, self).moutain_check()
        return "inherited"
