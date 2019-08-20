# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

import time

from odoo.tests.common import SavepointCase
from datetime import date


class TestAssetRegisterReport(SavepointCase):

    def setUp(self):
        super(TestAssetRegisterReport, self).setUp()
        self.asset_model = self.env['account.asset']
        self.asset_profile_model = self.env['account.asset.profile']
        self.account_account_model = self.env['account.account']
        self.accum_depre_type = self.env['account.account.type'].create({
            'name': 'Accumulated Depreciation',
            'type': 'other',
        })
        self.depre_type = self.env['account.account.type'].create({
            'name': 'Depreciation',
            'type': 'other',
        })
        self.data_type = self.env['date.range.type'].create({
            'name': 'Fiscal year',
            'company_id': False,
            'allow_overlap': False
        })

        self.date_range_id = self.env['date.range'].create({
            'name': 'FS2019',
            'date_start': '2019-01-01',
            'date_end': '2019-12-31',
            'type_id': self.data_type.id,
        })
        self.expenses_journal = self.env['account.journal'].create({
            'name': 'Test expense journal',
            'type': 'purchase',
            'code': 'EXP',
        })
        self.account_asset = self.account_account_model.search([
            ('user_type_id', '=',
                self.env.ref('account.data_account_type_fixed_assets').id)],
                limit=1)
        if not self.account_asset:
            self.account_asset = self.account_account_model.create({
                'code': 'asset',
                'name': 'Fixed Asset',
                'user_type_id':
                    self.env.ref('account.data_account_type_fixed_assets').id,
            })

        self.account_accum_depre = self.account_account_model.search(
            [('user_type_id', '=', self.accum_depre_type.id)], limit=1)
        if not self.account_accum_depre:
            self.account_accum_depre = self.account_account_model.create({
                'code': 'accumdepre',
                'name': 'Accumulated Depreciation',
                'user_type_id': self.accum_depre_type.id,
            })

        self.account_depreciation = self.account_account_model.search(
            [('user_type_id', '=', self.depre_type.id)], limit=1)
        if not self.account_depreciation:
            self.account_depreciation = self.account_account_model.create({
                'code': 'depre',
                'name': 'Depreciation',
                'user_type_id': self.depre_type.id,
            })
        self.asset_view = self.asset_model.create({
            'name': 'View',
            'type': 'view',
            'purchase_value': 0,
        })
        self.asset_profile_id = self.asset_profile_model.create({
            'name': 'Equipment',
            'parent_id': self.asset_view.id,
            'journal_id': self.expenses_journal.id,
            'account_asset_id': self.account_asset.id,
            'account_depreciation_id': self.account_accum_depre.id,
            'account_expense_depreciation_id': self.account_depreciation.id,
            'method': 'linear',
            'method_time': 'year',
            'method_number': 5,
            'method_period': 'year',
        })
        self.asset_id = self.asset_model.search(
            [('type', '!=', 'view')], limit=1)
        if not self.asset_id:
            self.asset_id = self.asset_model.create({
                'name': 'Table',
                'parent_id': self.asset_view.id,
                'type': 'normal',
                'purchase_value': 100000,
                'salvage_value': 1000,
                'date_start': '2019-01-01',
                'profile_id': self.asset_profile_id.id,
            })
        # self.before_previous_fy_year = fields.Date.from_string('2014-05-05')
        # self.previous_fy_date_start = fields.Date.from_string('2015-01-01')
        # self.previous_fy_date_end = fields.Date.from_string('2015-12-31')
        # self.fy_date_start = fields.Date.from_string('2016-01-01')
        # self.fy_date_end = fields.Date.from_string('2016-12-31')
        # self.receivable_account = self.env['account.account'].search([
        #     ('user_type_id.name', '=', 'Receivable')
        #     ], limit=1)
        # self.income_account = self.env['account.account'].search([
        #     ('user_type_id.name', '=', 'Income')
        #     ], limit=1)
        # self.unaffected_account = self.env['account.account'].search([
        #     (
        #         'user_type_id',
        #         '=',
        #         self.env.ref('account.data_unaffected_earnings').id
        #     )], limit=1)

    def _get_report_lines(self, with_partners=False):
        company = self.env.ref('base.main_company')
        general_ledger = self.env['report_general_ledger'].create({
            'date_from': self.fy_date_start,
            'date_to': self.fy_date_end,
            'only_posted_moves': True,
            'hide_account_at_0': False,
            'company_id': company.id,
            'fy_start_date': self.fy_date_start,
            })
        general_ledger.compute_data_for_report(
            with_line_details=True, with_partners=with_partners
        )
        lines = {}
        report_account_model = self.env['report_general_ledger_account']
        lines['receivable'] = report_account_model.search([
            ('report_id', '=', general_ledger.id),
            ('account_id', '=', self.receivable_account.id),
        ])
        lines['income'] = report_account_model.search([
            ('report_id', '=', general_ledger.id),
            ('account_id', '=', self.income_account.id),
        ])
        lines['unaffected'] = report_account_model.search([
            ('report_id', '=', general_ledger.id),
            ('account_id', '=', self.unaffected_account.id),
        ])
        if with_partners:
            report_partner_model = self.env[
                'report_general_ledger_partner'
            ]
            lines['partner_receivable'] = report_partner_model.search([
                ('report_account_id', '=', lines['receivable'].id),
                ('partner_id', '=', self.env.ref('base.res_partner_12').id),
            ])
        return lines

    # def test_01_account_balance(self):
    #     # Generate the general ledger line
    #     lines = self._get_report_lines()
    #     self.assertEqual(len(lines['receivable']), 0)
    #     self.assertEqual(len(lines['income']), 0)
    #
    #     # Add a move at the previous day of the first day of fiscal year
    #     # to check the initial balance
    #     self._add_move(
    #         date=self.previous_fy_date_end,
    #         receivable_debit=1000,
    #         receivable_credit=0,
    #         income_debit=0,
    #         income_credit=1000
    #     )
    #
    #     # Re Generate the general ledger line
    #     lines = self._get_report_lines()
    #     self.assertEqual(len(lines['receivable']), 1)
    #     self.assertEqual(len(lines['income']), 0)
    #
    #     # Check the initial and final balance
    #     self.assertEqual(lines['receivable'].initial_debit, 1000)
    #     self.assertEqual(lines['receivable'].initial_credit, 0)
    #     self.assertEqual(lines['receivable'].initial_balance, 1000)
    #     self.assertEqual(lines['receivable'].final_debit, 1000)
    #     self.assertEqual(lines['receivable'].final_credit, 0)
    #     self.assertEqual(lines['receivable'].final_balance, 1000)
    #
    #     # Add reversale move of the initial move the first day of fiscal year
    #     # to check the first day of fiscal year is not used
    #     # to compute the initial balance
    #     self._add_move(
    #         date=self.fy_date_start,
    #         receivable_debit=0,
    #         receivable_credit=1000,
    #         income_debit=1000,
    #         income_credit=0
    #     )
    #
    #     # Re Generate the general ledger line
    #     lines = self._get_report_lines()
    #     self.assertEqual(len(lines['receivable']), 1)
    #     self.assertEqual(len(lines['income']), 1)
    #
    #     # Check the initial and final balance
    #     self.assertEqual(lines['receivable'].initial_debit, 1000)
    #     self.assertEqual(lines['receivable'].initial_credit, 0)
    #     self.assertEqual(lines['receivable'].initial_balance, 1000)
    #     self.assertEqual(lines['receivable'].final_debit, 1000)
    #     self.assertEqual(lines['receivable'].final_credit, 1000)
    #     self.assertEqual(lines['receivable'].final_balance, 0)
    #
    #     self.assertEqual(lines['income'].initial_debit, 0)
    #     self.assertEqual(lines['income'].initial_credit, 0)
    #     self.assertEqual(lines['income'].initial_balance, 0)
    #     self.assertEqual(lines['income'].final_debit, 1000)
    #     self.assertEqual(lines['income'].final_credit, 0)
    #     self.assertEqual(lines['income'].final_balance, 1000)
    #
    #     # Add another move at the end day of fiscal year
    #     # to check that it correctly used on report
    #     self._add_move(
    #         date=self.fy_date_end,
    #         receivable_debit=0,
    #         receivable_credit=1000,
    #         income_debit=1000,
    #         income_credit=0
    #     )
    #
    #     # Re Generate the general ledger line
    #     lines = self._get_report_lines()
    #     self.assertEqual(len(lines['receivable']), 1)
    #     self.assertEqual(len(lines['income']), 1)
    #
    #     # Check the initial and final balance
    #     self.assertEqual(lines['receivable'].initial_debit, 1000)
    #     self.assertEqual(lines['receivable'].initial_credit, 0)
    #     self.assertEqual(lines['receivable'].initial_balance, 1000)
    #     self.assertEqual(lines['receivable'].final_debit, 1000)
    #     self.assertEqual(lines['receivable'].final_credit, 2000)
    #     self.assertEqual(lines['receivable'].final_balance, -1000)
    #
    #     self.assertEqual(lines['income'].initial_debit, 0)
    #     self.assertEqual(lines['income'].initial_credit, 0)
    #     self.assertEqual(lines['income'].initial_balance, 0)
    #     self.assertEqual(lines['income'].final_debit, 2000)
    #     self.assertEqual(lines['income'].final_credit, 0)
    #     self.assertEqual(lines['income'].final_balance, 2000)
    #
    # def test_02_partner_balance(self):
    #     # Generate the general ledger line
    #     lines = self._get_report_lines(with_partners=True)
    #     self.assertEqual(len(lines['partner_receivable']), 0)
    #
    #     # Add a move at the previous day of the first day of fiscal year
    #     # to check the initial balance
    #     self._add_move(
    #         date=self.previous_fy_date_end,
    #         receivable_debit=1000,
    #         receivable_credit=0,
    #         income_debit=0,
    #         income_credit=1000
    #     )
    #
    #     # Re Generate the general ledger line
    #     lines = self._get_report_lines(with_partners=True)
    #     self.assertEqual(len(lines['partner_receivable']), 1)
    #
    #     # Check the initial and final balance
    #     self.assertEqual(lines['partner_receivable'].initial_debit, 1000)
    #     self.assertEqual(lines['partner_receivable'].initial_credit, 0)
    #     self.assertEqual(lines['partner_receivable'].initial_balance, 1000)
    #     self.assertEqual(lines['partner_receivable'].final_debit, 1000)
    #     self.assertEqual(lines['partner_receivable'].final_credit, 0)
    #     self.assertEqual(lines['partner_receivable'].final_balance, 1000)
    #
    #     # Add reversale move of the initial move the first day of fiscal year
    #     # to check the first day of fiscal year is not used
    #     # to compute the initial balance
    #     self._add_move(
    #         date=self.fy_date_start,
    #         receivable_debit=0,
    #         receivable_credit=1000,
    #         income_debit=1000,
    #         income_credit=0
    #     )
    #
    #     # Re Generate the general ledger line
    #     lines = self._get_report_lines(with_partners=True)
    #     self.assertEqual(len(lines['partner_receivable']), 1)
    #
    #     # Check the initial and final balance
    #     self.assertEqual(lines['partner_receivable'].initial_debit, 1000)
    #     self.assertEqual(lines['partner_receivable'].initial_credit, 0)
    #     self.assertEqual(lines['partner_receivable'].initial_balance, 1000)
    #     self.assertEqual(lines['partner_receivable'].final_debit, 1000)
    #     self.assertEqual(lines['partner_receivable'].final_credit, 1000)
    #     self.assertEqual(lines['partner_receivable'].final_balance, 0)
    #
    #     # Add another move at the end day of fiscal year
    #     # to check that it correctly used on report
    #     self._add_move(
    #         date=self.fy_date_end,
    #         receivable_debit=0,
    #         receivable_credit=1000,
    #         income_debit=1000,
    #         income_credit=0
    #     )
    #
    #     # Re Generate the general ledger line
    #     lines = self._get_report_lines(with_partners=True)
    #     self.assertEqual(len(lines['partner_receivable']), 1)
    #
    #     # Check the initial and final balance
    #     self.assertEqual(lines['partner_receivable'].initial_debit, 1000)
    #     self.assertEqual(lines['partner_receivable'].initial_credit, 0)
    #     self.assertEqual(lines['partner_receivable'].initial_balance, 1000)
    #     self.assertEqual(lines['partner_receivable'].final_debit, 1000)
    #     self.assertEqual(lines['partner_receivable'].final_credit, 2000)
    #     self.assertEqual(lines['partner_receivable'].final_balance, -1000)

    def test_validate_date(self):
        company_id = self.env.ref('base.main_company')
        company_id.write({
            'fiscalyear_last_day': 31,
            'fiscalyear_last_month': 12,
        })
        user = self.env.ref('base.user_root').with_context(
            company_id=company_id.id)
        wizard = self.env['asset.register.report.wizard'].with_context(
            user=user.id
        )
        self.assertEqual(wizard._init_date_from(),
                         time.strftime('%Y') + '-01-01')

    def test_validate_date_range(self):
        wizard = self.env['asset.register.report.wizard'].create({
            'date_range_id': self.date_range_id.id,
            'accum_depre_account_type': self.accum_depre_type.id,
            'depre_account_type': self.depre_type.id,
        })
        wizard.onchange_date_range_id()
        self.assertEqual(wizard.date_from, date(2019, 1, 1))
        self.assertEqual(wizard.date_to, date(2019, 12, 31))

    def test_asset_report(self):
        wizard = self.env['asset.register.report.wizard'].create({
            'date_range_id': self.date_range_id.id,
            'accum_depre_account_type': self.accum_depre_type.id,
            'depre_account_type': self.depre_type.id,
        })
        wizard.button_export_html()
        wizard.button_export_pdf()
        wizard.button_export_xlsx()
