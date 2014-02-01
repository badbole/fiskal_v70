# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    #    Module: account_2nd_currency
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
from decimal_precision import decimal_precision as dp
from datetime import date
from numpy.lib.financial import rate

class account_invoice(osv.Model):
    _inherit = 'account.invoice'
    
    
    def my_company(self, cr, uid, context=None):
        #TODO : Multi company... 
        return self.pool.get('res.company').browse(cr, uid, 1)
    
    def _foreign_partner_check(self, cr, uid, ids, field, value, context=None):
        res={}
        cc=self.my_company(cr, uid).partner_id.country_id.id
        for p in self.browse(cr, uid, ids):
            res[p.id]= p.partner_id.country_id.id and p.partner_id.country_id.id !=cc or False
        return res
    
    def _second_currency_value(self, cr, uid, ids, name, val, context=None):
        res = {}
        #odmah na HRK. id=30
        sc = self.pool.get('res.currency').browse(cr, uid, 30)
        for inv in self.browse(cr, uid, ids):
            res[inv.id]={'second_rate':sc.rate,
                         #'second_rdate':sc.date,
                         'second_value':inv.amount_total / sc.rate}
        return res
    
    _columns = {
                'second_curr':fields.function(_foreign_partner_check, type="boolean", string="Foreign partner", method=True, ),
                'second_value':fields.function(_second_currency_value, type="float", string="Iznos u EUR", method=True, multi="2nd"),
                'second_rate':fields.function(_second_currency_value, type="float", digits=(12,6), string="Tečaj", method=True, multi="2nd"),
                #'second_rdate':fields.function(_second_currency_value, type="date", string="Rate date", method=True, multi="2nd"),
                }
    def button_reverse(self, cr, uid, ids, context=None):
        reverse = self.pool.get('invoice.reverse.calc').create(cr, uid,{'invoice_id':ids[0]})
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_2nd_currency', 'invoice_reverse_calc_wizard')
        view_id = view_ref and view_ref[1] or False,
        return {
                'type': 'ir.actions.act_window',
                'name': 'Reverse calculation',
                'res_model': 'invoice.reverse.calc',
                'res_id': reverse,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'target': 'new',
                'nodestroy': False,
                }
    
    
    
    
class invoice_reverse_calc(osv.TransientModel):
    _name='invoice.reverse.calc'
    """
    When using second invoice and want to set target price in other currency
    """
    _columns = {
                'invoice_id':fields.many2one('account.invoice','Invoice'),
                'target_amount':fields.float('Amount',digits=(16,2))
                }
    
    def reverse_calc(self, cr, uid, ids, context=None):
        invoice = self.browse(cr, uid, ids[0])
        total_curr = invoice.invoice_id.amount_total
        rate = invoice.invoice_id.second_rate
        total_target = invoice.target_amount
        total_new = total_target * rate #for now only eur, other not working
        ff = total_new / total_curr
        lines = []
        for l in invoice.invoice_id.invoice_line:
            discount = 1.0
            if l.discount:
                discount = 100 / (100 - l.discount)
             
            new_price = ff * l.price_subtotal / (l.quantity  * discount) #taxes!
            
            new_values = {'price_unit':new_price}
            lines.append((1,l.id,new_values))
            
        if invoice.invoice_id.state != 'draft':
            raise osv.ecxept_osv('Error!','Changing invoice not in draft state NOT ALLOWED!')
        inv = self.pool.get('account.invoice')
        
        return inv.write(cr, uid, invoice.invoice_id.id, {'invoice_line':lines})