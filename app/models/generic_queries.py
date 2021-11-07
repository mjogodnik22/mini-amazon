from flask import current_app as app
from flask_login import current_user


def get_sellers_orders():
    rows = app.db.execute('''
Select DISTINCT oid
FROM Products NATURAL JOIN ItemsInOrder
WHERE seller_id = :current_user_id
''',
    current_user_id = current_user.id)     
    return rows