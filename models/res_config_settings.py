# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	duration = fields.Float(string= _("Duration's slider"), related='company_id.duration', readonly=False)
	event_duration = fields.Float(string= _("Duration's event"), related='company_id.event_duration', readonly=False)
	company_qr = fields.Text(string=_("Company's url"), related='company_id.company_qr', readonly=False)
	company_description=fields.Text(string=_("Company's description"), related='company_id.company_description', readonly=False)

	# @api.constrains('company_description')
	# def _constrains_company_description(self):
	# 	if len(self.company_description) > 500:
	# 		raise exceptions.ValidationError(_("Límite de caracteres 500")) 
	# 	pass
