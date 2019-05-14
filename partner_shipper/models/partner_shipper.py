from odoo import fields, models


class PartnerShipper(models.Model):
    _name = 'partner.shipper'
    _description = 'For create shipper'

    code = fields.Char(
        string='Code',
    )
    name = fields.Char(
        string='Name',
        required=True,
    )
    route = fields.Selection([
        ('north', 'ภาคเหนือ'),
        ('northeast', 'ภาคอีสาน'),
        ('central', 'ภาคกลาง'),
        ('south', 'ภาคใต้'),
        ('other', 'อื่น')],
        required=True,
    )
    street = fields.Char(
        string='Street',
    )
    street2 = fields.Char(
        string='Street2',
    )
    city = fields.Char(
        string='City',
    )
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='State',
        ondelete='restrict',
        domain="[('country_id', '=?', country_id)]",
    )
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country',
        ondelete='restrict',
    )
    phone = fields.Char(
        string='Phone',
    )
    mobile = fields.Char(
        string='Mobile',
    )
    fax = fields.Char(
        string='Fax',
    )
    zip = fields.Char(
        change_default=True,
    )
    email = fields.Char(
        string='Email',
    )
    active = fields.Boolean(
        string='Active',
        default=True
    )
    conversed_area = fields.Text(
        string='Conversed Area',
    )
    destination_contact = fields.Text(
        string='Destination Contacts',
    )
    note = fields.Text(
        string='Note',
    )
