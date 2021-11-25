from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, BooleanField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from werkzeug.datastructures import MultiDict

from .models.user import User


from flask import Blueprint
bp = Blueprint('updatepassword', __name__)

class UpdatePasswordForm(FlaskForm):
    oldpassword = PasswordField(_l('Old Password'), validators=[DataRequired()])
    newpassword = PasswordField(_l('New Password'), validators=[DataRequired()])
    newpassword2 = PasswordField(
        _l('Repeat New Password'), validators=[DataRequired(),
                                           EqualTo('newpassword')])
    submit = SubmitField(_l('Update Password'))

@bp.route('/updatePasswordPage', methods=['GET', 'POST'])
def updatePasswordPage():
    form = UpdatePasswordForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            if not(User.get_by_auth(current_user.email, form.oldpassword.data)):
                flash('Wrong password!')
            elif form.oldpassword.data == form.newpassword.data:
                flash('Can only change password to a new one.')
            elif User.update_password(current_user.id,
                                   form.newpassword.data):
                flash('Your password has been updated!')
                return redirect(url_for('updatepassword.updatePasswordPage'))
            else:
                flash('Unknown error, contact Matt!!')
    else:
        return redirect(url_for('productPage.productPage'))
    return render_template('updatepassword.html', title='Update Password', form=form)
#     balance = 0
#     if current_user.is_authenticated:
#         balance = User.get_balance(current_user.id)

