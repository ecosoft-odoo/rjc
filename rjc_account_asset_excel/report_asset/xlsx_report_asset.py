# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, _


class AssetView(models.AbstractModel):
    # _name = 'account.view'
    _inherit = 'account.asset'
    _order = 'id'

    asset_id = fields.Many2one(
        comodel_name='account.asset',
        string='Asset ID',
    )
    depreciation = fields.Float(
        string='Depreciation',
    )
    accumulated_cf = fields.Float(
        string='Accumulated Depreciation',
    )
    accumulated_bf = fields.Float(
        string='Accumulated Depreciation Before',
    )


class XLSXReportAsset(models.TransientModel):
    _name = 'xlsx.report.asset'
    _description = 'Wizard for xlsx.report.asset'
    _inherit = 'xlsx.report'

    asset_status = fields.Selection(
        [('draft', 'Draft'),
         ('open', 'Running'),
         ('close', 'Close'),
         ('removed', 'Removed')],
        string=' Asset Status'
    )
    date_range_id = fields.Many2one(
        comodel_name='date.range',
        string='Period',
    )
    date_from = fields.Date(
        string='From Date',
        required=True,
    )
    date_to = fields.Date(
        string='To Date',
        required=True,
    )
    asset_ids = fields.Many2many(
        comodel_name='account.asset',
        string='Asset Code',
    )
    asset_profile_ids = fields.Many2many(
        'account.asset.profile',
        string='Asset Profile',
    )
    date_filter = fields.Char(
        compute='_compute_date_filter',
        string='Date Filter',
    )
    # Note: report setting
    accum_depre_account_type = fields.Many2one(
        'account.account.type',
        string='Account Type for Accum.Depre.',
        required=True,
        help="Define account type for accumulated depreciation account, "
        "to be used in report query SQL."
    )
    depre_account_type = fields.Many2one(
        'account.account.type',
        string='Account Type for Depre.',
        required=True,
        help="Define account type for depreciation account, "
        "to be used in report query SQL."
    )
    results = fields.Many2many(
        'account.asset',
        string='Results',
        compute='_compute_results',
        help='Use compute fields, so there is nothing store in database',
    )

    @api.onchange('date_range_id')
    def _onchange_date_range_id(self):
        self.date_from = self.date_range_id.date_start
        self.date_to = self.date_range_id.date_end

    @api.model
    def _domain_to_where_str(self, domain):
        """ Helper Function for better performance """
        # python v.3+ used str 'instead' of 'basestring'
        where_dom = [" %s %s %s " % (x[0], x[1], isinstance(x[2], str)
                     and "'%s'" % x[2] or x[2]) for x in domain]
        where_str = 'and'.join(where_dom)
        return where_str

    @api.multi
    def _compute_results(self):
        self.ensure_one()
        dom = []
        # Prepare DOM to filter assets
        # if self.asset_status_draft:
        #     status += ['draft']
        # if self.asset_status_open:
        #     status += ['open']
        # if self.asset_status_close:
        #     status += ['close']
        # if self.asset_status_removed:
        #     status += ['removed']
        if self.asset_ids:
            dom += [('id', 'in', tuple(self.asset_ids.ids + [0]))]
        if self.asset_profile_ids:
            dom += [('profile_id', 'in',
                    tuple(self.asset_profile_ids.ids + [0]))]
        if self.asset_status:
            dom += [('state', '=', tuple(self.asset_status))]
        # Prepare fixed params
        date_start = self.date_from
        date_end = self.date_to
        fiscalyear_start = self.date_from.strftime('%Y')
        accum_depre_account_ids = self.env['account.account'].search(
            [('user_type_id', '=', self.accum_depre_account_type.id)]).ids
        depre_account_ids = self.env['account.account'].search(
            [('user_type_id', '=', self.depre_account_type.id)]).ids
        where_str = self._domain_to_where_str(dom)
        if where_str:
            where_str = 'and ' + where_str
        self._cr.execute("""
            select a.*, id asset_id,
                -- depreciation
                (select coalesce(sum(debit-credit), 0.0)
                 from account_move_line ml
                 where account_id in %s  -- depreciation account
                 and ml.date between %s and %s
                 and asset_id = a.id) depreciation,
                -- accumulated_cf
                (select coalesce(sum(credit-debit), 0.0)
                 from account_move_line ml
                 where account_id in %s  -- accumulated account
                 and ml.date <= %s -- date end
                 and asset_id = a.id) accumulated_cf,
                -- accumulated_bf
                case when SUBSTRING(a.date_start :: text,1,4) >= %s
                then 0 else
                (select a.purchase_value - coalesce(sum(credit-debit), 0.0)
                 from account_move_line ml
                 where account_id in %s  -- accumulatedp account
                 and SUBSTRING(ml.date :: text,1,4) < %s -- fiscalyear start
                 and asset_id = a.id) end accumulated_bf
            from
            account_asset a
            where (a.state != 'close' or a.value_depreciated != 0)
        """ + where_str + "order by profile_id",
                         (tuple(depre_account_ids), date_start, date_end,
                          tuple(accum_depre_account_ids), date_end,
                          fiscalyear_start,
                          tuple(accum_depre_account_ids), fiscalyear_start))
        asset_results = self._cr.dictfetchall()
        ReportLine = self.env['account.asset']
        # Result = self.env['account.asset']
        # self.results = Result.search(dom)
        for line in asset_results:
            self.results += ReportLine.new(line)

    @api.multi
    def _compute_date_filter(self):
        self.date_filter = _(
            ('ตั้งแต่วันที่ %s ถึง %s') % (self.date_from, self.date_to))

    # @api.multi
    # def action_get_report(self):
    #     action = self.env.ref(
    #         'cmo_account_report.action_xlsx_report_asset_form')
    #     action.sudo().write({'context': {'wizard_id': self.id}})
    #     return super(XLSXReportAsset, self).action_get_report()

    @api.onchange('asset_status')
    def _onchange_asset_status(self):
        if self.asset_status:
            return {'domain': {'asset_ids': [
                ('state', '=', self.asset_status)]}}
        else:
            return {'domain': {'asset_ids': []}}
