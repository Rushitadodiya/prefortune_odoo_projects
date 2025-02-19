# -*- coding: utf-8 -*-
# from odoo import http


# class OneSignalApp(http.Controller):
#     @http.route('/one_signal_app/one_signal_app', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/one_signal_app/one_signal_app/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('one_signal_app.listing', {
#             'root': '/one_signal_app/one_signal_app',
#             'objects': http.request.env['one_signal_app.one_signal_app'].search([]),
#         })

#     @http.route('/one_signal_app/one_signal_app/objects/<model("one_signal_app.one_signal_app"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('one_signal_app.object', {
#             'object': obj
#         })

