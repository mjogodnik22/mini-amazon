from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login
from .product import Product


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, address, balance):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.balance = balance
        self.address = address

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, address, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, address, firstname, lastname):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, address, firstname, lastname)
VALUES(:email, :password, :address, :firstname, :lastname)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  address=address,
                                  firstname=firstname,
                                  lastname=lastname)
            id = rows[0][0]
            return User.get(id)
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, address, balance
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def update_balance(id, old_bal, dep_amt, wdr_amt):
        try:
            balance = (old_bal+dep_amt)-wdr_amt
            rows = app.db.execute("""
UPDATE Users
SET balance = :balance
WHERE id = :id
RETURNING id
""",
                              id=id,
                              balance = balance)
            return User.get(id)
        except Exception:
            # likely user not in system; better error checking and
            # reporting needed
            return None


    #SELLER METHODS BELOW, Considering Extending Users class but don't know it's necessary

    @staticmethod
    def is_seller(id):
        rows = app.db.execute("""
SELECT id
FROM Sellers
WHERE seller.sid = :id
""",
                              id=sid) #this method hasn't been tested
        return len(rows) > 0

    def get_products(id):
        rows = app.db.execute('''
            SELECT Products.pid, Products.name, Products.price, Products.quantity_available
            FROM Products
            WHERE Products.seller_id = :id
''',
                              id=id)

        return rows 