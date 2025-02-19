from odoo import api,fields,models
import logging

_logger = logging.getLogger(__name__)

class saleorder(models.Model):
    _inherit='res.partner'

    check_credit =fields.Boolean(string="Check Credit Limit")
    credit_limit=fields.Float(string="Credit Limit")
    credit_limit_on_hold=fields.Boolean(string="Credit Limit on Hold")

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    hold=fields.Boolean(related='partner_id.credit_limit_on_hold',readonly=False)
    limit=fields.Float(related="partner_id.credit_limit",readonly=False)
   
    def action_confirm(self):
        for order in self:
                current_quote = sum(x.price_total for x in order.order_line)
                existing_orders = self.env['sale.order'].search_count([
                ('partner_id', '=', order.partner_id.id),  
                ('id', '!=', order.id),  
                ('state', 'not in', ['cancel', 'done'])])  
                _logger.info(f"order_id.....................{order.id}")
                if existing_orders == 0:  
                    _logger.info(f"First order for partner {order.partner_id.name}, confirming order.{ {order.partner_id.id}}")
                    return super(SaleOrder, self).action_confirm()
                
                if order.partner_id.check_credit:
                    popup=self.env['customer.credit.limit.wizard'].create({
                         'partner_id':order.partner_id.id,
                         'current_Quotation':current_quote})
                    if popup.exceeded_amount > 0:
                        _logger.info(".................................................................")
                        return{
                            'name':'Credit Limit Warning',
                            'view_type':'form',
                            'view_mode':'form',
                            'res_model':'customer.credit.limit.wizard',
                            'type':'ir.actions.act_window',
                            'target':'new',
                            'res_id':popup.id,
                        }
        res=super(SaleOrder,self).action_confirm()
        return res

        

   