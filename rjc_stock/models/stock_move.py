from odoo import models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.onchange('product_id')
    def onchange_product_id(self):
        product = self.product_id.with_context(
            lang=self.partner_id.lang or self.env.user.lang)
        self.name = product.partner_ref
        self.product_uom = product.uom_id.id
        self.secondary_uom_id = product.purchase_secondary_uom_id
        return {'domain': {'product_uom': [
            ('category_id', '=', product.uom_id.category_id.id)]}}
