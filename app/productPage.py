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

class NewPageForm(FlaskForm):
    page_val = IntegerField(_l('Jump to Page'),validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

class NewSearchForm(FlaskForm):
    search_val = StringField(_l('Search:'),validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
#looking into a better way of implementing
#weird stuff with none that I will remove the hardcode for when I figure it out
#this will be cleaned later
@bp.route('/products',defaults={'page_num' : 1, 'sort_by': 'pid', 'filter_by': 'None' },methods=['GET', 'POST'])
@bp.route('/products/<page_num>',defaults={'sort_by': 'pid', 'filter_by': 'None' },methods=['GET', 'POST'])
@bp.route('/products/<page_num>/<sort_by>',defaults={'filter_by': 'None' },methods=['GET', 'POST'])
@bp.route('/products/<page_num>/<sort_by>/<filter_by>',methods=['GET', 'POST'])
def productPage(page_num = 1, sort_by = 'pid',filter_by = 'None'):
    # get all available products for sale:
    if filter_by == 'None':
        filter_by = None
    page_num = int(page_num)
    products = Product.get_all_page(page_num = page_num, sort_by = sort_by, filter_by = filter_by)
    filterform = NewFilterForm()
    filter_categories = Product.get_categories()
    filter_categories.append((None, 'Clear Filter'))
    filterform.category.choices = filter_categories
    sortform = NewSortForm()
    pageform = NewPageForm()
    searchform = NewSearchForm()
    prev_page = page_num - 1
    #only need to compute page count on addition of a product, will look into this
    next_page = page_num + 1
    max_pages = Product.get_page_count()
    
    if next_page > max_pages:
        next_page = 0
    if filterform.validate_on_submit():
        return redirect(url_for('productPage.productPage', page_num = page_num, sort_by = sort_by, filter_by = filterform.category.data))
    if sortform.validate_on_submit():
        return redirect(url_for('productPage.productPage', page_num = page_num, sort_by = sortform.key.data, filter_by = filter_by))
    if pageform.validate_on_submit():
        if pageform.page_val.data < 1 or pageform.page_val.data > max_pages:
            flash('Please input a page number between 1 and {num1}!'.format(num1 = max_pages))
            return redirect(url_for('productPage.productPage', page_num = page_num, sort_by = sort_by, filter_by = filter_by))
        else:
            return redirect(url_for('productPage.productPage', page_num = pageform.page_val.data, sort_by = sort_by, filter_by = filter_by))
    if searchform.validate_on_submit():
        return redirect(url_for('productPage.productSearchPage', page_num = page_num, query = searchform.search_val.data))
    
    return render_template('productpage.html',form1=filterform, form2 = sortform, form3 = pageform,form4 = searchform,
                           avail_products = products, next_page=next_page, prev_page=prev_page, curr_sort = sort_by, curr_filter = filter_by)

@bp.route('/products_search',defaults={'query' :'', 'page_num' : 1},methods=['GET', 'POST'])
@bp.route('/products_search/<query>',defaults={'page_num': 1 },methods=['GET', 'POST'])
@bp.route('/products_search/<query>/<page_num>',methods=['GET', 'POST'])
def productSearchPage(page_num = 1, query = ""):
    # get all available products for sale:
    page_num = int(page_num)
    products = Product.get_all_search(page_num = page_num, search_query = query)
    prev_page = page_num - 1
    #only need to compute page count on addition of a product, will look into this
    next_page = page_num + 1
    max_pages = Product.get_page_count()
    pageform = NewPageForm()
    if next_page > max_pages:
        next_page = 0
    if pageform.validate_on_submit():
        if pageform.page_val.data < 1 or pageform.page_val.data > max_pages:
            flash('Please input a page number between 1 and {num1}!'.format(num1 = max_pages))
            return redirect(url_for('productPage.productSearchPage', page_num = page_num, query = query))
        else:
            return redirect(url_for('productPage.productSearchPage', page_num = pageform.page_val.data,query = query))
    
    return render_template('productsearchpage.html',form1= pageform,
                           avail_products = products, next_page=next_page, prev_page=prev_page)