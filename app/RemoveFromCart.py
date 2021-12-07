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
bp = Blueprint('removeFromCart', __name__)

class UpdateCart(FlaskForm):
    confirm = SelectField(_l('You want more? Fewer? None at all?'), choices = [(1,"Add"),(2,"Subtract"),(3,"Delete")],validators=[DataRequired()])
    amount = StringField(_l('Please Enter the magnitude of change (Not Necessary for Deletion.'))
    submit = SubmitField(_l('Make The Adjustment'))

@bp.route('/updateCart/<pid>', methods=['GET', 'POST'])
def updateCart(pid):
    unread = num_unread()
    ido = Cartesian.getspecific(current_user.id,pid)
    product = ProductSummary.get(pid)
    producto = Product.get(pid)
    avail = producto.quantity_available
    amount = ido.quantity
    avail -= amount
    totalPrice = producto.price * amount
    form12 = UpdateCart()
    addorsub = False
    if form12.validate_on_submit:
        if form12.confirm.data == '1':
            if form12.amount.data == '':
                flash("Please Select a Quantity to add")
                return redirect(url_for('removeFromCart.updateCart', uid = current_user.id, pid = pid))
            elif int(form12.amount.data) <= int(avail):
                Cartesian.addToCartAgain(current_user.id,pid,int(form12.amount.data),product.price)
                return redirect(url_for('Cart.myCart', uid = current_user.id))
            else:
                flash("The seller does not have enough to satisfy this order. Please place fewer items into your cart")
        if form12.confirm.data == '2':
            if form12.amount.data == '':
                flash("Please Select a Quantity to subtract")
            elif int(form12.amount.data) > amount:
                flash("You can't delete what you don't have! Please choose delete to remove all items from your cart.")
            else:
                if int(form12.amount.data) == amount:
                    Cartesian.removeFromCart(pid,current_user.id)
                    return redirect(url_for('Cart.myCart', uid = current_user.id))
                Cartesian.subFromCart(current_user.id,pid,int(form12.amount.data),product.price)
                return redirect(url_for('Cart.myCart', uid = current_user.id))
        if form12.confirm.data == '3':
            Cartesian.removeFromCart(pid,current_user.id)
            return redirect(url_for('Cart.myCart', uid = current_user.id))

    return render_template('removeFromCart.html', title='Update Cart', form=form12,
                            prod = product,
                            currcart = ido,
                            avail=avail,
                            amt = amount,
                            tpr = totalPrice,
                            unread=unread)