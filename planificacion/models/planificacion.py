# -*- coding: utf-8 -*-

from openerp import models, fields, api
#from datetime import datetime
#from openerp import tools
#from openerp.osv import osv
#from openerp import workflow


class planificacion_cursos(models.Model):
    _name = 'planificacion.cursos'
    _description = 'Formulario de Cursos'

    
    name = fields.Selection([('A','A'),('B','B'),('C','C'),('D','D'),('E','E'),('F','F')],'Cursos', size =30, required=True, help='Ingrese los cursos')
    #description = fields.Text()
    active = fields.Boolean('Active', default=True)
    institucion = fields.Many2one('res.company', default = lambda self: self.env.user.company_id.name, string="Colegio")
    #name = fields.Char (string="Nombre del Curso",required=True, readonly=False, help="Introduzca el Nombre del Curso")


class planificacion_nivel(models.Model):
    _name = 'planificacion.nivel'
    _description = 'Formulario de Nivel'

    
    name = fields.Selection([('Primero_Basico','Primero Basico'),('Segundo_Basico','Segundo Basico'),('Tercero_Basico','Tercero Basico'),('Cuarto_Basico','Cuarto Basico'),
        ('Quinto_Basico','Quinto Basico'),('Sexto_Basico','Sexto Basico')],'Niveles', size =30, required=True, help = 'Ingrese los Niveles')
    #description = fields.Text()
    active = fields.Boolean('Active', default=True)
    institucion = fields.Many2one('res.company', default = lambda self: self.env.user.company_id.name, string="Colegio")
    #name = fields.Char (string="Nombre del Curso",required=True, readonly=False, help="Introduzca el Nombre del Curso")
    
        
class planificacion_nivel_curso(models.Model):
    _name = 'planificacion.nivel_curso'
    _description = 'Formulario de Niveles'

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['nivel_id', 'cursos_id'], context=context)
        res = []
        for record in reads:
            name1 = record['nivel_id']
            name2 = record['cursos_id']
            if name2:
                name3 = name1 + name2
            res.append((record['id'], name3))
        return res 

    name = fields.Char(string='Descripcion', required=True)
    nivel_id = fields.Many2one ('planificacion.nivel', 'nivel')
    active = fields.Boolean('Active', default=True)
    cursos_id = fields.Many2one ('planificacion.cursos', 'Cursos')
    institucion = fields.Many2one('res.company', default = lambda self: self.env.user.company_id.name, string="Colegio")
    

class planificacion_asignaturas(models.Model):
    _name = 'planificacion.asignaturas'
    _description = 'Formulario de Asignaturas'

    name = fields.Char('Asignatura', required=True, help = 'Ingrese las Asignaturas')
    active = fields.Boolean('Active', default=True)
    institucion = fields.Many2one('res.company', default = lambda self: self.env.user.company_id.name, string="Colegio")
    horas = fields.Integer (string ='Horas')


class planificacion_asignaturas_niveles(models.Model):
    _name = 'planificacion.asignaturas_niveles'
    _description = 'Formulario de Asignaturas Niveles'

    name = fields.Char('Asignatura-Nivel', required=True)
    asignatura_id = fields.Many2one ('planificacion.asignaturas', 'Asignatura')
    active = fields.Boolean('Active', default=True)
    institucion = fields.Many2one('res.company', default = lambda self: self.env.user.company_id.name, string="Colegio")
    nivel_id = fields.Many2one ('planificacion.nivel', 'niveles')


class planificacion_unidades(models.Model):
    _name = 'planificacion.unidades'
    _description = 'Formulario de Unidades'

    name = fields.Char('Unidad', required=True, help = 'Ingrese las Unidades')
    #description = fields.Text()
    active = fields.Boolean('Active', default=True)
    institucion = fields.Many2one('res.company', default = lambda self: self.env.user.company_id.name, string="Colegio")
    

class planificacion_ejes(models.Model):
    _name = 'planificacion.ejes'
    _description = 'Formulario de Ejes'

    name = fields.Char('Eje', required=True, help = 'Ingrese los Ejes')
    #description = fields.Text()
    active = fields.Boolean('Active', default=True)
    institucion = fields.Many2one('res.company', default = lambda self: self.env.user.company_id.name, string="Colegio")
    nivel_id = fields.Many2one ('planificacion.nivel', 'niveles')
    asignatura_id = fields.Many2one ('planificacion.asignaturas', 'Asignaturas')


class planificacion_tipo(models.Model):
    _name = 'planificacion.tipo'
    _description = 'Formulario de Tipos'

    name = fields.Char('Tipo', required=True, help = 'Ingrese los Tipos')
    #description = fields.Text()
    active = fields.Boolean('Active', default=True)
    institucion = fields.Many2one('res.company', default = lambda self: self.env.user.company_id.name, string="Colegio")
    

