# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class Company(models.Model):
	_inherit = 'res.company'

	duration = fields.Float()
	event_duration = fields.Float()
	company_qr = fields.Text()
	company_refresh_time=fields.Float()
	company_pop_up_time = fields.Float()
	company_header_background = fields.Binary()
	company_general_background = fields.Binary()
	company_footer_background = fields.Binary()
	text_color_header = fields.Selection([
		('black','Negro'),
		('white','Blanco'),
		])
	text_color_general = fields.Selection([
		('black','Negro'),
		('white','Blanco'),
		])
	text_color_footer = fields.Selection([
		('black','Negro'),
		('white','Blanco'),
		])

	company_description=fields.Text(help="Para más información consulte este qr")

