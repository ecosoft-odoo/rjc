pg_user="odoo"
prod_db="RJC"
psql="psql -U $pg_user -d $prod_db"

# Sales
$psql -c "delete from sale_order";
$psql -c "delete from sale_order_line";
$psql -c "delete from sale_order_template";

# Purchase
$psql -c "delete from purchase_order";
$psql -c "delete from purchase_order_line";

# MRP
$psql -c "delete from mrp_bom";
$psql -c "delete from mrp_production";

# Stock
$psql -c "delete from stock_inventory";
$psql -c "delete from stock_picking";
$psql -c "delete from stock_move";
$psql -c "delete from stock_quant";

# Accounting
$psql -c "delete from account_partial_reconcile";
$psql -c "delete from account_move_line";
$psql -c "delete from account_invoice";
$psql -c "delete from account_move";
$psql -c "delete from account_invoice_line_tax";
$psql -c "delete from account_invoice_tax";
$psql -c "delete from account_tax";
$psql -c "delete from withholding_tax_cert";
$psql -c "delete from account_payment";
$psql -c "delete from account_account";
$psql -c "delete from account_bank_statement";
$psql -c "delete from account_bank_statement_line";
$psql -c "delete from account_analytic_line";
$psql -c "delete from account_analytic_account";
$psql -c "delete from account_billing";

# Expense
$psql -c "delete from hr_expense";
$psql -c "delete from hr_expense_sheet";

# Asset
$psql -c "delete from account_asset";

# Stock Warehouse
$psql -c "delete from stock_warehouse_orderpoint";

# Product
$psql -c "delete from product_template";
$psql -c "delete from product_supplierinfo";
$psql -c "delete from product_product";
