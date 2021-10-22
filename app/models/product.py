from flask import current_app as app


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
