# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class Company(models.Model):
	_inherit = 'res.company'

	duration = fields.Float()
	event_duration = fields.Float()
	company_qr = fields.Text()
	company_description=fields.Text()