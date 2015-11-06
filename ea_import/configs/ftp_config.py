# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Enapps LTD (<http://www.enapps.co.uk>).
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

from ftplib import FTP_TLS

from openerp.osv import orm, fields
from openerp.tools.translate import _


class ftp_config(orm.Model):
    _name = 'import.ftp_config'
    _rec_name = 'name'

    _columns = {
        'name': fields.char('Name', size=512),
        'host': fields.char('Host', size=512, required=True),
        'port': fields.integer('Port'),
        'username': fields.char('Username', size=512, required=True),
        'passwd': fields.char('Password', size=512, required=True),
    }

    _defaults = {
        'host': 'localhost',
        'port': 21,
    }

    def test_connection(self, cr, uid, ids, context={}):
        for ftp in self.browse(cr, uid, ids, context=context):
            conn = FTP_TLS(
                host=ftp.host, user=ftp.username, passwd=ftp.passwd
            )
            if not conn:
                raise orm.except_orm(
                    _('Error!'),
                    _("Connection can not be established!\n"
                      "Please, check you settings")
                )

            conn.quit()
        raise orm.except_orm(
            _('!'),
            _("Connection Succeed!")
        )
