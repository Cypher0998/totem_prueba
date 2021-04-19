# -*- coding: utf-8 -*-

from odoo import api, models, fields, _, exceptions


from . import utilities


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	OVERFLOW_TIME_MESSAGE = "El valor debe ser al menos 0 o superior"
	CHARACTER_BOUNDARY_MESSAGE = 'Límite de caracteres '
	NORMAL_LIMIT_CHARACTER = 100
	DEFAULT_DESCRIPTION_MESSAGE = 'Si desea reservar su propio espacio publicitario, contacte con Bakata Solutions, S.L'

	duration = fields.Float(
		string= _("Duration's slider"), 
		related='company_id.duration', 
		readonly=False, digits=(3, 0))
	event_duration = fields.Float(
		string= _("Duration's event"), 
		related='company_id.event_duration', 
		readonly=False, digits=(3, 0))

	company_qr = fields.Text(string=_("Company's url"), related='company_id.company_qr', readonly=False)
	company_description = fields.Text(
		string=_("Company's description"), 
		related='company_id.company_description',
		readonly=False)

	refresh_time = fields.Float(
		string=_("Refresh Time"),
		related='company_id.company_refresh_time',
		readonly=False, digits=(3, 0))
	pop_up_time = fields.Float(
		string=_("Pop-up Time"),
		related='company_id.company_pop_up_time',
		readonly=False, digits=(3, 0))

	header_background = fields.Binary(related = 'company_id.company_header_background', readonly=False)
	general_background = fields.Binary(related = 'company_id.company_general_background', readonly=False)
	footer_background = fields.Binary(related = 'company_id.company_footer_background', readonly=False)
	text_color_header = fields.Selection([
		('black','Negro'),
		('white','Blanco'),
		],
		related='company_id.text_color_header', readonly=False, string=_("Header's Text Color"))

	text_color_general = fields.Selection([
		('black','Negro'),
		('white','Blanco'),
		],
		related='company_id.text_color_general', readonly=False, string=_("General's Text Color"))

	text_color_footer = fields.Selection([
		('black','Negro'),
		('white','Blanco'),
		],
		related='company_id.text_color_footer', readonly=False, string=_("Footer's Text Color"))

	@api.model
	def is_filled(self, element):
		return bool(element)

	@api.onchange('company_description', 'DEFAULT_DESCRIPTION_MESSAGE')
	def on_change_default_company_description(self): 
		if not self.is_filled(self.company_description):
			self.company_description = self.DEFAULT_DESCRIPTION_MESSAGE

	@api.onchange('duration')
	def on_change_default_duration(self): 
		if not self.is_filled(self.duration):
			self.duration = 4

	@api.onchange('event_duration')
	def on_change_default_initial_hour(self): 
		if not self.is_filled(self.event_duration):
			self.event_duration = 10

	@api.onchange('refresh_time')
	def on_change_default_refresh_time(self): 
		if not self.is_filled(self.refresh_time):
			self.refresh_time = 15
	
	@api.onchange('pop_up_time')
	def on_change_default_pop_up_time(self): 
		if not self.is_filled(self.pop_up_time):
			self.pop_up_time = 10


	@api.constrains('company_description', 'NORMAL_LIMIT_CHARACTER', 'CHARACTER_BOUNDARY_MESSAGE')
	def _constrains_company_description(self):
		if self.is_filled(self.company_description):
			if len(self.company_description) > self.NORMAL_LIMIT_CHARACTER:
				raise exceptions.ValidationError(_(self.CHARACTER_BOUNDARY_MESSAGE +
				 self.NORMAL_LIMIT_CHARACTER)) 
		pass
	@api.constrains('event_duration', 'OVERFLOW_TIME_MESSAGE')
	def _constrains_event_duration(self):
		if self.event_duration < 0:
			raise exceptions.ValidationError(_(self.OVERFLOW_TIME_MESSAGE))
		pass
	@api.constrains('duration', 'OVERFLOW_TIME_MESSAGE')
	def _constrains_duration(self):
		if self.duration < 0:
			raise exceptions.ValidationError(_(self.OVERFLOW_TIME_MESSAGE))
		pass
	@api.constrains('refresh_time', 'OVERFLOW_TIME_MESSAGE')
	def _constrains_refresh_time(self):
		if self.refresh_time < 0:
			raise exceptions.ValidationError(_(self.OVERFLOW_TIME_MESSAGE))
		pass
	@api.constrains('pop_up_time', 'OVERFLOW_TIME_MESSAGE')
	def _constrains_pop_up_time(self):
		if self.pop_up_time < 0:
			raise exceptions.ValidationError(_(self.OVERFLOW_TIME_MESSAGE))
		pass