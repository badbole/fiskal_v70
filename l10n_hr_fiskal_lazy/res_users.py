# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Module: l10n_hr_fiskal_lazy
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

from osv import osv, fields

class res_users(osv.osv):
    _inherit = "res.users"
    
    _columns = {
                'prostor_id':fields.many2one('fiskal.prostor','Podružnica', help="Zadana podružnica"),
                'uredjaj_id':fields.many2one('fiskal.uredjaj','Naplatni uredjaj',help="Zadani naplatni uređaj"),
                'journal_id':fields.many2one('account.journal','Dokument', help="Zadani dnevnik"),
                'double_check':fields.boolean('Dvostruka provjera na računima'),
                }
    
    def onchange_journal_id(self, cr, uid, ids, journal_id=False, context=None):
        result = super(res_users,self).onchange_journal_id(cr, uid, ids, journal_id=journal_id, context=context)
        if journal_id:
            journal = self.pool.get('account.journal').browse(cr, uid, journal_id, context=context)
            prostor_id = journal.prostor_id and journal.prostor_id.id or False
            nac_plac = journal.nac_plac or False
            uredjaj_id = journal.fiskal_uredjaj_ids and journal.fiskal_uredjaj_ids[0].id or False
            result['value'].update({'nac_plac' : nac_plac,
                                    'uredjaj_id' : uredjaj_id,
                                   })
            result['domain']= result.get('domain',{})
            result['domain'].update({'uredjaj_id':[('prostor_id','=',prostor_id )]})
        
        return result
