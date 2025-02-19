from odoo import api,fields,models,_
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)




class CustomerCreditLimitWizard(models.TransientModel):
    _name = 'customer.credit.limit.wizard'
    _description = 'Customer Credit Limit'

    partner_id = fields.Many2one('res.partner', string="Customer", readonly=True)
    sale_order_id = fields.Many2one('sale.order', string="Current Quotation", readonly=True)
    credit_limit=fields.Float(related='partner_id.credit_limit',readonly=False)
    credit_limit_on_hold=fields.Boolean(related='partner_id.credit_limit_on_hold',readonly=False)
   
    total_receivable = fields.Float(string="Total Receivable",compute="_compute_total_receivable")
    pending_sale_orders = fields.Float(string="Sale Orders",compute="_compute_total_pending_amount")
    draft_invoices = fields.Float(string="Invoices",compute="_compute_invoices")
    current_Quotation=fields.Float(string="Current Quotation", readonly=True)
    exceeded_amount = fields.Float(string="Exceeded Amount", readonly=True, compute="_compute_exceeded_amount")
    
    
    @api.model
    def default_get(self, fields):
        res = super(CustomerCreditLimitWizard, self).default_get(fields)
        active_id = self.env.context.get('active_id') 

        if active_id:
            sale_order = self.env['sale.order'].browse(active_id)
            partner = sale_order.partner_id  

            res['partner_id'] = partner.id
            res['sale_order_id'] = sale_order.id
            res['credit_limit'] = partner.credit_limit
            res['credit_limit_on_hold'] = partner.credit_limit_on_hold
        return res
    
    @api.depends('partner_id','current_Quotation')
    def _compute_total_pending_amount(self):
        for record in self:
            # add draft orders
            pending_orders = self.env['sale.order'].search([
                ('partner_id','=',record.partner_id.id),
                ('state', 'in', ['draft','sale'])
            ])
            amt = sum(order.amount_total for order in pending_orders)
            invoice=sum(o.amount_invoiced for o in pending_orders)
            _logger.info(f"invoice...................{invoice}")

            if record.current_Quotation:
                record.pending_sale_orders =round(amt - record.current_Quotation - invoice, 3)
            else:
                record.pending_sale_orders =round(amt - invoice, 3)
            
    @api.depends('partner_id')
    def _compute_total_receivable(self):
        for rec in self:
            if rec.partner_id:
                invoices = self.env['account.move'].search([
                    ('partner_id', '=', rec.partner_id.id), 
                    ('state', 'in', ['open', 'posted'])
                    ])
                rec.total_receivable = sum(invoice.amount_residual for invoice in invoices)


    @api.depends('partner_id')
    def _compute_invoices(self):
        for rec in self:
            if rec.partner_id:
                # draft_invo=0
                d_invoices=self.env['account.move'].search([
                    ('partner_id','=',rec.partner_id.id),
                    ('state','=','draft'),
                ])
                rec.draft_invoices=sum(invoice.amount_total for invoice in d_invoices)
                _logger.info(f"rec_draft_invoices..........................{rec.draft_invoices}")

    @api.depends('total_receivable', 'current_Quotation', 'credit_limit','draft_invoices')
    def _compute_exceeded_amount(self):
        for rec in self:
            total_due = rec.total_receivable + rec.current_Quotation +rec.pending_sale_orders + rec.draft_invoices
            rec.exceeded_amount =total_due - rec.credit_limit

    
    def confirm_order(self):
        for rec in self:
            total_due = rec.total_receivable + rec.current_Quotation + rec.pending_sale_orders +rec.draft_invoices
            rec.exceeded_amount =total_due - rec.credit_limit

            if total_due > rec.credit_limit:
                raise ValidationError(_("Your credit limit is exceeded"))
                _logger.info(f"rec_credit_limit.............................{rec.credit_limit}")

            elif rec.exceeded_amount > 0:
                raise ValidationError(_("The exceeded amount is too high "))
                _logger.info(f"total_due.......................{total_due}")

            elif rec.credit_limit_on_hold:    
                raise ValidationError(_("This customer has a credit limit hold. You cannot confirm this order."))
            
            else:
                rec.sale_order_id.action_confirm()


   
































