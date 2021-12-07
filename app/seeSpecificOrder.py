from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, BooleanField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.Carts import Cartesian
from .models.product_summary import ProductSummary
from .models.purchase import Purchase
from .models.product_sellers import ProductSeller
from .models.product import Product
from .models.messages import *


from flask import Blueprint
bp = Blueprint('seeSpecificOrder', __name__)


@bp.route('/seeSpecificOrder/<oid>', methods=['GET', 'POST'])
def seeSpecificOrder(oid):
    unread = num_unread()
    order = Cartesian.getOrderInfo(oid)
    time = Cartesian.getOTime(oid)[0]
    address = Cartesian.getOAddress(oid)[0]
    totalPrice = 0
    for i in range(len(order)):
        print(order[i][3])
        totalPrice += order[i][3]*order[i][2]
        prod = ProductSummary.get(order[i][0])
        seller = ProductSeller.get_all(order[i][0])[0].id
        order[i][1] = prod.name
        order[i].append(seller)
    return render_template('seeSpecificOrder.html', title='Update Cart', unread = unread, orders = order, oid = oid,time=time,totalPrice = totalPrice, address= address)