# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
class Screen(models.Model):
	_name = 'screen.screen'

	name = fields.Char(string = _("Virtual Screen's Name"))
	description = fields.Text(string = _('Description'))
	userController = fields.Many2one('res.users', string =("Usuario"))
	event_ids = fields.Many2many('event.event', string = _("Event List"))

