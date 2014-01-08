# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Module: l10n_hr_acc_reports
#    Author: Davor Bojkić
#    mail:   bole@dajmi5.com
#    Copyright (C) 2012- Daj Mi 5, 
#                  http://www.dajmi5.com
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

from osv import fields,osv
import datetime

class l10n_hr_report_wiz(osv.TransientModel):
    _name='l10n.hr.report.wiz'
    
    _REPORT_TYPE = [
                    ('periodi','Kumulativno prometi po periodima'),
                    ('ppj','Periodi / Pos.Jed.')
                    ]
    
    def print_selected_report(selfcr, uid, ids, context=None):
        rtype = str(self.browse(cr, uid, ids[0]).report_type)
        if rtype == 'periodi': return True
        else: return False
    
    _columns = {
                'report_type':fields.selection(_REPORT_TYPE,'Report type', required=True),
                'period_id':fields.many2one('account.period','Period'),
                'date_start':fields.date('Date start'),
                'date_end':fields.selection('Date end')
                }
    
    
        