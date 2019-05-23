# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    shipper_ids = fields.Many2many(
        comodel_name='partner.shipper',
        string='Shippers',
        relation='partner_shipper_ref',
        column1='partner_id',
        column2='shipper_id',
    )
