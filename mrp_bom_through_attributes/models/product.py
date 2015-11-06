# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import fields, models

class ProductAttribute2(models.Model):
    _inherit = "product.attribute"

    product_qty_ids = fields.One2many('product.attribute.qty', 'attribute_id', 'Atributos')


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    raw_product = fields.Many2one('product.product',
                                  string='Raw Product')
    raw_qty = fields.Float(string='Raw Product QTY', default=1.)

    product_tmpl_id = fields.Many2one('product.template',
                                  string='roduct Template')

    size_x = fields.Float('Width')
    size_y = fields.Float('Length')
    size_z = fields.Float('Thickness')


class ProductAttributeqty(models.Model):
    _name = "product.attribute.qty"

    name = fields.Char(string='Nombre')
    raw_product = fields.Many2one('product.product',
                                  string='Raw Product')
    sequence = fields.Integer(string='secuencia')
    raw_qty = fields.Float(string='Raw Product QTY', default=1.)

    product_tmpl_id = fields.Many2one('product.template',
                                  string='roduct Template')

    value_id = fields.Many2one('product.attribute.value', string = 'Valores')
    attribute_id = fields.Many2one('product.attribute', string = 'Atributos')
    size_x = fields.Float('Width')
    size_y = fields.Float('Length')
    size_z = fields.Float('Thickness')

class ProductAttributePrice(models.Model):
    _inherit = "product.attribute.price"

    raw_product = fields.Many2one('product.product',
                                  string='Raw Product')
    raw_qty = fields.Float(string='Raw Product QTY', default=1.)
    size_x = fields.Float('Width', default=1.)
    size_y = fields.Float('Length', default=1.)
    size_z = fields.Float('Thickness', default=1.)

    



