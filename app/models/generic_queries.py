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

def order_fulfilled(oid):
    rows = app.db.execute('''
    SELECT fulfilled
    FROM ItemsInOrder
    WHERE oid = :oid
    ''',
    oid = oid)
    for row in rows:
        if row.fulfilled == 'Not Fulfilled':
            return False
    return True


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

def get_seller_information(id):
    rows = app.db.execute('''
    SELECT firstname, lastname, rating, review
    FROM Users, SellerReview
    WHERE id = :id
    AND seller_id = :id
    AND id = seller_id
    ''',
    id = id)
    return rows

def get_seller_products(id):
    rows = app.db.execute('''
    SELECT pid, name, price
    FROM Products
    WHERE seller_id=:id
    ''',
    id=id)
    return rows