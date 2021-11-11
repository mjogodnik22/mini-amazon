from flask import current_app as app
from flask_login import current_user

def get_messages():
    rows=app.db.execute('''
    SELECT sender_id, firstname, lastname, recipient_id, msg, subject, msg_read
    FROM Messages, Users
    WHERE recipient_id = :id
    AND sender_id = Users.id
    ''',
    id = current_user.id)
    return rows

def send_message(recipient_id, subject, message):
    rows=app.db.execute('''
    INSERT INTO Messages(sender_id, recipient_id, msg, subject)
    VALUES(:sender_id, :recipient_id, :message, :subject)
    RETURNING :sender_id
    ''',
    sender_id = current_user.id,
    recipient_id = recipient_id,
    message = message,
    subject=subject)
    return 1