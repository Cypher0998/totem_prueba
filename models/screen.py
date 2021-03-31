# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class totem_general(models.Model):
	_name = 'screen.screen'

	name = fields.Char(string = _("Virtual Screen's Name"))
	description = fields.Text(string = _('Description'))

	event_ids = fields.Many2many('totem_general.totem_general', string = _("Event List"))

