from odoo import models, fields, api, _, exceptions

import logging, re

class My_Date(models.Model):
	_name = 'my_date.my_date'

	date = fields.Date(string = _('Day'))
	hour_set = fields.Many2many('my_time.my_time', string = _("Available Hour Set"))
	assigned_event = fields.Many2one('totem_general.totem_general', string = _("My Assigned Event"))	