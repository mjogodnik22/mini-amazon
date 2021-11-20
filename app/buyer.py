from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.generic_queries import *
from .models.Carts import Cartesian


from flask import Blueprint
buyer_bp = Blueprint('BuyerOrders', __name__)

@buyer_bp.route('/BuyerOrders')
def buyer_orders():
   empty = False
   borders = Cartesian.getOrders(current_user.id)
   if borders is None:
      empty = True
   return render_template('buyer.html', orders=borders, empty= empty)

