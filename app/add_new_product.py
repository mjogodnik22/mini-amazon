from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.product import Product


from flask import Blueprint
bp = Blueprint('add_new_product', __name__)


class NewProductForm(FlaskForm):
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    category = StringField(_l('Category'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), validators=[DataRequired()])
    quantity_available = IntegerField(_l('Quantity Available'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    # ADD VALIDATOR FOR CATEGORY AND OTHER STUFF


@bp.route('/new_product', methods=['GET', 'POST'])
def new_product():
    form = NewProductForm()
    if form.validate_on_submit():
        if Product.make_new_product(form.name.data,
                         form.description.data,
                         form.category.data,
                         form.price.data,
                         form.quantity_available.data):
            flash('Congratulations, you just added this product!')
            return redirect(url_for('index.index'))
    return render_template('add_product_for_sale.html', title='Add Product', form=form)