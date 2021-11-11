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


from flask import Blueprint
bp = Blueprint('removeFromCart', __name__)

class UpdateCart(FlaskForm):
    confirm = SelectField(_l('Please Confirm'), choices = [(1,"I do not confirm"),(2,"I confirm")],validators=[DataRequired()])
    submit = SubmitField(_l('Remove From Cart'))

@bp.route('/updateCart/<pid>', methods=['GET', 'POST'])
def updateCart(pid):
    ido = Cartesian.getspecific(current_user.id,pid)
    product = ProductSummary.get(pid)
    form12 = UpdateCart()
    if form12.validate_on_submit:
        if form12.confirm.data == '2':
            Cartesian.removeFromCart(pid,current_user.id)
            flash("Successfully removed from Cart!")
            return redirect(url_for('Cart.myCart', uid = current_user.id))

    return render_template('removeFromCart.html', title='Update Cart', form=form12, prod = product,currcart = ido)