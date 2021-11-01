from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.product_summary import ProductSummary
from .models.product import Product
from .models.purchase import Purchase
from .models.product_sellers import ProductSeller

from flask import Blueprint
bp = Blueprint('productPage', __name__)

#pagination testing
#temp = Product.get_test().yield_per(2).partitions()
#@bp.route('/products/home',methods=['GET'])
#def view(page=1):
#    # get all available products for sale:
#    products = Product.get_all(True)
#    # find the products current user has bought:
#    # render the page by adding information to the index.html file
#    return render_template('index.html',
#                           avail_products=products)

class NewFilterForm(FlaskForm):
    category = SelectField(_l('Filter by Category'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    
class NewSortForm(FlaskForm):
    key = SelectField(_l('Sort by Key'), choices = [('name','Name'),('pid','ID'),('price','Price'),('pid','Clear Sort')],validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


#looking into a better way of implementing
#weird stuff with none that I will remove the hardcode for when I figure it out
@bp.route('/products',defaults={'sort_by': 'pid', 'filter_by': None },methods=['GET', 'POST'])
@bp.route('/products/<sort_by>',defaults={'filter_by': None },methods=['GET', 'POST'])
@bp.route('/products/<sort_by>/<filter_by>',methods=['GET', 'POST'])
def productPage(sort_by = 'pid',filter_by = None):
    # get all available products for sale:
    if filter_by == 'None':
        filter_by = None
    products = Product.get_all(sort_by = sort_by, filter_by = filter_by)
    filterform = NewFilterForm()
    filter_categories = Product.get_categories()
    filter_categories.append((None, 'Clear Filter'))
    filterform.category.choices = filter_categories
    sortform = NewSortForm()
    if filterform.validate_on_submit():
        return redirect(url_for('productPage.productPage', sort_by = sort_by, filter_by = filterform.category.data))
    if sortform.validate_on_submit():
        return redirect(url_for('productPage.productPage', sort_by = sortform.key.data, filter_by = filter_by))
    return render_template('productpage.html',form1=filterform, form2 = sortform, avail_products = products)
