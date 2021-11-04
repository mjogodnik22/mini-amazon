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
bp = Blueprint('updateinformation', __name__)

class UpdateInformationForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    address = StringField(_l('Address'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    submit = SubmitField(_l('Update Information'))

@bp.route('/updateInformationPage', methods=['GET', 'POST'])
def updateInformationPage():
    form = UpdateInformationForm()
    if request.method == 'GET':
        form = UpdateInformationForm(formdata = MultiDict({
            'firstname': current_user.firstname,
            'lastname': current_user.lastname,
            'email': current_user.email,
            'address': current_user.address
        }))
    if current_user.is_authenticated:
        if form.validate_on_submit():
            if not(User.get_by_auth(current_user.email, form.password.data)):
                flash('Wrong password!')
            elif form.firstname.data == current_user.firstname and form.lastname.data == current_user.lastname and form.email.data == current_user.email and form.address.data == current_user.address:
                flash('Please change something, or go back to My Account!')
            elif User.update_information(current_user.id,
                                   form.firstname.data,
                                   form.lastname.data,
                                   form.email.data,
                                   form.address.data):
                flash('Your information has been updated!')
                return redirect(url_for('updateinformation.updateInformationPage'))
            else:
                flash('This email is already in use.')
    else:
        return redirect(url_for('index.index'))
    return render_template('updateinformation.html', title='Update Information', form=form)
#     balance = 0
#     if current_user.is_authenticated:
#         balance = User.get_balance(current_user.id)

