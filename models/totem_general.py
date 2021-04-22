# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
from urllib.request import urlopen
from xml.etree.ElementTree import parse
from xml.dom import minidom
import logging, re

_logger=logging.getLogger(__name__)

class totem_general(models.Model):
	_inherit = 'event.event'

	# CONSTANT VARS
	CHARACTER_BOUNDARY_MESSAGE = 'Límite de caracteres '
	NORMAL_LIMIT_CHARACTER = 80
	EXTENSE_LIMIT_CHARACTER = 250
	DESCRIPTION_LIMIT_CHARACTER = 800

	# Display selector
	selector_display = fields.Selection([
		('web','Solo Web'),
		('totem','Solo Totem'),
		('web_totem',"Web y Totem")],
		string = _('Display Type'), default = 'web_totem')
	# General fields
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
	my_event_dates = fields.One2many('my_date.my_date', 'assigned_event',  string = _("Event Date Set"))

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
		TRUE = True
		TWENTY_FOR = 24
		THIRTY = 30

		if self.banner_video is TRUE:
			if not re.search(BAD_EMBED, self.banner_video):
				self.banner_video = self.banner_video[:TWENTY_FOR] + EMBED + self.banner_video[TWENTY_FOR:]
			if re.search(BAD_WATCH,self.banner_video):
				self.banner_video = self.banner_video.replace(CORRECT_WATCH, SLASH)
			self.video_id = self.banner_video[THIRTY:]
		pass


	@api.model
	def get_events_by_screen(self,uid):
		events_id = self.env['screen.screen'].search_read([('userController','=',uid)])
		user_events = []

		if len(events_id) > 0:
			user_events= self.env['event.event'].search_read([('id','in',events_id[0]['event_ids'])],
				['name','description','banner_url','banner_video','banner_rss','selector_banner',
				'video_id','image_ids','my_event_dates','pop_up_product_name',
				'pop_up_description','pop_up_qr_url'])
			
			for i in user_events:
				if i['selector_banner']=='rss':
					banner_playlist = self.parse_rss_video_ids(self.get_RSS_data(i['banner_rss']))
					i['banner_rss'] = banner_playlist
				if i['my_event_dates']!='':
					i['my_event_dates']=self.date_Time_Process(i['my_event_dates'])		

		return user_events

	def get_RSS_data(self,RSS_url):
		get_XML_from_url = urlopen(RSS_url)
		data_from_XML = minidom.parse(get_XML_from_url)
		return self.obtain_rss_video_ids(data_from_XML)
		


	def obtain_rss_video_ids(self,RSS_data):
		media=[]
		iterador = 0

		for i in RSS_data.getElementsByTagName('media:content'):
			id_video = str(i.attributes['url'].value)
			id_video = id_video.replace('?version=3','')
			id_video = id_video.replace('https://www.youtube.com/v/','')
			
			media.append(id_video)
			iterador+=1

		return media

	def date_Time_Process(self,fecha):
		FechasEmision = self.env['my_date.my_date'].search_read([('id','in',fecha)],['date','hour_set','final_date'])
		for diaEmision in FechasEmision:
			RangoHoras=self.env['my_time.my_time'].search_read([('id','in',diaEmision['hour_set'])],['initial_hour','final_hour'])
			for hora in RangoHoras:
				hora['initial_hour'] = self.convert_To_Seconds(hora['initial_hour'])
				hora['final_hour'] = self.convert_To_Seconds(hora['final_hour'])
				diaEmision['hour_set'][RangoHoras.index(hora)]=hora

		return FechasEmision

	def convert_To_Seconds(self,time):
		Hour=str(time).rsplit('.',1)[0]
		Min=str(time).rsplit('.',1)[1]
		if len(Min)<=1:
			Min=str(Min)+"0"
		min_to_milsec=int(Min)*60*1000
		hour_to_milsec=int(Hour)*60*60*1000

		return hour_to_milsec + min_to_milsec
		


	def parse_rss_video_ids(self,ids_list):
		final_string = "https://www.youtube.com/embed/"

		final_string += ids_list[0] + "?autoplay=1&mute=1&controls=0&rel=0&loop=1&playlist="

		for iterator_list in ids_list:
			final_string += iterator_list + ','

		final_string = final_string[:-1]
		return final_string

	def is_filled(self, element):
		return bool(element)

	@api.constrains('name', 'CHARACTER_BOUNDARY', 'NORMAL_LIMIT_CHARACTER')
	def _constrains_name(self):
		if len(self.name) > self.NORMAL_LIMIT_CHARACTER:
			raise exceptions.ValidationError(
				_(self.CHARACTER_BOUNDARY + self.NORMAL_LIMIT_CHARACTER))
		pass


	@api.constrains('pop_up_qr_url', 'CHARACTER_BOUNDARY','EXTENSE_LIMIT_CHARACTER')
	def _constrains_pop_up_url(self): 
		if len(self.pop_up_qr_url) > self.EXTENSE_LIMIT_CHARACTER:
			raise exceptions.ValidationError(
				_(self.CHARACTER_BOUNDARY + 
					self.EXTENSE_LIMIT_CHARACTER)) 
		pass

	@api.constrains('pop_up_product_name', 'CHARACTER_BOUNDARY', 'NORMAL_LIMIT_CHARACTER')
	def _constrains_pop_up_name(self):  
		if len(self.pop_up_product_name) > self.NORMAL_LIMIT_CHARACTER:
			raise exceptions.ValidationError(
				_(self.CHARACTER_BOUNDARY_MESSAGE + 
					self.NORMAL_LIMIT_CHARACTER)) 
		pass




