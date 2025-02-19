from odoo import models
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)




class customerxlsx(models.AbstractModel):
    _name="report.customer_limit.report_sale_quotation_xls"
    _inherit="report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, orders):
                _logger.info(f"orders................{orders.partner_id.name}")  
                
                for order in orders:
                         worksheet = workbook.add_worksheet(order.partner_id.name[:30])
                         bold = workbook.add_format({'bold': True})
                         center_format = workbook.add_format({'align': 'center'})
                         bold_color = workbook.add_format({'bold': True,'fg_color': 'yellow','align': 'center'})
                         bold_center = workbook.add_format({'align': 'center','bold': True,'font_size': 21})
                         worksheet.set_column('A:Z',15)

                         row=0 #starting position of row
                         col=0 #starting position of column
                         worksheet.write(row,col,'Date',bold) 
                         worksheet.write(row,col+1,order.date_order.strftime('%d-%m-%Y'))
                         row +=1 #row+1=1
                         worksheet.write(row,col,'Customer',bold) 
                         worksheet.write(row,col+1,order.partner_id.name)   
                         row +=1 #row+1=2
                         worksheet.write(row,col,'Payment Terms',bold) 
                         worksheet.write(row,col+1,order.payment_term_id.name)    

                        #  worksheet.write('A1','Date',bold) 
                        #  worksheet.write('A2','Customer',bold)  
                        #  worksheet.write('A3','Payment Terms',bold)    

                        #  worksheet.write('B1',order.date_order.strftime('%d-%m-%Y')) 
                        #  worksheet.write('B2',order.partner_id.name)  
                        #  worksheet.write('B3',order.payment_term_id.name)  

                         worksheet.merge_range('A5:F6','ORDER LINES',bold_center)

                         headers = [
                                 "No",
                                 "Product Name",
                                 "Quantity",
                                 "Unit Price",
                                 "Taxes",
                                 "Total Price",]
                         for i, header in enumerate(headers):
                            worksheet.write(6, i, header,bold_color)
                            # worksheet.set_column(i, i, len(header) + 5)   

                         row = 7  # Start after the headers for order lines
                         total=0
                         count_qty=0
                         count_taxes=0
                         for line in order.order_line:
                            worksheet.write(row, 0, row - 6,center_format)  # Row number
                            worksheet.write(row, 1, line.product_id.name,center_format)
                            worksheet.write(row, 2, line.product_uom_qty,center_format)
                            worksheet.write(row, 3, line.price_unit,center_format)
                            worksheet.write(row, 4, line.tax_id.name,center_format)
                            worksheet.write(row, 5, line.price_total,center_format)
                            total +=line.price_total
                            count_qty += line.product_uom_qty
                            count_taxes += sum(line.tax_id.mapped('amount'))
                            row += 1  # Move to the next row for each line
                            _logger.info(f"row.........................{row}")
                         worksheet.write(row + 4, 5,f'Total={total}',center_format)
                         worksheet.write(row + 4, 2,f'Total_qty={count_qty}',center_format)
                         worksheet.write(row + 4, 4,f'Total_taxes={count_taxes}',center_format)



                        #  max_length = max(len('Date'), len('Customer'), len('Payment Terms')) + 4  # Add some padding
                        #  worksheet.set_column('A:A', max_length)
                        #  worksheet.set_column('B:B', max_length)
                        #  worksheet.set_column('C:C', max_length)
                        #  worksheet.set_column('D:D', max_length)
                        #  worksheet.set_column('E:E', max_length)

                        #  worksheet.write('A7', 'No', bold)
                        #  worksheet.write('B7', 'Product Name', bold)
                        #  worksheet.write('C7', 'Quantity', bold)
                        #  worksheet.write('D7', 'Unit Price', bold)
                        #  worksheet.write('E7', 'Total Price', bold)


                        #  row = 7  # Start after the headers for order lines
                        #  total=0
                        #  count_qty=0
                        #  count_taxes=0
                        #  row1=7
                        #  for line in order.order_line:
                        #    #  _logger.info(f"row0.........................{row}")
                        #     worksheet.write(row+1, 0, row1 - 6,center_format)  # Row number
                        #     row+=1 #give the space between two lines
                        #    #  _logger.info(f"row1........................{row}")
                        #     worksheet.write(row, 1, line.product_id.name,center_format)
                        #    #  _logger.info(f"row2........................{row}")
                        #     worksheet.write(row, 2, line.product_uom_qty,center_format)
                        #    #  _logger.info(f"row3........................{row}")
                        #     worksheet.write(row, 3, line.price_unit,center_format)
                        #    #  _logger.info(f"row4........................{row}")
                        #     worksheet.write(row, 4, line.tax_id.name,center_format)
                        #    #  _logger.info(f"row5........................{row}")
                        #     worksheet.write(row, 5, line.price_total,center_format)
                        #    #  _logger.info(f"row6........................{row}")
                        #     total +=line.price_total
                        #     count_qty += line.product_uom_qty
                        #     count_taxes += sum(line.tax_id.mapped('amount'))
                        #     row += 1  # Move to the next row for each line
                        #     row1+=1
                        #     _logger.info(f"row.........................{row}")
                        #  worksheet.write(row + 4, 5,f'Total={total}',center_format)
                        #  worksheet.write(row + 4, 2,f'Total_qty={count_qty}',center_format)
                        #  worksheet.write(row + 4, 4,f'Total_taxes={count_taxes}',center_format)



class SaleOrder(models.Model):
    _inherit = "sale.order"                      
    

    def report_name(self):
         """Compute the report filename dynamically"""
         for record in self: 
            date_str = datetime.today().strftime("%Y-%m-%d") 
            return f"Customer_Report_{record.name or 'Unknown'}_{date_str}"









                        