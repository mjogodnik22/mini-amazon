from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from werkzeug.datastructures import MultiDict

from .models.user import User
from .models.messages import *


from flask import Blueprint
messages_bp = Blueprint('messages', __name__)
messages_email_bp = Blueprint('messages_email', __name__)
message_details_bp = Blueprint('message_details', __name__)

class MessageForm(FlaskForm):
    recipient_email = StringField(_l('Recipient Email'), validators=[DataRequired(), Email()])
    subject = StringField(_l('Subject'), validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField(_l('Send'))

    def validate_email(self, email):
        if not User.email_exists(email.data):
            raise ValidationError(_('Please check your email - recipient not found!'))

@messages_bp.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = get_messages()
    sent_msgs = get_sent_msgs()
    form = MessageForm()
    if form.validate_on_submit():
        recipient_id = User.get_id_by_email(form.recipient_email.data)
        if recipient_id == None:
            flash('That email is not associated with any user.')
            return redirect(url_for('messages.messages'))
        elif form.recipient_email.data == current_user.email:
            flash('You cannot send yourself a message!')
            return redirect(url_for('messages.messages'))
        elif send_message(recipient_id, form.subject.data, form.message.data):
            flash('Your message has been sent!')
            return redirect(url_for('messages.messages'))
    return render_template('messages.html', title='My Messages', messages=messages, sent_msgs=sent_msgs, form=form)


@messages_email_bp.route('/messages/email/<email>', methods=['GET', 'POST'])
def text(email):
    messages = get_messages()
    sent_msgs = get_sent_msgs()
    form = MessageForm()
    if request.method == 'GET':
        form = MessageForm(formdata = MultiDict({
            'recipient_email': email
        }))
    if form.validate_on_submit():
        recipient_id = User.get_id_by_email(form.recipient_email.data)
        if recipient_id == None:
            flash('That email is not associated with any user.')
            return redirect(url_for('messages.messages'))
        elif form.recipient_email.data == current_user.email:
            flash('You cannot send yourself a message!')
            return redirect(url_for('messages.messages'))
        elif send_message(recipient_id, form.subject.data, form.message.data):
            flash('Your message has been sent!')
            return redirect(url_for('messages.messages'))
    return render_template('messages.html', title='My Messages', messages=messages, sent_msgs=sent_msgs, form=form)

@message_details_bp.route('/messages/msg/<mid>')
def detailed_messages(mid):
    message = get_message_by_mid(mid)
    if message[1] == 'Unread':
        mark_message_read(mid)
    return render_template('message_detail.html', title = 'Your Message', message=message)
