from loaders.suppliers_loader import load_suppliers
from loaders.purchase_headers_loader import load_purchase_headers
from loaders.sale_headers_loader import load_sale_headers
from loaders.age_analysis_loader import load_age_analysis
from loaders.payment_lines_loader import load_payment_lines
from loaders.products_loader import load_products
from loaders.customers_loader import load_customers
from loaders.product_categories_loader import load_product_categories
from loaders.product_brands_loader import load_product_brands
from loaders.product_ranges_loader import load_product_ranges
from loaders.trans_types_loader import load_trans_types
from loaders.representatives_loader import load_representatives
from loaders.customer_categories_loader import load_customer_categories
from loaders.customer_regions_loader import load_customer_regions
from loaders.payment_headers_loader import load_payment_headers

# import other loaders...

FILE_PATH = "data/ClearView.xlsx"

load_suppliers(FILE_PATH)
load_purchase_headers(FILE_PATH)
load_sale_headers(FILE_PATH)
load_age_analysis(FILE_PATH)
load_payment_lines(FILE_PATH)
load_products(FILE_PATH)
load_customers(FILE_PATH)
load_product_categories(FILE_PATH)
load_product_brands(FILE_PATH)
load_product_ranges(FILE_PATH)
load_trans_types(FILE_PATH)
load_representatives(FILE_PATH)
load_customer_categories(FILE_PATH)
load_customer_regions(FILE_PATH)
load_payment_headers(FILE_PATH)

# call other loaders...

print("\n✅ All data successfully loaded into MongoDB. ClearVue is ready to roll!")