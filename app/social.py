from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import ValidationError, DataRequired
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.generic_queries import *


from flask import Blueprint
bp = Blueprint('social', __name__)

class LookupByName(FlaskForm):
    firstname = StringField(_l('First Name'))
    lastname = StringField(_l('Last Name'))
    email = StringField(_l('Email'))
    submit = SubmitField(_l('Search'))

@bp.route('/social/<id>', methods=['GET', 'POST'])
def social(id):
    max_uid = User.max_user()
    if int(id) > int(max_uid) or int(id) < 1:
        flash('This user does not exist')
        return redirect(url_for('social.social', id=current_user.id))
    form = LookupByName()
    social = User.get(id)
    seller = User.is_seller(id)
    reviews = [0,1]
    products = None
    avg = 0
    if seller:
        reviews = get_seller_information(id)
        products = get_seller_products(id)
        sum = 0
        count = 0
        for rev in reviews:
            sum += rev.rating
            count += 1
        avg = sum/count
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        results = User.get_user_by_name(firstname, lastname, email)
        return render_template('social_search.html', firstname = firstname, lastname=lastname, email = email, results = results)
    return render_template('social_page.html', user=social, is_seller=seller, reviews=reviews, seller=reviews[0], products=products, avg=avg, form=form)

