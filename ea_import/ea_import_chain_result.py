# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Enapps LTD (<http://www.enapps.co.uk>).
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

import base64

from openerp.osv import orm, fields


class ea_import_chain_result(orm.Model):
    _name = 'ea_import.chain.result'
    _order = 'import_time desc'
    _columns = {
        'name': fields.char('Model', size=256, required=True),
        'chain_id': fields.many2one('ea_import.chain',),  # to be removed
        'log_id': fields.many2one('ea_import.log',),
        'result_ids_file': fields.binary('Result Ids',),
        'import_time': fields.datetime('Import Time',),
        'scheduler_log_id': fields.many2one('ea_import.scheduler.log', 'Scheduler Log'),
        }

    def show_result(self, cr, uid, ids, context={}):
        for result in self.browse(cr, uid, ids, context=context):
            result_ids = eval(base64.b64decode(result.result_ids_file))
            return {
                'name': 'Result',
                'view_mode': 'tree,form',
                'view_type': 'form',
                'view_id': False,
                'res_model': result.name,
                'domain': [('id', 'in', result_ids)],
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
            }
