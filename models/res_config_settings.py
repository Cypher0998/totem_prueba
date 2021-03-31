# -*- coding: utf-8 -*-

from odoo import api, models, fields, _, exceptions


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	duration = fields.Float(string= _("Duration's slider"), default=10.00, related='company_id.duration', readonly=False)
	event_duration = fields.Float(string= _("Duration's event"), related='company_id.event_duration', readonly=False)
	company_qr = fields.Text(string=_("Company's url"), related='company_id.company_qr', readonly=False)
	company_description = fields.Text(
		string=_("Company's description"), 
		related='company_id.company_description',
		readonly=False)

	refresh_time = fields.Float(string=_("Refresh Time"),related='company_id.company_refresh_time', readonly=False)

	@api.multi
	def set_values(self):
		res = super(ResConfigSettings, self).set_values()
		param=self.env['ir.config_parameter'].sudo()
		param.set_param('totem_prueba.duration', self.duration)
		return res

	@api.model
	def get_values(self):
		res = super(ResConfigSettings, self).get_values()
		params = self.env['ir.config_parameter'].sudo()
		res.update(duration=float(params.get_param('totem_prueba.duration', 10.00)))
		return res

		

	@api.constrains('company_description')
	def _constrains_company_description(self):
		if len(self.company_description) > 50:
			raise exceptions.ValidationError(_("Límite de caracteres 50")) 
		pass
	@api.constrains('event_duration')
	def _constrains_event_duration(self):
		if self.event_duration < 1:
			raise exceptions.ValidationError(_("El valor debe ser mayor a 1"))
		pass
	@api.constrains('duration')
	def _constrains_duration(self):
		if self.duration < 1:
			raise exceptions.ValidationError(_("El valor debe ser mayor a 1"))
		pass
	@api.constrains('refresh_time')
	def _constrains_refresh_time(self):
		if self.refresh_time < 1:
			raise exceptions.ValidationError(_("El valor debe ser mayor a 1"))
		pass