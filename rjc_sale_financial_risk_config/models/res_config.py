# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_order_block = fields.Boolean(
        string='Block Sale Order Risk',
        config_parameter='sale.sale_order_block',
    )
