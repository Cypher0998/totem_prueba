# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class totem_general(models.Model):
	_name = 'totem_general.totem_general'

	name = fields.Char()
	banner = fields.Binary()
	description = fields.Text()
	event_url = fields.Text()
	

	image_ids = fields.Many2many('image.image', string = _("Images slider"))

	# @api.constrains('description')
	# def _constrains_description(self):
	# 	if len(self.description) > 500:
	# 		raise exceptions.ValidationError(_("Límite de caracteres 500")) 
	# 	pass
	# @api.constrains('name')
	# def _constrains_name(self):
	# 	if len(self.name) > 80:
	# 		raise exceptions.ValidationError(_("Límite de caracteres 80"))
	# 	pass


