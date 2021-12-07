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
from .models.messages import *

from flask import Blueprint
bp = Blueprint('productPage', __name__)

class NewFilterForm(FlaskForm):
    category = SelectField(_l('Filter by Category'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    
class NewSortForm(FlaskForm):
    key = SelectField(_l('Sort by Key'), choices = [('name','Name'),('pid','ID'),('price','Price'),('avg_rating', 'Average Rating'),('pid','Clear Sort')],validators=[DataRequired()])
    direction = SelectField(_l('Sorting Direction'), choices = [('','Ascending'), ('DESC', 'Descending')])
    submit = SubmitField(_l('Submit'))

class NewPageForm(FlaskForm):
    page_val = IntegerField(_l('Jump to Page'),validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

class NewSearchForm(FlaskForm):
    search_val = StringField(_l('Search:'),validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

class NewRangeFilterForm(FlaskForm):
    filter_type =  SelectField(_l('Range Filter By:'), choices = [('price', 'Price'),('avg_rating', 'Average Rating')], validators=[DataRequired()])
    lower = DecimalField(_l('Lower Bound'), validators = [DataRequired()])
    upper = DecimalField(_l('Upper Bound'), validators = [DataRequired()])
    submit = SubmitField(_l('Submit'))

@bp.route('/',defaults={'page_num' : 1, 'sort_by': 'pid', 'filter_by': 'None' },methods=['GET', 'POST'])
@bp.route('/page/<page_num>',defaults={'sort_by': 'pid', 'filter_by': 'None' },methods=['GET', 'POST'])
@bp.route('/page/<page_num>/<sort_by>',defaults={'filter_by': 'None' },methods=['GET', 'POST'])
@bp.route('/page/<page_num>/<sort_by>/<filter_by>',methods=['GET', 'POST'])
def productPage(page_num = 1, sort_by = 'pid',filter_by = 'None'):
    # get all available products for sale:
    unread=None
    if current_user.is_authenticated:
        unread = num_unread()
    if filter_by == 'None':
        filter_by = None
    page_num = int(page_num)
    temp = ['All']
    if filter_by:
        temp = filter_by.split('|')
    if len(temp)>1:
        if temp[0] == 'All':
            filter_val = None
        else:
            filter_val = temp[0]
        products = Product.get_all_page(page_num = page_num, sort_by = sort_by,filter_by = filter_val,  range_filter = temp[1], bottom = temp[2], top = temp[3])
    else:
        products = Product.get_all_page(page_num = page_num, sort_by = sort_by, filter_by = filter_by)
    filterform = NewFilterForm()
    filter_categories = Product.get_categories()
    filter_categories.append((None, 'Clear Filter'))
    filterform.category.choices = filter_categories
    sortform = NewSortForm()
    pageform = NewPageForm()
    searchform = NewSearchForm()
    rangefilterform = NewRangeFilterForm()
    prev_page = page_num - 1

    next_page = page_num + 1
    max_pages = Product.get_page_count()
    
    if next_page > max_pages:
        next_page = 0
    if filterform.validate_on_submit():
        return redirect(url_for('productPage.productPage', page_num = 1, sort_by = sort_by, filter_by = filterform.category.data))
    if sortform.validate_on_submit():
        return redirect(url_for('productPage.productPage', page_num = 1, sort_by = sortform.key.data + sortform.direction.data, filter_by = filter_by))
    if pageform.validate_on_submit():
        if pageform.page_val.data < 1 or pageform.page_val.data > max_pages:
            flash('Please input a page number between 1 and {num1}!'.format(num1 = max_pages))
            return redirect(url_for('productPage.productPage', page_num = page_num, sort_by = sort_by, filter_by = filter_by))
        else:
            return redirect(url_for('productPage.productPage', page_num = pageform.page_val.data, sort_by = sort_by, filter_by = filter_by))
    if searchform.validate_on_submit():
        return redirect(url_for('productPage.productSearchPage', page_num = 1, query = searchform.search_val.data))
    if rangefilterform.validate_on_submit():
        filter_type = rangefilterform.filter_type.data
        lower_bound = rangefilterform.lower.data
        upper_bound = rangefilterform.upper.data
        filter_range = '|'.join([temp[0],filter_type,str(lower_bound), str(upper_bound)])
        return redirect(url_for('productPage.productPage', page_num = 1, sort_by = sort_by, filter_by = filter_range))
    return render_template('index.html',form1=filterform, form2 = sortform, form3 = pageform,form4 = searchform, form5 = rangefilterform,
                           avail_products = products, next_page=next_page, prev_page=prev_page, curr_sort = sort_by, curr_filter = filter_by, unread=unread)

@bp.route('/products_search',defaults={'query' :'', 'page_num' : 1},methods=['GET', 'POST'])
@bp.route('/products_search/<query>',defaults={'page_num': 1 },methods=['GET', 'POST'])
@bp.route('/products_search/<query>/<page_num>',methods=['GET', 'POST'])
def productSearchPage(page_num = 1, query = ""):
    # get all available products for sale:
    page_num = int(page_num)
    unread=None
    if current_user.is_authenticated:
        unread = num_unread()
    products = Product.get_all_search(page_num = page_num, search_query = query)
    prev_page = page_num - 1

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
                           avail_products = products, next_page=next_page, prev_page=prev_page, query=query, unread=unread)