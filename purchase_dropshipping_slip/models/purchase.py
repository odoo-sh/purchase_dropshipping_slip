# copyright 2023 Sodexis
# license OPL-1 (see license file for full copyright and licensing details).
import base64
from odoo import models, fields, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_partner_id = fields.Many2one(comodel_name="res.partner",
                                      compute="_get_sale_partner",
                                      compute_sudo = True,
                                      string="Customer")

    def _get_sale_partner(self):
        for purchase in self:
            purchase.sale_partner_id = False
            if purchase._get_sale_orders():
                purchase.sale_partner_id = purchase._get_sale_orders()[0].partner_id.id

    def action_rfq_send(self):
        res = super(PurchaseOrder,self).action_rfq_send()
        if not self._context.get('send_rfq') and self.default_location_dest_id_usage == 'customer' and self._get_sale_orders():
            self.ensure_one()
            ir_model_data = self.env['ir.model.data']
            try:
                template_id = ir_model_data._xmlid_lookup('purchase_dropshipping_slip.email_template_edi_purchase_dropshipping')[2]
            except ValueError:
                template_id = False
            dropship_report = self.env.ref('purchase_dropshipping_slip.action_report_purchase_dropshipping_order')._render_qweb_pdf(self.id)
            purchase_order_report = self.env.ref('purchase.action_report_purchase_order')._render_qweb_pdf(self.id)
            filename = self.name
            res['context'].update({
                            'default_use_template': bool(template_id),
                            'default_template_id': template_id,
                            })
            attachments = self.env['ir.attachment'].create([{
                    'name': F"Purchase Order - {filename}",
                    'datas': base64.b64encode(purchase_order_report[0]),
                    'res_model': 'purchase.order',
                    'res_id': self.id,
                    'type': 'binary',
                },{
                    'name': F"DeliverySlip_{self.origin}",
                    'datas': base64.b64encode(dropship_report[0]),
                    'res_model': 'purchase.order',
                    'res_id': self.id,
                    'type': 'binary',
                }])
            if attachments:
                res['context'].update({
                            'default_attachment_ids': attachments.ids,
                            })
        return res