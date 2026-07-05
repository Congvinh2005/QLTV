import json
import werkzeug
from odoo import http
from odoo.http import request

class MainController(http.Controller):

    @http.route('/moutain', type='http', auth='public')
    def moutain_check(self):
        return "Moutain check route"
    
    
    # @http.route('/moutain/<int:id>', type='http', auth='public')
    # def moutain_check_id(self, id):
    #     return "Mountain check route with %s" % str(id)

    # @http.route('/moutain', type='http', auth='public')
    # def moutain_check(self):
    #     return werkzeug.utils.redirect('https://www.facebook.com/')

    # @http.route('/moutain', type='http', auth='public')
    # def moutain_check(self):
    #     return werkzeug.utils.redirect('/web/login')

    # @http.route('/moutain', type='http', auth='public')
    # def moutain_check(self):
    #     return json.dumps({
    #         "name": "Hệ thống quản lý thư viện",
    #         "summary": "Quản lý sách, bạn đọc, mượn trả, bảng điều khiển và báo cáo.",
    #         "version": "2",
    #         "check": "ok"
    #     })

    # @http.route('/moutain', type='http', auth='public')
    # def moutain_check(self):
    #     partner = request.env['res.dongnghiep'].sudo().create({
    #         'name': 'Nguyen Van A',
    #     })
    #     return "Partner has been created with ID: %s" % str(partner.name)
    
    
