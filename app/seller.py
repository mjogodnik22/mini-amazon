from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.generic_queries import *


from flask import Blueprint
seller_inventory_bp = Blueprint('seller_inventory', __name__)
seller_orders_bp = Blueprint('seller_orders', __name__)
seller_order_details_bp = Blueprint('seller_order_details', __name__)

@seller_inventory_bp.route('/seller_inventory')
def seller_inventory():
   inventory = User.get_products(current_user.id) 
   return render_template('seller_inventory.html', inventory=inventory)

@seller_orders_bp.route('/seller_orders')
def seller_orders():
   orders = get_sellers_orders() 
   return render_template('seller_orders.html', orders=orders)

@seller_order_details_bp.route('/seller_order_details/<oid>')
def seller_order_details(oid):
   orderer_info = get_order_purchase_details(oid)
   purchases = get_sellers_order_details(oid)
   return render_template('seller_order_details.html', purchases=purchases, orderer_info= orderer_info)