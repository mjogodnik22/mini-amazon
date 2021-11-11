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
SELECT Users.firstname, Products.pid, CARTS.quantity, CARTS.price_when_placed
FROM CARTS, Users, Products
WHERE uid = :uid AND CARTS.uid = Users.id AND CARTS.pid = Products.pid
''',
                              uid=uid)
        return [Cartesian(*row) for row in rows] if rows else None
    
    @staticmethod
    def getspecific(uid,pid):
        rows = app.db.execute('''
SELECT Users.firstname, Products.pid, CARTS.quantity, CARTS.price_when_placed
FROM CARTS, Users, Products
WHERE uid = :uid AND Products.pid = :pid AND CARTS.uid = Users.id AND CARTS.pid = Products.pid
''',
                              uid=uid,
                              pid = pid)
        return Cartesian(*(rows[0])) if rows else None


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

    @staticmethod
    def removeFromCart(pid,uid):
        try:
            rows = app.db.execute("""
    DELETE FROM Carts WHERE pid = :pid and carts.uid= :uid
            """,pid=pid,
                uid = current_user.id)
            return 1
        except Exception as l:
            print(l)
            return None
