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

@bp.route('/seller_inventory')
def seller_inventory():
   inventory = User.get_products(current_user.id) 
   return render_template('seller_inventory.html', inventory=inventory)