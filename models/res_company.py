# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class Company(models.Model):
	_inherit = 'res.company'

	duration = fields.Float()
	event_duration = fields.Float()
	company_qr = fields.Text()
	company_refresh_time=fields.Float()
	company_pop_up_time = fields.Float()

	@api.model
	def _get_default_company_description(self): 
		return "Para más información consulte este qr"

	company_description=fields.Text(help="Para más información consulte este qr")


