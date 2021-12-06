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
from .models.Carts import Cartesian
from flask import Blueprint
bp = Blueprint('productSummary', __name__)


class NewBuyingProductForm(FlaskForm):
    amountToBuy = IntegerField(_l('Amount'), validators = [DataRequired()])
    submit1 = SubmitField(_l('Add to Cart'))

class NewReviewForm(FlaskForm):
    review = StringField(_l('Review'), validators = [DataRequired()])
    rating = SelectField(_l('Rating'), choices = [(1,1),(2,2),(3,3),(4,4),(5,5)],validators=[DataRequired()])
    submit2 = SubmitField(_l('Add Review'))

class NewUpdateReviewForm(FlaskForm):
    review = StringField(_l('Review'), validators = [DataRequired()])
    rating = SelectField(_l('Rating'), choices = [(1,1),(2,2),(3,3),(4,4),(5,5)],validators=[DataRequired()])
    submit3 = SubmitField(_l('Update Review'))

class NewDeleteReviewForm(FlaskForm):
    submit4 = SubmitField(_l('Delete Review'))
    
@bp.route('/product/<pid>',methods=['GET', 'POST'])
def product_summaries(pid):
    # get all available products for sale:
    products = ProductSummary.get_all(pid)
    product_temp = Product.get(pid)
    product_name = product_temp.name
    sellers = ProductSeller.get_all_name(product_name)
    bought = False
    sold = False
    left_review = False
    buyform = NewBuyingProductForm()
    reviewform = NewReviewForm()
    updatereviewform = NewUpdateReviewForm()
    deleteform = NewDeleteReviewForm()
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        for purchase in purchases:
            if purchase.pid == int(pid):
                bought = True
        for seller in ProductSeller.get_all(pid):
            if seller.id == current_user.id:
                sold = True
        for i in Product.get_all_review():
            if i[1] == int(pid):
                left_review = True
                if request.method == 'GET':
                    updatereviewform = NewUpdateReviewForm(formdata = MultiDict({
                'review': i[3],
                'rating': i[2]
            }))
        if buyform.validate_on_submit():
            if buyform.amountToBuy.data <= product_temp.quantity_available:
                ido = Cartesian.get(current_user.id)
                alreadyinCart = False
                if ido != None:
                    for i in ido:
                        if i.pid == int(pid):
                            alreadyinCart = True
                if alreadyinCart:
                    Cartesian.addToCartAgain(current_user.id, int(pid), buyform.amountToBuy.data)
                else:
                    Cartesian.addToCart(current_user.id, int(pid), buyform.amountToBuy.data)
                flash('You have successfully added this to your cart!')
                return redirect(url_for('productSummary.product_summaries', pid = pid))
            else:
                flash('You cannot buy more than what is available!')
                return redirect(url_for('productSummary.product_summaries', pid = pid))
        if reviewform.submit2.data and reviewform.validate_on_submit():
            if Product.add_review(current_user.id,int(pid), reviewform.review.data, reviewform.rating.data):
                flash('You have successfully added a review for this product!')
            return redirect(url_for('productSummary.product_summaries', pid = pid))
        if updatereviewform.submit3.data and updatereviewform.validate_on_submit():
            Product.update_review(current_user.id, int(pid), updatereviewform.review.data, int(updatereviewform.rating.data))
            flash('You have successfully updated your review for this product!')
            return redirect(url_for('productSummary.product_summaries', pid = pid))
        if deleteform.validate_on_submit():
            Product.delete_review(current_user.id, int(pid))
            flash('You have successfully updated your review for this product!')
            return redirect(url_for('productSummary.product_summaries', pid = pid))
            
    return render_template('product_summary.html',
                           curr_product=products[0],
                           reviews = products,
                           curr_product_2 = product_temp,
                           all_sellers = sellers,
                           bought_product = bought,
                           sold_product = sold,
                            pid = pid,
                            num_reviews = len(products),
                           left_review = left_review,
                          form1 = buyform,
                          form2 = reviewform,
                          form3 = updatereviewform,
                          form4 = deleteform)
