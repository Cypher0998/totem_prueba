# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging, re

_logger=logging.getLogger(__name__)

class totem_general(models.Model):

	_name = 'totem_general.totem_general'

	# General fields
	name = fields.Char(string = _('Name'))
	banner = fields.Binary(string = _('Banner'))
	description = fields.Text(string = _('Description'))
	
	banner_url = fields.Text(string =_("Banner Url's QR"))
	banner_video = fields.Text()
	banner_rss = fields.Text()
	selector_banner = fields.Selection([
		('video','Video'),
		('pic','Imagen'),
		('rss','RSS')], 
		string = _('Type Banner'))
		
	video_id = fields.Text()

	# Image Slider Page field
	image_ids = fields.Many2many('image.image', string = _("Images slider"))


	# Event's date Page fields
	initial_event_datetime = fields.Datetime(string = _("Initial Date"))
	final_event_datetime = fields.Datetime(string = _("Final Date"))

	# Pop Up's Information fields
	pop_up_product_name = fields.Text(string = _('Product name'))
	pop_up_image = fields.Binary(string = _('Pop-up Image'))
	pop_up_description = fields.Text(string = _('Description'))
	pop_up_qr_url = fields.Text(string = _('Pop-up QR'))


	@api.onchange('banner_video', 'video_id')
	def _onchange_(self):
		SLASH = '/'		
		EMBED ='embed' + SLASH
		BAD_EMBED = SLASH + EMBED
		WATCH = 'watch'
		QUESTION_MARK = '?'
		V_EQUAL = 'v='
		SPECIAL_WATCH_EXTENSION = '\?v\='
		BAD_WATCH = SLASH + WATCH + SPECIAL_WATCH_EXTENSION
		CORRECT_WATCH = SLASH + WATCH + QUESTION_MARK + V_EQUAL

		print ("\n\n\n\n")
		print (type(BAD_EMBED))
		print ("\n\n\n\n")
		if not re.search(BAD_EMBED, self.banner_video):
			self.banner_video = self.banner_video[:24] + EMBED + self.banner_video[24:]
		if re.search(BAD_WATCH,self.banner_video):
			self.banner_video = self.banner_video.replace(CORRECT_WATCH, SLASH)
		self.video_id = self.banner_video[30:]
		pass



	@api.constrains('description')
	def _constrains_description(self):
		CHARACTER_BOUNDARY = 'Límite de caracteres '
  
		if len(self.description) > 200:
			raise exceptions.ValidationError(_(CHARACTER_BOUNDARY + '250')) 
		pass
	@api.constrains('name')
	def _constrains_name(self):
		CHARACTER_BOUNDARY = 'Límite de caracteres '
		if len(self.name) > 30:
			raise exceptions.ValidationError(_(CHARACTER_BOUNDARY + '80'))
		pass

	@api.onchange('event_url','banner_url')
	def _onchange_field_name(self):
		if self.event_url:
			self.banner_url = self.event_url
