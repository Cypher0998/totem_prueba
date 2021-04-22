from odoo import models, fields, api, _, exceptions
from datetime import datetime
import logging, re

class My_Date(models.Model):
	_name = 'my_date.my_date'

	actual_date = datetime.now()

	date = fields.Date(string = _('Initial Date'))
	final_date=fields.Date(string=_('Final Date'))
	hour_set = fields.Many2many('my_time.my_time', string = _("Available Hour Set"))
	assigned_event = fields.Many2one('event.event', string = _("My Assigned Event"))

	@api.model
	def is_filled(self, element):
		return bool(element)

	@api.onchange('date','final_date','actual_date')
	def on_change_default_final_date(self): 
		if not self.is_filled(self.final_date):
			self.final_date = self.date


	@api.onchange('date','actual_date')
	def on_change_default_initial_date(self):
		if not self.is_filled(self.date):
			self.date=self.actual_date.date()	