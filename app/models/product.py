from flask import current_app as app
from flask_login import login_user, logout_user, current_user
from sqlalchemy import text

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
    def get_all(available=True, filter_by = None, sort_by = 'pid'):
        if filter_by:
            rows = app.db.execute('''
    SELECT pid, name, price, quantity_available
    FROM Products
    WHERE category = :filter_by
    ORDER BY {sort_by}
    '''.format(sort_by = sort_by), filter_by = filter_by)
        else:
            rows = app.db.execute('''
    SELECT pid, name, price, quantity_available
    FROM Products
    ORDER BY {sort_by}
    '''.format(sort_by = sort_by))
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_test(available=True):
        rows = app.db.execute_test('''
SELECT pid, name, price, quantity_available
FROM Products

''')
        return rows
    
    @staticmethod
    def get_categories():
        try:
            rows = app.db.execute('''
    SELECT name
    FROM Category
    ORDER BY name
    ''')
            return [(row.name,row.name) for row in rows]
        except Exception:
            return None

    @staticmethod
    def make_new_product(name, description, category,price, quantity_available):
        try:
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
            return 1
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None
    @staticmethod
    def update_product(name, description, category,price, quantity_available):
        try:
            rows = app.db.execute("""
UPDATE Products
SET name = :name, description  = :description, category = :category, picture = :picture,price = :price, quantity_available = :quantity_available
WHERE seller_id = :seller_id
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
            return 1
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None
