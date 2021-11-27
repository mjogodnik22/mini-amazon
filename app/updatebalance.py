from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, BooleanField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.user import User


from flask import Blueprint
bp = Blueprint('updatebalance', __name__)

class UpdateBalanceForm(FlaskForm):
    depOrWdr = SelectField(u'Field name', choices = [('wdr', 'Withdrawal'), ('dep', 'Deposit')], validators = [DataRequired()])
    amount = DecimalField(_l('Amount to Change'), validators=[DataRequired()])
    submit = SubmitField(_l('Update Balance'))

@bp.route('/updateBalancePage', methods=['GET', 'POST'])
def updateBalancePage():
    form = UpdateBalanceForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            if User.update_balance(current_user.id,
                                   current_user.balance,
                                   form.amount.data,
                                   form.depOrWdr.data):
                flash('Your balance has been updated!')
                return redirect(url_for('updatebalance.updateBalancePage'))
            elif form.depOrWdr.data == "wdr" and form.amount.data > current_user.balance:
                flash('You cannot withdraw more than your balance. Please try again!')
                return redirect(url_for('updatebalance.updateBalancePage'))
    else:
        return redirect(url_for('productPage.productPage'))
    return render_template('updatebalance.html', title='Update Balance', form=form)
#     balance = 0
#     if current_user.is_authenticated:
#         balance = User.get_balance(current_user.id)

