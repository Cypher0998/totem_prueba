# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class totem_general(models.Model):
	_name = 'totem_general.totem_general'

	name = fields.Char(string = _('Name'))
	banner = fields.Binary(string = _('Banner'))
	description = fields.Text(string = _('Description'))
	event_url = fields.Text(string = _('Event url'))
	banner_url = fields.Text()
	banner_video = fields.Text()
	banner_rss = fields.Text()
	selector_banner = fields.Selection([
		('video','Video'),
		('pic','Imagen'),
		('rss','RSS')], 
		string = _('Type banner selector'))
	
	initial_event_datetime = fields.Datetime()
	final_event_datetime = fields.Datetime()

	image_ids = fields.Many2many('image.image', string = _("Images slider"))



	@api.constrains('description')
	def _constrains_description(self):
		if len(self.description) > 250:
			raise exceptions.ValidationError(_("Límite de caracteres 250")) 
		pass
	@api.constrains('name')
	def _constrains_name(self):
		if len(self.name) > 30:
			raise exceptions.ValidationError(_("Límite de caracteres 80"))
		pass

	@api.onchange('event_url','banner_url')
	def _onchange_field_name(self):
		if self.event_url:
			self.banner_url = self.event_url
