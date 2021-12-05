from flask import current_app as app
from flask_login import current_user

def get_messages():
    rows=app.db.execute('''
    SELECT mid, sender_id, firstname, lastname, recipient_id, msg, subject, msg_read, time_rev
    FROM Messages, Users
    WHERE recipient_id = :id
    AND sender_id = Users.id
    ORDER BY time_rev DESC
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

def get_message_by_mid(mid):
    rows=app.db.execute('''
    SELECT msg, msg_read, recipient_id, sender_id
    FROM Messages
    WHERE mid = :mid
    ''',
    mid = mid)
    return rows[0]

def mark_message_read(mid):
    rows=app.db.execute('''
    UPDATE Messages
    SET msg_read = 'Read'
    WHERE mid = :mid
    RETURNING mid
    ''',
    mid = mid)
    return mid

def get_sent_msgs():
    rows=app.db.execute('''
    SELECT *
    FROM Messages, Users
    WHERE sender_id = :id
    AND recipient_id = Users.id
    ORDER BY time_rev DESC
    ''',
    id = current_user.id)
    return rows