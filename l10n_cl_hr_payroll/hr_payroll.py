# -*- coding: utf-8 -*-
##############################################################################
# Chilean Payroll
# Odoo / OpenERP, Open Source Management Solution
# Copyright (c) 2015 Blanco Martin y Asociados
# Nelson Ramírez Sánchez - Daniel Blanco
# http://blancomartin.cl
#
# Derivative from Odoo / OpenERP / Tiny SPRL
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
from openerp import models, fields
# from datetime import date, datetime, timedelta


class hr_indicadores_previsionales(models.Model):

    _name = 'hr.indicadores'
    _description = 'Indicadores Previsionales'

    name = fields.Char('Nombre', required=True)
    asignacion_familiar_primer = fields.Float(
        'Asignacion Familiar Tramo 1', digits=(16, 2),
        help="Asig Familiar Primer Tramo")
    asignacion_familiar_segundo = fields.Float(
        'Asignacion Familiar Tramo 2', digits=(16, 2),
        help="Asig Familiar Segundo Tramo")
    asignacion_familiar_tercer = fields.Float(
        'Asignacion Familiar Tramo 3', digits=(16, 2),
        help="Asig Familiar Tercer Tramo")
    asignacion_familiar_monto_a = fields.Float(
        'Monto Tramo Uno', digits=(16, 2), help="Monto A")
    asignacion_familiar_monto_b = fields.Float(
        'Monto Tramo Dos', digits=(16, 2), help="Monto B")
    asignacion_familiar_monto_c = fields.Float(
        'Monto Tramo Tres', digits=(16, 2), help="Monto C")
    contrato_plazo_fijo_empleador = fields.Float(
        'Contrato Plazo Fijo Empleador', digits=(16, 2),
        help="Contrato Plazo Fijo Empleador")
    contrato_plazo_indefinido_empleador = fields.Float(
        'Contrato Plazo Indefinido Empleador', digits=(16, 2),
        help="Contrato Plazo Fijo")
    contrato_plazo_indefinido_empleador_otro = fields.Float(
        'Contrato Plazo Indefinido 11 anos o mas', digits=(16, 2),
        help="Contrato Plazo Indefinido 11 anos")
    caja_compensacion = fields.Float(
        'Caja Compensacion Los Andes', digits=(16, 2),
        help="Caja de Compensacion")
    deposito_convenido = fields.Float(
        'Deposito Convenido', digits=(16, 2), help="Deposito Convenido")
    fonasa = fields.Float('Fonasa', digits=(16, 2), help="Fonasa")
    mutual_seguridad = fields.Float(
        'Mutual Seguridad', digits=(16, 2), help="Mutual de Seguridad")
    pensiones_ips = fields.Float(
        'Pensiones IPS', digits=(16, 2), help="Pensiones IPS")
    sueldo_minimo = fields.Float(
        'Sueldo Minimo', digits=(16, 2), help="Sueldo Minimo")
    sueldo_minimo_otro = fields.Float(
        'Sueldo Minimo Menores de 18 y Mayores de 65', digits=(16, 2),
        help="Sueldo Minimo para Menores de 18 y Mayores a 65")
    tasa_mutual = fields.Float(
        'Tasa Mutual', digits=(16, 2), help="Tasa AFP Mutual")
    tasa_afp_cuprum = fields.Float(
        'Cuprum', digits=(16, 2), help="Tasa AFP Cuprum")
    tasa_afp_capital = fields.Float(
        'Capital', digits=(16, 2), help="Tasa AFP Capital")
    tasa_afp_provida = fields.Float(
        'ProVida', digits=(16, 2), help="Tasa AFP Provida")
    tasa_afp_modelo = fields.Float(
        'Modelo', digits=(16, 2), help="Tasa AFP Modelo")
    tasa_afp_planvital = fields.Float(
        'PlanVital', digits=(16, 2), help="Tasa AFP PlanVital")
    tasa_afp_habitat = fields.Float(
        'Habitat', digits=(16, 2), help="Tasa AFP Habitat")
    tasa_sis_cuprum = fields.Float(
        'SIS', digits=(16, 2), help="Tasa SIS Cuprum")
    tasa_sis_capital = fields.Float(
        'SIS', digits=(16, 2), help="Tasa SIS Capital")
    tasa_sis_provida = fields.Float(
        'SIS', digits=(16, 2), help="Tasa SIS Provida")
    tasa_sis_planvital = fields.Float(
        'SIS', digits=(16, 2), help="Tasa SIS PlanVital")
    tasa_sis_habitat = fields.Float(
        'SIS', digits=(16, 2), help="Tasa SIS Habitat")
    tasa_sis_modelo = fields.Float(
        'SIS', digits=(16, 2), help="Tasa SIS Modelo")
    tasa_independiente_cuprum = fields.Float(
        'SIS', digits=(16, 2), help="Tasa Independientes Cuprum")
    tasa_independiente_capital = fields.Float(
        'SIS', digits=(16, 2), help="Tasa Independientes Capital")
    tasa_independiente_provida = fields.Float(
        'SIS', digits=(16, 2), help="Tasa Independientes Provida")
    tasa_independiente_planvital = fields.Float(
        'SIS', digits=(16, 2), help="Tasa Independientes PlanVital")
    tasa_independiente_habitat = fields.Float(
        'SIS', digits=(16, 2), help="Tasa Independientes Habitat")
    tasa_independiente_modelo = fields.Float(
        'SIS', digits=(16, 2), help="Tasa Independientes Modelo")
    tope_anual_apv = fields.Float(
        'Tope Anual APV', digits=(16, 2), help="Tope Anual APV")
    tope_mensual_apv = fields.Float(
        'Tope Mensual APV', digits=(16, 2), help="Tope Mensual APV")
    tope_imponible_afp = fields.Float(
        'Tope imponible AFP', digits=(16, 2), help="Tope Imponible AFP")
    tope_imponible_ips = fields.Float(
        'Tope Imponible IPS', digits=(16, 2), help="Tope Imponible IPS")
    tope_imponible_salud = fields.Float(
        'Tope Imponible Salud', digits=(16, 2), help="Tope Imponible Salud")
    tope_imponible_seguro_cesantia = fields.Float(
        'Tope Imponible Seguro Cesantia', digits=(16, 2),
        help="Tope Imponible Seguro de Cesantia")
    uf = fields.Float(
        'UF', digits=(16, 2), required=True, help="UF fin de Mes")
    utm = fields.Float(
        'UTM', digits=(16, 2), required=True, help="UTM Fin de Mes")
    uta = fields.Float('UTA', digits=(16, 2), help="UTA Fin de Mes")
    uf_otros = fields.Float(
        'UF Otros', digits=(16, 2), help="UF Seguro Complementario")


