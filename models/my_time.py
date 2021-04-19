from odoo import models, fields, api, _, exceptions

import logging, re

_logger = logging.getLogger(__name__)
class My_Time(models.Model):
	_name = 'my_time.my_time'

	OVERFLOW_HOUR_MESSAGE = 'Please, introduce an hour between [0:00, 23:59]h'

	initial_hour = fields.Float(digits=(2, 2), default = 0)
	final_hour = fields.Float(digits=(2, 2), default = 0)	

	@api.model
	def is_in_hour_range(self, my_hour):
		return my_hour >= 0 and my_hour < 24

	def is_filled(self, element):
		return bool(element)

	@api.onchange('initial_hour')
	def on_change_default_initial_hour(self): 
		if not self.is_filled(self.initial_hour):
			self.initial_hour = 0

	@api.onchange('final_hour')
	def on_change_default_final_hour(self): 
		if not self.is_filled(self.final_hour):
			self.final_hour = 23.59


	# Constrains
	@api.constrains('initial_hour', 'OVERFLOW_HOUR_MESSAGE')
	def _constrains_initial_hour_range(self):
		if not self.is_in_hour_range(self.initial_hour):
			raise exceptions.ValidationError(_(self.OVERFLOW_HOUR_MESSAGE)) 
		pass

	@api.constrains('final_hour', 'OVERFLOW_HOUR_MESSAGE')
	def _constrains_final_hour_range(self):
		if not self.is_in_hour_range(self.final_hour):
			raise exceptions.ValidationError(_(self.OVERFLOW_HOUR_MESSAGE)) 
		pass

	@api.constrains('final_hour', 'initial_hour')
	def _constrains_final_hour_range(self):
		INITIAL_HOUR_GREATER_THAN_FINAL_HOUR = 'Remember, always Initial Hour must be lower than Final Hour'
		if self.is_filled(self.final_hour) and self.is_filled(self.initial_hour):
			if self.final_hour <= self.initial_hour:
				raise exceptions.ValidationError(_(INITIAL_HOUR_GREATER_THAN_FINAL_HOUR)) 
		pass
