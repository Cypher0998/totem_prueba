# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
from urllib.request import urlopen
from xml.etree.ElementTree import parse
from xml.dom import minidom
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

		if self.banner_video is True:
			if not re.search(BAD_EMBED, self.banner_video):
				self.banner_video = self.banner_video[:24] + EMBED + self.banner_video[24:]
			if re.search(BAD_WATCH,self.banner_video):
				self.banner_video = self.banner_video.replace(CORRECT_WATCH, SLASH)
			self.video_id = self.banner_video[30:]
		pass


	@api.model
	def get_events_by_screen(self,uid):

		events_id = self.env['screen.screen'].search_read([('userController','=',uid)])
		user_events= self.env['totem_general.totem_general'].search_read([('id','in',events_id[0]['event_ids'])],
			['name','description','banner_url','banner_video','banner_rss','selector_banner',
			'video_id','image_ids','initial_event_datetime','final_event_datetime','pop_up_product_name',
			'pop_up_description','pop_up_qr_url'])

		for i in user_events:
			if i['selector_banner']=='rss':
				banner_playlist = self.parse_rss_video_ids(self.get_RSS_data(i['banner_rss']))
				# _logger.info(banner_playlist + " 500")
				i['banner_rss'] = banner_playlist
				# _logger.info(i['banner_rss'] + " 500")

		_logger.info(str(user_events[0]['banner_rss']) + " 500")

				

		return user_events

	def get_RSS_data(self,RSS_url):
		get_XML_from_url = urlopen(RSS_url)
		data_from_XML = minidom.parse(get_XML_from_url)
		return self.obtain_rss_video_ids(data_from_XML)
		pass


	def obtain_rss_video_ids(self,RSS_data):
		media=[]
		iterador = 0

		for i in RSS_data.getElementsByTagName('media:content'):
			id_video = str(i.attributes['url'].value)
			id_video = id_video.replace('?version=3','')
			id_video = id_video.replace('https://www.youtube.com/v/','')
			
			media.append(id_video)
			# _logger.info(media[iterador] + " 500")
			iterador+=1

		return media
		pass

	def parse_rss_video_ids(self,ids_list):
		final_string = "https://www.youtube.com/embed/"

		final_string += ids_list[0] + "?autoplay=1&mute=1&controls=0&rel=0&loop=1&playlist="

		# _logger.info(final_string + " 500")

		for iterator_list in ids_list:
			final_string += iterator_list + ','

		final_string = final_string[:-1]
		# _logger.info(final_string + " 500")
		return final_string

	

	@api.constrains('description')
	def _constrains_description(self):
		CHARACTER_BOUNDARY = 'Límite de caracteres '
  
		if len(self.description) > 250:
			raise exceptions.ValidationError(_(CHARACTER_BOUNDARY + '250')) 
		pass

	@api.constrains('name')
	def _constrains_name(self):
		CHARACTER_BOUNDARY = 'Límite de caracteres '
		if len(self.name) > 80:
			raise exceptions.ValidationError(_(CHARACTER_BOUNDARY + '80'))
		pass

	# @api.constrains('pop_up_description')
	# def _constrains_description(self):
	# 	CHARACTER_BOUNDARY = 'Límite de caracteres '
  
	# 	if len(self.description) > 400:
	# 		raise exceptions.ValidationError(_(CHARACTER_BOUNDARY + '400')) 
	# 	pass

	@api.constrains('pop_up_qr_url')
	def _constrains_description(self):
		CHARACTER_BOUNDARY = 'Límite de caracteres '
  
		if len(self.description) > 250:
			raise exceptions.ValidationError(_(CHARACTER_BOUNDARY + '250')) 
		pass

	@api.constrains('pop_up_product_name')
	def _constrains_description(self):
		CHARACTER_BOUNDARY = 'Límite de caracteres '
  
		if len(self.description) > 80:
			raise exceptions.ValidationError(_(CHARACTER_BOUNDARY + '80')) 
		pass




