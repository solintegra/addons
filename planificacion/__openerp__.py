# -*- coding: utf-8 -*-
{
    'name': "planificacion",

    'summary': """
        Modulo de planificaciones educativas para la plataforma Integrate""",

    'description': """
        Modulo de planificaciones educativas
    """,

    'author': "Integrate",
    'website': "http://www.redintegrate.cl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Educacion',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/planificacion_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        '',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