class planificacion_curriculo(models.Model):
    _name = 'planificacion.curriculo'
    _description = 'Formulario de Curriculum'

    name = fields.Text('Descripcion', required=True, help = 'Ingrese los Curriculums')
    orden = fields.Char('Orden', help = 'Ingresar el Orden del Curriculo segun MINEDUC')
    active = fields.Boolean('Active', default=True)
    institucion = fields.Many2one('res.company', default = lambda self: self.env.user.company_id.name, string="Colegio")
    nivel_id = fields.Many2one ('planificacion.nivel', 'niveles')
    asignatura_id = fields.Many2one ('planificacion.asignaturas', 'Asignaturas')
    unidad_id = fields.Many2one ('planificacion.unidades', 'Unidad')
    tipo_id = fields.Many2one ('planificacion.tipo', 'Tipo')
    indicadores_ids = fields.One2many('planificacion.indicadores', 'curriculo_id', 'Indicadores')
    clase_line = fields.Many2one('planificacion.clases.line', 'Renglon')


class planificacion_indicadores(models.Model):
    _name = 'planificacion.indicadores'
    _description = 'Formulario de Indicadores'

    curriculo_id = fields.Many2one('planificacion.curriculo', 'Curriculo')
    name = fields.Text('Descripcion', required=True, help = 'Ingrese los Indicadores')
    

class planificacion_clases(models.Model):
    _name = 'planificacion.clases'
    _description = 'Formulario de Clases'
#    
#    @api.one
#    @api.depends('attribute', 'sale_line.product_template',
#                 'sale_line.product_template.attribute_line_ids')
#    def _get_possible_attribute_values(self): 
#        attr_values = self.env['product.attribute.name']
#        for curr_line in self.sale_line.product_template.attribute_line_ids:
#            if attr_line.attribute_id.id == self.attribute.id:
#                attr_values |= attr_line.value_ids
#        self.possible_values = attr_values.sorted()

#    @api.one
#    @api.depends('attribute', 'sale_line.product_template',
#                 'sale_line.product_template.attribute_line_ids')
    
    #def _get_curriculo(self): 
    #    curr_values = self.env['planificacion.curriculo.name']
    #    for curr_line in self.sale_line.product_template.attribute_line_ids:
    #        if attr_line.attribute_id.id == self.attribute.id:
    #            attr_values |= attr_line.value_ids
    #    self.possible_values = attr_values.sorted()

    nivel_id = fields.Many2one ('planificacion.nivel', 'niveles')
    asignatura_id = fields.Many2one ('planificacion.asignaturas', 'Asignaturas')
    name = fields.Char('Descripcion', required=True, help = 'Ingrese El nombre de la clase')
    active = fields.Boolean('Active', default=True)
    objetivo = fields.Text('Objetivo', required=True, help = 'Ingrese El Objetivo de la clase')
    inicio = fields.Text('Inicio', required=True, help = 'Inicio de la clase')
    desarrollo = fields.Text('Desarrollo', required=True, help = 'Desarrollo de la clase')
    cierre = fields.Text('Cierre', required=True, help = 'Cierre de la clase')
    evaluacion = fields.Text('Evaluacion', required=True, help = 'Evaluacon de la clase')
    recursos = fields.Text('Recursos', required=True, help = 'Recursos de la clase')    
    institucion = fields.Many2one('res.company', default = lambda self: self.env.user.company_id.name, string="Colegio")
    #nivel_id = fields.Many2one ('planificacion.nivel', 'niveles')
    #asignatura_id = fields.Many2one ('planificacion.asignaturas', 'Asignaturas')
    fecha = fields.Datetime('Fecha')
    clase_line_ids = fields.One2many('planificacion.clases.line', 'clase_id', 'Curriculos')
    #name_curriculo = fields.Many2many(comodel_name='planificacion.curriculo.name',
    #    compute='_get_curriculo', readonly=True)
    #unidad_id = fields.Many2one ('planificacion.unidades', 'Unidad')
    #tipo_id = fields.Many2one ('planificacion.tipo', 'Tipo')
    #indicadores_ids = fields.One2many('planificacion.indicadores', 'curriculo_id', 'Indicadores')

class planif_clases_curric_line(models.Model):
    _name = 'planificacion.clases.line'
    _description = 'Curriculo asociado a las clases'

    clase_id = fields.Many2one('planificacion.clases', 'Clase')
    name = fields.Text('Descripcion', required=True, help = 'Ingrese los Indicadores')
    curriculo_ids = fields.One2many('planificacion.curriculo', 'clase_line', 'Clases')
    indicadores_ids = fields.Many2many('planificacion.curriculo', 'planif_clas__curr_rel', 'clase_id', 'indicadores_ids', 'Indicadores Lines', readonly=True, copy=False)
    
