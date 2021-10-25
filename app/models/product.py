from flask import current_app as app
from flask_login import login_user, logout_user, current_user


class Product:
    def __init__(self, pid, name, price, quantity_available):
        self.pid = pid
        self.name = name
        self.price = price
        self.quantity_available = quantity_available

    @staticmethod
    def get(pid):
        rows = app.db.execute('''
SELECT pid, name, price, quantity_available
FROM Products
WHERE pid = :pid
''',
                              pid=pid)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT pid, name, price, quantity_available
FROM Products

''',
                              available=available)
        return [Product(*row) for row in rows]
    
    

    @staticmethod
    def make_new_product(name, description, category,price, quantity_available):
        try:
            print("HI")
            rows = app.db.execute("""
INSERT INTO Products(seller_id, name, description, category, picture,price, quantity_available)
VALUES(:seller_id, :name, :description, :category, :picture,:price, :quantity_available)
RETURNING seller_id
""",
                                  seller_id = current_user.id,
                                  name = name,
                                  description = description,
                                  category = category,
                                picture = None,
                                price = price,
                                quantity_available = quantity_available)
            id = rows[0][0]
            return 5
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None