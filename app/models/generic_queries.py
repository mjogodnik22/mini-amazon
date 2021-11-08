from flask import current_app as app
from flask_login import current_user


def get_sellers_orders():
    rows = app.db.execute('''
Select DISTINCT oid
FROM Products NATURAL JOIN ItemsInOrder
WHERE seller_id = :current_user_id
''',
    current_user_id = current_user.id)     
    return rows[0]


def get_sellers_order_details(oid):
    rows = app.db.execute('''
Select pid, name, quantity, fulfilled
FROM Products NATURAL JOIN ItemsInOrder
WHERE seller_id = :current_user_id
AND  oid = :oid
''',
    current_user_id = current_user.id,
    oid = oid)     
    return rows

def get_order_purchase_details(oid):
    orderer = app.db.execute('''
Select Distinct firstname, address
FROM OrderInformation, Users
WHERE oid = :oid
AND Users.id = OrderInformation.uid
''',
    oid = oid)     
    return orderer[0]