from flask import render_template
from flask_login import current_user
import datetime
from flask_sqlalchemy import BaseQuery
from .models.product_summary import ProductSummary
from .models.purchase import Purchase
from .models.product_sellers import ProductSeller
from .models.product import Product
from flask import Blueprint
bp = Blueprint('productSummary', __name__)

@bp.route('/product/<pid>')
def product_summaries(pid):
    # get all available products for sale:
    products = ProductSummary.get_all(pid)
    sellers = ProductSeller.get_all(pid)
    bought = False
    sold = False
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        for purchase in purchases:
            if purchase.pid == int(pid):
                bought = True
        for seller in sellers:
            if seller.id == current_user.id:
                sold = True
    return render_template('product_summary.html',
                           curr_product=products[0],
                           reviews = products,
                           all_sellers = sellers,
                           bought_product = bought,
                           sold_product = sold,
                            pid = pid)
