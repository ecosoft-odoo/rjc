# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import _, api, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        sale_order_block = self.env['ir.config_parameter'].sudo()\
            .get_param('sale.sale_order_block')
        partner = self.partner_id.commercial_partner_id
        exception_msg = ""
        if partner.risk_exception:
            exception_msg = _("Financial risk exceeded.\n")
        elif partner.risk_sale_order_limit and (
                (partner.risk_sale_order + self.amount_total) >
                partner.risk_sale_order_limit):
            exception_msg = _(
                "This sale order exceeds the sales orders risk.\n")
        elif partner.risk_sale_order_include and (
                (partner.risk_total + self.amount_total) >
                partner.credit_limit):
            exception_msg = _(
                "This sale order exceeds the financial risk.\n")
        if sale_order_block and exception_msg:
            raise ValidationError(exception_msg)
        return super(SaleOrder, self).action_confirm()
