# -*- coding: utf-8 -*-

from openerp import models, fields, api

class open_academy(models.Model):
    _name = 'open_academy.curso'

    name = fields.Char(string='Title',required=True)
    description = fields.Text('Description')
    
    _sql_constraints = [('name_unico','unique (name)','¡El nombre del recurso debe ser único!')]
