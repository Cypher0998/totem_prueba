# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
class Screen(models.Model):
	_name = 'screen.screen'

	name = fields.Char(string = _("Virtual Screen's Name"))
	description = fields.Text(string = _('Description'))
	userController = fields.Many2one('res.users')
	event_ids = fields.Many2many('totem_general.totem_general', string = _("Event List"))

