# -*- coding: utf-8 -*-
# from odoo import http

# class TotemPrueba(http.Controller):
#     @http.route('/totem_prueba', auth = 'public', website = True)
#     # @http.route('/totem_prueba/totem_prueba/', auth='public')
#     def index(self, **kw):
#         return http.request.render('totem_prueba.index', {})

#     @http.route('/totem_prueba/objects/', auth='public', website = True)
#     def list(self, **kw):
#         return http.request.render('totem_prueba.assets_frontend', {
#             'root': '/totem_prueba',
#             'objects': http.request.env['totem_prueba.totem_prueba'].search([]),
#         })

#     @http.route('/totem_prueba/totem_prueba/objects/<model("totem_prueba.totem_prueba"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('totem_prueba.object', {
#             'object': obj
#         })