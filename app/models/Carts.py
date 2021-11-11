from flask import current_app as app
from flask_login import login_user, logout_user, current_user
from .. import login

class Cartesian:
    def __init__(self, uid, pid, quantity, price):
        self.uid = uid
        self.pid = pid
        self.priceatpurchase = price
        self.quantity = quantity

    
    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT Users.firstname, Products.name, CARTS.quantity, CARTS.price_when_placed
FROM CARTS, Users, Products
WHERE uid = :uid AND CARTS.uid = Users.id AND CARTS.pid = Products.pid
''',
                              uid=uid)
        return [Cartesian(*row) for row in rows] if rows else None

    @staticmethod
    def addToCart(uid, pid, quantity, price):
        try:
            rows = app.db.execute("""
INSERT INTO CARTS(uid, pid, quantity, price_when_placed)
VALUES(:uid, :pid, :quantity, :price)
RETURNING uid
""",
                                  uid=uid,
                                  pid=pid,
                                  quantity=quantity,
                                  price=price)
            id = rows[0][0]
            return 1
        except Exception as e:
            # likely email already in use; better error checking and
            # reporting needed
            return None

