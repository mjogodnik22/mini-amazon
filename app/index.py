from flask import render_template, redirect, url_for
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.messages import *
from .models.generic_queries import make_seller, is_seller

from flask import Blueprint
bp = Blueprint('index', __name__)
make_seller_bp = Blueprint('make_seller_pg', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all_page()
    num_unread = None
    # find the products current user has bought:
    if current_user.is_authenticated:
        messages = get_messages()
        num_unread = sum([1 for k in messages if k.msg_read == 'Unread'])
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        inSeller = is_seller()
    else:
    # render the page by adding information to the index.html file
        purchases = None
        inSeller = None

    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           num_unread = num_unread,
                           s = inSeller)

@make_seller_bp.route("/make_seller_pg", methods=['GET', 'POST'])
def make_seller_page():
    make_seller()
    return redirect(url_for('index.index'))