class hr_payslip(models.Model):

    '''
    Pay Slip
    '''
    _inherit = 'hr.payslip'
    _description = 'Pay Slip'

    indicadores_id = fields.Many2one(
        'hr.indicadores', 'Indicadores',
        states={'draft': [('readonly', False)]}, readonly=True, required=True)

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        else:
            vals.update({'indicadores_id': context.get('indicadores_id')})
        return super(hr_payslip, self).create(
            cr, uid, vals, context=context)


class hr_payslip_run(models.Model):

    _inherit = 'hr.payslip.run'
    _description = 'Payslip Run'

    indicadores_id = fields.Many2one(
        'hr.indicadores', 'Indicadores',
        states={'draft': [('readonly', False)]}, readonly=True, required=True)


class hr_isapre(models.Model):
    _name = 'hr.isapre'
    _description = 'Isapres'

    name = fields.Char('Nombre', required=True)
    rut = fields.Char('RUT', required=True)


class hr_afp(models.Model):
    _name = 'hr.afp'
    _description = 'Fondos de Pension'

    codigo = fields.Char('Codigo', required=True)
    name = fields.Char('Nombre', required=True)
    rut = fields.Char('RUT', required=True)
    rate = fields.Float('Tasa', required=True)
    sis = fields.Float('Aporte Empresa', required=True)
    independiente = fields.Float('Independientes', required=True)


class hr_contract(models.Model):

    _inherit = 'hr.contract'
    _description = 'Employee Contract'

    afp_id = fields.Many2one('hr.afp', 'AFP')
    aporte_voluntario = fields.Float(
        'Aporte Voluntario', help="Aporte Voluntario al ahorro individual")
    anticipo_sueldo = fields.Float(
        'Anticipo de Sueldo',
        help="Anticipo De Sueldo Realizado Contablemente")
    carga_familiar = fields.Integer(
        'Carga Familiar',
        help="Carga Familiar para el calculo de asignacion familiar")
    colacion = fields.Float('Colacion', help="Colacion")
    isapre_id = fields.Many2one('hr.isapre', 'ISAPRE')
    isapre_cotizacion_uf = fields.Float(
        'Cotizacion UF', digits=(16, 2), help="Cotizacion Pactada en UF")
    movilizacion = fields.Float(
        'Movilizacion', help="Movilizacion")
    mutual_seguridad = fields.Boolean('Mutual Seguridad')
    otro_no_imp = fields.Float(
        'Otros No Imponible', help="Otros Haberes No Imponibles")
    otros_imp = fields.Float(
        'Otros Imponible', help="Otros Haberes Imponibles")
    pension = fields.Boolean('Pensionado')
    # seguro_complementario_id = fields.Many2one('hr.seguro.complementario',
    #    'Seguro Complementario')
    seguro_complementario_cotizacion_uf = fields.Float(
        'Cotizacion UF', digits=(16, 2), help="Cotizacion Pactada en UF")
    viatico_santiago = fields.Float(
        'Viatico Santiago', digits=(16, 2), help="Viatico Santiago")


class hr_type_employee(models.Model):
    _name = 'hr.type.employee'
    _description = 'Tipo de Empleado'

    id_type = fields.Char('Codigo', required=True)
    name = fields.Char('Nombre', required=True)


class hr_employee(models.Model):

    _inherit = 'hr.employee'
    _description = 'Employee Contract'

    type_id = fields.Many2one('hr.type.employee', 'Tipo de Empleado')


class hr_payslip_employees(models.TransientModel):

    _inherit = 'hr.payslip.employees'

    def compute_sheet(self, cr, uid, ids, context=None):
        run_pool = self.pool.get('hr.payslip.run')
        if context is None:
            context = {}
        if context.get('active_id'):
            run_data = run_pool.read(
                cr, uid, context['active_id'], ['indicadores_id'])
        indicadores_id = run_data.get('indicadores_id')
        indicadores_id = indicadores_id and indicadores_id[0] or False
        if indicadores_id:
            context = dict(context, indicadores_id=indicadores_id)
        return super(hr_payslip_employees, self).compute_sheet(
            cr, uid, ids, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
