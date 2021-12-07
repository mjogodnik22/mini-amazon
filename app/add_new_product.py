from flask import render_template, redirect, url_for, flash, request,current_app
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Regexp, Optional
from flask_babel import _, lazy_gettext as _l
from werkzeug.utils import secure_filename
from .models.product import Product
from .models.messages import *
from flask_wtf.file import FileField, FileRequired
import os
from flask import Blueprint
bp = Blueprint('add_new_product', __name__)


class NewProductForm(FlaskForm):
    name = StringField(_l('Product Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    category = SelectField(_l('Category'), validators=[DataRequired()])
    price = DecimalField(_l('Price'), validators=[DataRequired()])
    quantity_available = IntegerField(_l('Quantity Available'), validators=[DataRequired()])
    image = FileField(_l('Image File Upload (Optional)'), validators=[Optional()])
    image2 = StringField(_l('Image URL Upload (Optional)'), validators = [Optional(),Regexp(regex = r'(?:http\:|https\:)?\/\/.*?\.(?:png|jpg)')])
    submit = SubmitField(_l('Submit'))


        
@bp.route('/new_product', methods=['GET', 'POST'])
def new_product():
    unread = num_unread()
    form = NewProductForm()
    form.category.choices = Product.get_categories()
    if form.validate_on_submit():
        f = form.image.data
        if f != None:
            filename = secure_filename(f.filename)
            f.save(os.path.join(
                current_app.root_path, 'static', 'images',filename))
            image_file ='/' + os.path.join('static', 'images',filename)
        else:
            image_file = form.image2.data
        if Product.make_new_product(form.name.data,
                         form.description.data,
                         form.category.data,
                         form.price.data,
                         form.quantity_available.data,
                         image_file):
            flash('Congratulations, you just added a product!')
            return redirect(url_for('productPage.productPage'))
    return render_template('add_product_for_sale.html', title='Add Product', unread = unread, form=form)