pg_user="odoo"
prod_db="RJC_TEST"
psql="psql -U $pg_user -d $prod_db"

# Sales
$psql -c "delete from sale_order";
$psql -c "delete from sale_order_line";

# Purchase
$psql -c "delete from purchase_order";
$psql -c "delete from purchase_order_line";

# Stock
$psql -c "delete from stock_inventory";
$psql -c "delete from stock_inventory_line";
$psql -c "delete from stock_picking";
$psql -c "delete from stock_move";
$psql -c "delete from stock_quant";

# foreign key
$psql -c "delete from account_move_line_partner_id_fkey";
$psql -c "delete from account_invoice_move_id_fkey";

# Accounting
$psql -c "delete from account_invoice";
$psql -c "delete from account_invoice_line";
$psql -c "delete from account_invoice_line_tax";
$psql -c "delete from account_invoice_tax";
$psql -c "delete from account_payment";
$psql -c "delete from account_bank_statement";
$psql -c "delete from account_bank_statement_line";
$psql -c "delete from account_move";
$psql -c "delete from account_move_line";
$psql -c "delete from account_analytic_line";
$psql -c "delete from account_analytic_account";
$psql -c "delete from account_billing";
$psql -c "delete from withholding_tax_cert";
$psql -c "delete from withholding_tax_cert_line";

# Asset
$psql -c "delete from account_asset";
$psql -c "delete from account_asset_line";

# Expense
$psql -c "delete from hr_expense";
$psql -c "delete from hr_expense_sheet";

# Partner
$psql -c "delete from res_partner";

#Product
$psql -c "delete from product_template";
$psql -c "delete from product_product";
