# -*- coding: utf-8 -*-

from odoo import models, fields, api

class image(models.Model):
	_name = 'image.image'

	name = fields.Char()
	my_image = fields.Binary()

