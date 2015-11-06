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
    #description = fields.Text()
    active = fields.Boolean('Active', default=True)
    institucion = fields.Many2one('res.company', default = lambda self: self.env.user.company_id.name, string="Colegio")
    nivel_id = fields.Many2one ('planificacion.nivel', 'niveles')
    asignatura_id = fields.Many2one ('planificacion.asignaturas', 'Asignaturas')
    unidad_id = fields.Many2one ('planificacion.unidades', 'Unidad')
    tipo_id = fields.Many2one ('planificacion.tipo', 'Tipo')
    indicadores_ids = fields.One2many('planificacion.indicadores', 'curriculo_id', 'Indicadores')


class planificacion_indicadores(models.Model):
    _name = 'planificacion.indicadores'
    _description = 'Formulario de Indicadores'

    curriculo_id = fields.Many2one('planificacion.curriculo', 'Curriculo')
    name = fields.Text('Descripcion', required=True, help = 'Ingrese los Indicadores')
    #description = fields.Text()
    #active = fields.Boolean('Active', default=True)
    #institucion = fields.Many2one('res.company', default = lambda self: self.env.user.company_id.name, string="Colegio")
    #nivel_id = fields.Many2one ('planificacion.nivel', 'niveles')
    #Asignatura_id = fields.Many2one ('planificacion.asignaturas', 'Asignaturas')
    #unidad_id = fields.Many2one ('planificacion.unidades', 'Unidad')    
    #tipo_id = fields.Many2one ('planificacion.tipo', 'Tipo')


