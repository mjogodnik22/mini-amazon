from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.user import User
from .models.messages import *


from flask import Blueprint
bp = Blueprint('myaccount', __name__)

@bp.route('/myAccountPage')
def myAccountPage():
#     balance = 0
#     if current_user.is_authenticated:
#         balance = User.get_balance(current_user.id)
    unread = num_unread()
    return render_template('myaccount.html', title='My Account', unread = unread)