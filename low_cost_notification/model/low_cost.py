from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class LowCost(models.Model):
    _name = "low.cost"
    _description = "Low Cost Notification"
    _rec_name="product_id"

   
    product_id = fields.Many2one('product.template',string="Low Cost Product")
    current_qty=fields.Float(string="current qty")
    minimum_qty=fields.Float(string="Minimum Qty")

    # @api.model
    # def low_cost_quantity(self):
    #     min_qty = int(self.env['ir.config_parameter'].get_param('low_cost_notification.minimum_quantity'))
    #     _logger.info(f"Minimum quantity: {min_qty}")

    #     low_qty_pro = self.env['product.template'].search([('qty_available', '<', min_qty)])
    #     _logger.info(f"Low cost quantity products: {low_qty_pro}")

    #     records_to_update = []
    #     records_to_create = []

    #     for rec in low_qty_pro:
    #         existing_record = self.search([('product_id', '=', rec.id)])
    #         _logger.info(f'Existing record: {existing_record}')
            
    #         if existing_record:
    #             if rec.qty_available > 10:
    #                 _logger.info(f"Deleting record for product {rec.id} as quantity is greater than 10")
    #                 existing_record.unlink()
    #             elif existing_record.current_qty != rec.qty_available:
    #                 _logger.info(f"Updating existing record for product {rec.id}")
    #                 existing_record.write({
    #                     'current_qty': rec.qty_available,
    #                     'minimum_qty': min_qty
    #                 })
    #         else:
    #             if rec.qty_available <= 10:
    #                 records_to_create.append({
    #                     'product_id': rec.id,
    #                     'current_qty': rec.qty_available,
    #                     'minimum_qty': min_qty
    #                 })

    #     if records_to_create:
    #         self.create(records_to_create)
    #         _logger.info(f"Created new records: {records_to_create}")

            
      
    @api.model
    def low_cost_quantity(self):
        min_qty = int(self.env['ir.config_parameter'].get_param('low_cost_notification.minimum_quantity'))
        _logger.info(f"Minimum quantity: {min_qty}")

        record_of_product = self.env['product.template'].search([])
        _logger.info(f"record_of_product: {record_of_product}")

        for record in record_of_product:
        
            existing_record = self.search([('product_id', '=', record.id)])
            
            
            if record.qty_available < min_qty:
                if existing_record:
                    if existing_record.current_qty != record.qty_available:
                        _logger.info(f"existing_record............. {record.id}")
                        existing_record.write({
                            'current_qty': record.qty_available,
                            'minimum_qty': min_qty
                        })
                else:
                    _logger.info(f"Creating new record for product................. {record.id}")
                    self.create({
                        'product_id': record.id,
                        'current_qty': record.qty_available,
                        'minimum_qty': min_qty,
                    })
            else:
                if existing_record:
                    existing_record.unlink()


    



        
      
