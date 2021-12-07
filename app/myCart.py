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
from .models.generic_queries import *
from .models.messages import *


from flask import Blueprint
bp = Blueprint('Cart', __name__)

class UpdateInformationForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    submit = SubmitField(_l('Update Information'))



class placeOrder(FlaskForm):
    confirm = SelectField(_l('Confirm'), choices = [(1,"I do not confirm"),(2,"I confirm")],validators=[DataRequired()])
    address = StringField(_l('Address'), validators=[DataRequired()])
    submit = SubmitField(_l('Place Order'))

@bp.route('/myCart',methods=['GET', 'POST'])
def myCart():
    form11 = placeOrder()
    unread = None
    if request.method == 'GET':
        form11= placeOrder(formdata = MultiDict({
            'address': current_user.address
        }))
    empty = False
    if current_user.is_authenticated:
        unread = num_unread()
        balance = User.get(current_user.id).balance
        totalcost = 0
        ido = Cartesian.get(current_user.id)
        save_for_later = Cartesian.getSaved(current_user.id)
        if ido is None:
            empty = True
            return render_template('myCart.html',
                            form = form11,
                            currcart = ido,
                            empty = empty,
                            balance = balance,
                            saved = save_for_later,
                            any_saved = len(save_for_later))
        for element in ido:
            totalcost += element.price*element.quantity
        hasEnough = True
        if balance < totalcost:
            hasEnough = False
        if form11.validate_on_submit:
            if form11.confirm.data == '2' and hasEnough:
                albert = Cartesian.placeOrder(current_user.id, form11.address.data)
                if User.update_balance(current_user.id,
                                   balance,
                                   totalcost,
                                   "wdr"):
                    flash('Your balance has been updated!')
                    for product in ido:
                        seller = who_sells(product.pid)
                        balance = User.get(seller).balance
                        User.update_balance(seller, balance, product.price * product.quantity, "dep")
                for gangarang in ido:
                    Cartesian.addtoOrder(albert,gangarang.pid,gangarang.quantity,gangarang.price)
                    Product.adjustWithOrder(gangarang.pid,gangarang.quantity)
                    Cartesian.removeFromCart(gangarang.pid,current_user.id)
                return redirect(url_for('BuyerOrders.buyer_orders', uid = current_user.id))

        
       
    return render_template('myCart.html',
    unread=unread,
                            form = form11,
                            currcart = ido,
                            empty = empty,
                            balance = balance,
                            totalcost=totalcost,
                            hasEnough=hasEnough,
                            saved = save_for_later,
                            any_saved = len(save_for_later))

@bp.route('/myCart/<uid>/<pid>/<quantity>',methods=['GET', 'POST'])
def saveForLater(uid, pid, quantity):
    save_for_later(uid, pid, quantity)
    return redirect(url_for('Cart.myCart'))

@bp.route('/myCart/delete/<uid>/<pid>',methods=['GET', 'POST'])
def deleteSaved(uid, pid):
    delete_saved(uid, pid)
    return redirect(url_for('Cart.myCart'))

@bp.route('/myCart/add/<uid>/<pid>/<quantity>',methods=['GET', 'POST'])
def addCart(uid, pid, quantity):
    back_in_cart(uid, pid, quantity)
    return redirect(url_for('Cart.myCart'))