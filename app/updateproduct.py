from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from werkzeug.datastructures import MultiDict

from .models.product import Product
from .models.product_summary import ProductSummary


from flask import Blueprint
bp = Blueprint('updateproduct', __name__)

class UpdateProductForm(FlaskForm):
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    category = SelectField(_l('Category'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), validators=[DataRequired()])
    quantity_available = IntegerField(_l('Quantity Available'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

@bp.route('/updateProductPage/<pid>', methods=['GET', 'POST'])
def updateProductPage(pid):
    form = UpdateProductForm()
    form.category.choices = Product.get_categories()
    if request.method == 'GET':
        curr_product = ProductSummary.get(pid)
        curr_product_temp = Product.get(pid)  
        form = UpdateProductForm(formdata = MultiDict({
            'name': curr_product.name,
            'description': curr_product.description,
            'category': curr_product.category,
            'price': curr_product.price,
            'quantity_available': curr_product_temp.quantity_available,
        }))
        form.category.choices = Product.get_categories()
    if form.validate_on_submit():
        if Product.update_product(form.name.data,
                         form.description.data,
                         form.category.data,
                         form.price.data,
                         form.quantity_available.data):
            flash('Congratulations, you just updated this product!')
            return redirect(url_for('productSummary.product_summaries', pid = pid))
    return render_template('updateproduct.html', title='Update Product', form=form)