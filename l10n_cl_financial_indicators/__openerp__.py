# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2004-2015 OdooL (<http://odoo.com>).
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# This module authored by Daniel Blanco, Blanco Martín & Asociados
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Chilean Financial Indicators',
    'version': '0.1',
    'category': 'Tools',
    'complexity': 'easy',
    'description': '''Update UF, UTM and Dollar Official Value in a daily basis
using SBIF webservices''',
    'author': 'Blanco Martin & Asociados',
    'website': 'http://blancomartin.cl',
    'depends': ['base'],
    'init_xml': [],
    'update_xml': [
        'ir_cron.xml'
    ],
    'demo_xml': [
    ],
    'test': [
    ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
