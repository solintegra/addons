# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2012 ENNAPS LTD (<http://www.enapps.co.uk>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import orm, fields


class import_wizard(orm.TransientModel):
    _name = 'import_wizard'
    _description = 'Simple import wizard'

    _columns = {
        'chain_id': fields.many2one(
            'ea_import.chain', 'Import Chain',
            domain="[('model_id', '=', model_id)]"
        ),
        'model_id': fields.many2one(
            'ir.model', 'Related document model'
        ),
        'import_file': fields.binary('Importing file',),
        'type': fields.selection(
            [('csv', 'CSV Import'),
             ('ftp', 'Import from ftp server'),
             ('mysql', 'MySql Import'),
             ('po3', 'PO3 Import')],
            'Import Type', required=True,
            help="Type of connection import will be done from"
        ),
        'date': fields.date(
            'Fecha de Poliza'
        ),
    }

    def _get_default_chain(self, cr, uid, context=None):
        """
        Get default import chain based on selected object
        """
        objChain = self.pool.get('ea_import.chain')
        modelId = self.pool.get('ir.model').search(
            cr, uid, [('model', '=', context['model'])], context=context
        )[0]
        chainIds = objChain.search(
            cr, uid, [('model_id', '=', modelId)], context=context
        )
        return chainIds[0] if len(chainIds) else 0

    def _get_model(self, cr, uid, context=None):
        """
        Return the model from context to filter available Import Chains
        """
        res = self.pool.get('ir.model').search(
            cr, uid, [('model', '=', context.get('model', ''))],
            context=context
        )
        return res[0] if len(res) else None

    _defaults = {
        'model_id': _get_model,
        'chain_id': _get_default_chain,
    }

    def onchange_chain_id(self, cr, uid, ids, chain_id=False, context=None):
        """
        Update type field when user selects the Import Chain
        """
        res = {}
        ObjChain = self.pool.get('ea_import.chain')
        res['value'] = {
            'type': ObjChain.browse(
                cr, uid, chain_id, context=context
            ).type
        }
        return res

    def do_import(self, cr, uid, ids, context={}):
        for wizard in self.browse(cr, uid, ids, context=context):
            wizard.chain_id.write({'input_file': wizard.import_file})
            cr.commit()
            date = wizard.date
            wizard.chain_id.import_to_db(date)
        return {'type': 'ir.actions.act_window_close'}
