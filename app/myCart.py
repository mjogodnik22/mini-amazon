from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from werkzeug.datastructures import MultiDict

from .models.product_summary import ProductSummary
from .models.purchase import Purchase
from .models.product_sellers import ProductSeller
from .models.product import Product

from app.models import Carts
from .models.Carts import Cartesian
from .models.user import User
from .models.product_summary import ProductSummary


from flask import Blueprint
bp = Blueprint('Cart', __name__)

@bp.route('/myCart',methods=['GET', 'POST'])
def myCart():
    empty = False
    if current_user.is_authenticated:
        ido = Cartesian.get(current_user.id)
        if ido is None:
            ido = ["nothing at all","",0,0]
            empty = True
       
    return render_template('myCart.html',
                            currcart = ido,
                            empty = empty)