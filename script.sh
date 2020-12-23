pg_container="postgres"
pg_user="odoo"
prod_db="TGI"
psql="docker exec -it $pg_container psql -U $pg_user $prod_db"

# Sales
$psql -c "delete from sale_order";
$psql -c "delete from sale_order_line";

# Purchase
$psql -c "delete from purchase_order";
$psql -c "delete from purchase_order_line";

# Point of sale
$psql -c "delete from pos_order";
$psql -c "delete from pos_session";

# MRP
$psql -c "delete from mrp_production";
$psql -c "delete from mrp_unbuild";

# Stock
$psql -c "delete from stock_inventory";
$psql -c "delete from stock_picking";
$psql -c "delete from stock_move";
$psql -c "delete from stock_scrap";
$psql -c "delete from stock_move_line";

# serial number
$psql -c "delete from stock_quant";
$psql -c "delete from stock_production_lot";

# Expense
$psql -c "delete from hr_expense_sheet";
$psql -c "delete from hr_expense";

# Accounting
$psql -c "delete from account_invoice_reimbursable";
$psql -c "delete from account_payment_intransit_deduction";
$psql -c "delete from account_payment_intransit_line";
$psql -c "delete from account_payment_intransit";
$psql -c "delete from account_partial_reconcile";
$psql -c "delete from account_move_line";
$psql -c "delete from account_invoice_line_tax";
$psql -c "delete from account_invoice_tax";
$psql -c "delete from account_invoice";
$psql -c "delete from account_move";
$psql -c "delete from tax_adjustments_wizard";
$psql -c "delete from withholding_tax_cert";
$psql -c "delete from account_payment";
$psql -c "delete from account_bank_statement";
$psql -c "delete from account_analytic_line";
$psql -c "delete from account_analytic_account";
$psql -c "delete from account_billing";

# Asset
$psql -c "delete from account_asset";
