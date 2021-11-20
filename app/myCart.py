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

class placeOrder(FlaskForm):
    confirm = SelectField(_l('Confirm'), choices = [(1,"I do not confirm"),(2,"I confirm")],validators=[DataRequired()])
    submit = SubmitField(_l('Place Order'))

@bp.route('/myCart',methods=['GET', 'POST'])
def myCart():
    form11 = placeOrder()
    empty = False
    if current_user.is_authenticated:
        balance = User.get(current_user.id).balance
        totalcost = 0
        ido = Cartesian.get(current_user.id)
        if ido is None:
            empty = True
            return render_template('myCart.html',
                            form = form11,
                            currcart = ido,
                            empty = empty,
                            balance = balance)
        for element in ido:
            totalcost += element.priceatpurchase
        hasEnough = True
        if balance < totalcost:
            hasEnough = False
        if form11.validate_on_submit:
            if form11.confirm.data == '2' and hasEnough:
                albert = Cartesian.placeOrder(current_user.id)
                if User.update_balance(current_user.id,
                                   int(balance),
                                   int(totalcost),
                                   "wdr"):
                    flash('Your balance has been updated!')
                for gangarang in ido:
                    Cartesian.addtoOrder(albert,gangarang.pid,gangarang.quantity,gangarang.priceatpurchase)
                    Product.adjustWithOrder(gangarang.quantity)
                    Cartesian.removeFromCart(gangarang.pid,current_user.id)
                return redirect(url_for('BuyerOrders.buyer_orders', uid = current_user.id))

        
       
    return render_template('myCart.html',
                            form = form11,
                            currcart = ido,
                            empty = empty,
                            balance = balance,
                            totalcost=totalcost,
                            hasEnough=hasEnough)