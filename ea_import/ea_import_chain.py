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
import csv
import re
import logging
from datetime import datetime
from cStringIO import StringIO

from openerp.osv import orm, fields
from openerp.tools.translate import _
from xml.etree import ElementTree as ET
from collections import defaultdict

_logger = logging.getLogger(__name__)

try:
    from ftplib import FTP_TLS
except:
    from ftplib import FTP

try:
    import MySQLdb as mdb
except:
    _logger.error(
        'Not able to import MySQL dependencies. '
        'MySQL imports are not going to work.'
    )

def unicode_csv_reader(
    unicode_csv_data, dialect=csv.excel, charset='utf-8', **kwargs
):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data, charset),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, charset) for cell in row]


def utf_8_encoder(unicode_csv_data, charset):
    for line in unicode_csv_data:
        yield line
        # yield line.decode(charset).encode('utf-8', 'ignore')


class ea_import_chain(orm.Model):
    _name = 'ea_import.chain'
    _columns = {
        'name': fields.char('Name', size=256, required=True),
        'type': fields.selection(
            [('csv', 'CSV Import'),
             ('ftp', 'Import from ftp server'),
             ('mysql', 'MySql Import'),
             ('po3', 'PO3 Import')],
            'Import Type',
            required=True,
            help="Type of connection import will be done from"
        ),
        'mysql_config_id': fields.many2one(
            'mysql.config', 'MySql configuration'
        ),
        'ftp_config_id': fields.many2one(
            'import.ftp_config', 'FTP Configuration'
        ),
        'input_file': fields.binary('Test Importing File', required=False),
        'header': fields.boolean('Header'),
        'template_ids': fields.one2many(
            'ea_import.template', 'chain_id', 'Templates',
        ),
        # to be removed
        'result_ids': fields.one2many(
            'ea_import.chain.result', 'chain_id', 'Import Results',
        ),
        'log_ids': fields.one2many('ea_import.log', 'chain_id', 'Import Log',),
        'separator': fields.selection([
            (",", '<,> - Coma'),
            (";", '<;> - Semicolon'),
            ("\t", '<TAB> - Tab'),
            (" ", '<SPACE> - Space'),
        ], 'Separator', required=True),
        'delimiter': fields.selection([
            ("'", '<\'> - Single quotation mark'),
            ('"', '<"> - Double quotation mark'),
        ], 'Delimiter',),
        'charset': fields.selection([
            ('us-ascii', 'US-ASCII'),
            ('utf-7', 'Unicode (UTF-7)'),
            ('utf-8', 'Unicode (UTF-8)'),
            ('utf-16', 'Unicode (UTF-16)'),
            ('windows-1250', 'Central European (Windows 1252)'),
            ('windows-1251', 'Cyrillic (Windows 1251)'),
            ('iso-8859-1', 'Western European (ISO)'),
            ('iso-8859-15', 'Latin 9 (ISO)'),
        ], 'Encoding', required=True),
        'model_id': fields.many2one('ir.model', 'Related document model'),
        }

    _defaults = {
        'separator': ",",
        'charset': 'utf-8',
        'delimiter': "'",
        'type': 'csv',
    }

    def get_po3_data(self, cr, uid, data, charset, date, context):
        period_obj = self.pool.get('account.period')
        period_ids = period_obj.search(cr, uid, [], context=context)

        def etree_to_dict(t):
            d = {t.tag: {} if t.attrib else None}
            children = list(t)
            if children:
                dd = defaultdict(list)
                for dc in map(etree_to_dict, children):
                    for k, v in dc.iteritems():
                        dd[k].append(v)
                d = {t.tag: {
                    k: v[0] if len(v) == 1 else v for k, v in dd.iteritems()}
                }
            if t.attrib:
                d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
            if t.text:
                text = t.text.strip()
                if children or t.attrib:
                    if text:
                        d[t.tag]['#text'] = text
                else:
                    d[t.tag] = text
            return d
        date = datetime.strptime(date, '%Y-%m-%d')
        for period_id in period_ids:
            period = period_obj.browse(cr, uid, period_id, context)
            if (
                datetime.strptime(period.date_start, '%Y-%m-%d') <= date <=
                datetime.strptime(period.date_stop, '%Y-%m-%d')and not
                period.special
            ):
                date_move = date.strftime('%d/%m/%Y')
                period_code = period.code
        tree = ET.parse(data)
        root = tree.getroot()
        account_move_lines = []
        account_move = []
        datas = []
        date = None
        xml_dictionary = etree_to_dict(root)
        for count, row in enumerate(
                xml_dictionary['DATAPACKET']['ROWDATA'].values()):
            for rowpartidas in row:
                for line in rowpartidas['Partidas']['ROWPartidas']:
                    account_move_lines.append(date_move)
                    account_move_lines.append(period_code)
                    account_move_lines.append(row[count]['@TipoPoliz'])
                    if line['@DebeHaber'] == 'H':
                        account_move_lines.append(line['@Monto'])
                        account_move_lines.append(0.0)
                    else:
                        account_move_lines.append(0.0)
                        account_move_lines.append(line['@Monto'])
                    account_move_lines.append(line['@Cuenta'])
                    account_move_lines.append(line['@ConceptoPol'])
                    if not line['CDSPartidasUUID'] == None:
                        rfc = line['CDSPartidasUUID']['ROWCDSPartidasUUID'][
                            '@RFCRECEPTOR']
                    account_move_lines.append(rfc)
                    account_move.append(account_move_lines)
                    account_move_lines = []
                datas.append(account_move)
                account_move = []
        return datas

    def import_data_from_file(self, cr, uid, chain, context, datas):
        context = context or None
        result = {}
        result_pool = self.pool.get('ea_import.chain.result')
        log_pool = self.pool.get('ea_import.log')
        if any(
            [True for template in chain.template_ids for line in
             template.line_ids if line.field_type == 'many2one' and
             line.many2one_rel_type == 'active_id']
        ):
            self.check_active_ids(context=context)
        for template in chain.template_ids:
            model_name = template.target_model_id.model
            result.update({model_name: {
                'ids': set([]),
                'post_import_hook': template.post_import_hook}})
        for row_number, record_list in enumerate(datas):
            if (
                len(record_list) < max(
                    [template_line.sequence for template_line in
                     template.line_ids for template in chain.template_ids])
            ):
                raise orm.except_orm(
                    _('Error !'),
                    _("Invalid File or template definition. You have less "
                      "columns in file than in template. Check the file "
                      "separator or delimiter or template.")
                )
            for template in sorted(
                chain.template_ids, key=lambda k: k.sequence
            ):
                model_name = template.target_model_id.model
                result_id = template.generate_record(
                    record_list, row_number, context=context)
                result[model_name]['ids'] = (
                    result[model_name]['ids'] | set(result_id))
        for name, imported_ids, post_import_hook in [
                (name, value['ids'], value['post_import_hook'])
                for name, value in result.iteritems()]:
            if post_import_hook and hasattr(
                self.pool.get(name), post_import_hook
            ):
                getattr(self.pool.get(name), post_import_hook)(
                    cr, uid, list(imported_ids), context=context)
            result_ids_file = base64.b64encode(str(list(imported_ids)))
            result_ids = result_pool.create(cr, uid, {
                'chain_id': chain.id,
                'result_ids_file': result_ids_file,
                'name': name,
                'import_time': datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S'), }
            )
            context['result_ids'].append(result_ids)

        log_id = log_pool.create(cr, uid, {
            'chain_id': chain.id,
            'import_time': datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'), }
        )
        result_pool.write(
            cr, uid,
            context.get('result_ids', []),
            {'log_id': log_id},
            context=context
        )
        log_line_obj = self.pool.get('ea_import.log.line')
        for line in context.get('import_log', []):
            log_line_obj.create(cr, uid, {
                'log_id': log_id,
                'name': line}
            )
        context['log_id'].append(log_id)
        return True

    def get_mysql_data(self, config_obj):
        connect = mdb.connect(
            host=config_obj.host, user=config_obj.username,
            passwd=config_obj.passwd, db=config_obj.db
        )
        connect.escape_string("'")
        cursor = connect.cursor()
        if re.match(
            r'CREATE|DROP|UPDATE|DELETE', config_obj.query, re.IGNORECASE
        ):
            raise orm.except_orm(
                _('Error !'),
                _("Operation prohibitet!")
            )
        cursor.execute(config_obj.query)
        data = cursor.fetchall()
        connect.close()
        return '\n'.join(
            [row[1:-2] for row in [str(item) + ',' for item in data]])

    def get_ftp_data(self, cr, uid, ids, context={}):
        for chain in self.browse(cr, uid, ids, context=context):
            config_obj = chain.ftp_config_id
            try:
                conn = FTP_TLS(
                    host=config_obj.host,
                    user=config_obj.username,
                    passwd=config_obj.passwd
                )
                conn.prot_p()
            except:
                conn = FTP(
                    host=config_obj.host,
                    user=config_obj.username,
                    passwd=config_obj.passwd
                )
            filenames = conn.nlst()
            for filename in filenames:
                input_file = StringIO()
                conn.retrbinary(
                    'RETR %s' % filename, lambda data: input_file.write(data))
                input_string = input_file.getvalue()
                input_file.close()
                csv_reader = unicode_csv_reader(
                    StringIO(input_string),
                    delimiter=str(chain.separator),
                    quoting=(
                        (not chain.delimiter and csv.QUOTE_NONE) or
                        csv.QUOTE_MINIMAL
                    ),
                    quotechar=chain.delimiter and str(chain.delimiter) or None,
                    charset=chain.charset
                )
                self.import_to_db(
                    cr, uid, ids, csv_reader=csv_reader, context=context
                )
                conn.delete(filename)
            conn.quit()
        return True

    def check_active_ids(self, context={}):
        """Checks whether import is run from form view
        of object with model name defined above if there
        is template line defined with relational type of
        'active_id'.
        """
        if (
            not context.get('active_id') or
            len(context.get('active_ids', [])) > 1
        ):
            raise orm.except_orm(
                _('Error!'),
                _("This import template can be used only from form view!")
            )
        return True

    def import_to_db(self, cr, uid, ids, date, context={}, csv_reader=False):
        if not csv_reader:
            time_of_start = datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S.%f')
            context.update({'time_of_start': time_of_start})
            context['result_ids'] = []
            context['log_id'] = []
            context['import_log'] = []
        result_pool = self.pool.get('ea_import.chain.result')
        log_pool = self.pool.get('ea_import.log')
        for chain in self.browse(cr, uid, ids, context=context):
            if not chain.type:
                raise orm.except_orm(
                    _('Error !'),
                    _("No connection type specified!")
                )
            if chain.type == 'csv' and not csv_reader:
                csv_reader = unicode_csv_reader(
                    StringIO(base64.b64decode(chain.input_file)),
                    delimiter=str(chain.separator),
                    quoting=(
                        (not chain.delimiter and csv.QUOTE_NONE) or
                        csv.QUOTE_MINIMAL),
                    quotechar=chain.delimiter and str(chain.delimiter) or None,
                    charset=chain.charset
                )
            elif chain.type == 'mysql' and not csv_reader:
                input_data = self.get_mysql_data(chain.mysql_config_id)
                csv_reader = unicode_csv_reader(
                    StringIO(input_data),
                    delimiter=str(chain.separator),
                    quoting=(
                        (not chain.delimiter and csv.QUOTE_NONE) or
                        csv.QUOTE_MINIMAL),
                    quotechar=chain.delimiter and str(chain.delimiter) or None,
                    charset=chain.charset
                )
            elif chain.type == 'ftp' and not csv_reader:
                self.get_ftp_data(cr, uid, ids, context=context)
                continue
            if chain.type == 'po3':
                file_po3 = self.get_po3_data(
                    cr, uid,
                    StringIO(base64.b64decode(chain.input_file)),
                    chain.charset, date, context
                )
            else:
                if chain.header:
                    csv_reader.next()
            if csv_reader:
                self.import_data_from_file(
                    cr, uid, chain, context, csv_reader)
            else:
                for item in file_po3:
                    self.import_data_from_file(
                        cr, uid, chain, context, item)
        return True
