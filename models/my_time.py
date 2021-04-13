from odoo import models, fields, api, _, exceptions

import logging, re

class My_Time(models.Model):
	_name = 'my_time.my_time'

	OVERFLOW_HOUR_MESSAGE = 'Please, introduce an hour between [0:00, 23:59]h'

	initial_hour = fields.Float()
	final_hour = fields.Float()	

	@api.model 
	def is_in_hour_range(self, hour_to_analyse):
		if self.greater_lower_limit(hour_to_analyse):
			return self.greater_upper_limit(hour_to_analyse)

	def lower_upper_limit(self, hour_to_analyse):
		UPPER_LIMIT_HOUR_INTERVAL = 24.0
		return hour_to_analyse < UPPER_LIMIT_HOUR_INTERVAL

	def greater_lower_limit(self, hour_to_analyse):
		LOWER_LIMIT_HOUR_INTERVAL = 0.0
		return hour_to_analyse >= LOWER_LIMIT_HOUR_INTERVAL

	# Constrains
	@api.constrains('initial_hour', 'OVERFLOW_HOUR_MESSAGE')
	def _constrains_initial_hour_range(self):
		if self.is_in_hour_range(self.initial_hour):
			raise exceptions.ValidationError(_(self.OVERFLOW_HOUR_MESSAGE)) 
		pass

	@api.constrains('final_hour', 'OVERFLOW_HOUR_MESSAGE')
	def _constrains_final_hour_range(self):
		if self.is_in_hour_range(self.final_hour):
			raise exceptions.ValidationError(_(self.OVERFLOW_HOUR_MESSAGE)) 
		pass

	@api.constrains('final_hour', 'initial_hour')
	def _constrains_final_hour_range(self):
		INITIAL_HOUR_GREATER_THAN_FINAL_HOUR = 'Remember, always Initial Hour must be lower than Final Hour'
		if self.final_hour <= self.initial_hour:
			raise exceptions.ValidationError(_(INITIAL_HOUR_GREATER_THAN_FINAL_HOUR)) 
		pass