from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.product import Product


from flask import Blueprint
bp = Blueprint('seller_inventory', __name__)

class UpdateAmountForm(FlaskForm):
    quantity_available = IntegerField(_l('New Quantity'), validators=[DataRequired()]) #include a validator to ensure its positive. Figure out removal of product
    submit = SubmitField(_l('Update Quantity Available'))


@bp.route('/seller_inventory')
def seller_inventory():
   inventory = User.get_products(current_user.id) 
   return render_template('seller_inventory.html', inventory=inventory)
 
@bp.route('/<product>', methods=['GET', 'POST'])
def update_product(product):
   print(product)
   inventory = User.get_products(current_user.id) 
   form = UpdateAmountForm()
   if form.validate_on_submit():
      if Product.update_quantity(product.id, form.quant):
         flash('Quantity Updated')
         return render_template('seller_inventory.html', inventory=inventory)
      else:
         print("issue")
         flash('Issue With Quantity Updated')
   else:
      print(form)
      print('Form not validated')
   return render_template('productUpdate.html', product=product, form = form)

