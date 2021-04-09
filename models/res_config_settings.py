# -*- coding: utf-8 -*-

from odoo import api, models, fields, _, exceptions


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	duration = fields.Float(string= _("Duration's slider"), related='company_id.duration', readonly=False)
	event_duration = fields.Float(string= _("Duration's event"), related='company_id.event_duration', readonly=False)
	company_qr = fields.Text(string=_("Company's url"), related='company_id.company_qr', readonly=False)
	company_description = fields.Text(
		string=_("Company's description"), 
		related='company_id.company_description',
		readonly=False)

	refresh_time = fields.Float(string=_("Refresh Time"),related='company_id.company_refresh_time', readonly=False)
	pop_up_time = fields.Float(string=_("Pop-up Time"),related='company_id.company_pop_up_time', readonly=False)
			
	@api.constrains('company_description')
	def _constrains_company_description(self):
		if len(self.company_description) > 100:
			raise exceptions.ValidationError(_("Límite de caracteres 75")) 
		pass
	@api.constrains('event_duration')
	def _constrains_event_duration(self):
		if self.event_duration < 0:
			raise exceptions.ValidationError(_("El valor debe ser al menos 0 o superior"))
		pass
	@api.constrains('duration')
	def _constrains_duration(self):
		if self.duration < 0:
			raise exceptions.ValidationError(_("El valor debe ser al menos 0 o superior"))
		pass
	@api.constrains('refresh_time')
	def _constrains_refresh_time(self):
		if self.refresh_time < 0:
			raise exceptions.ValidationError(_("El valor debe ser al menos 0 o superior"))
		pass
	@api.constrains('pop_up_time')
	def _constrains_pop_up_time(self):
		if self.pop_up_time < 0:
			raise exceptions.ValidationError(_("El valor debe ser al menos 0 o superior"))
		pass