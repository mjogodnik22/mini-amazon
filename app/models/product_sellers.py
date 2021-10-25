from flask import current_app as app


class ProductSeller:
    # ADD AVERAGE SELLER RATING LATER
    # can also sort by price?
    def __init__(self, id, first_name, last_name,price, quantity_available):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.price = price
        self.quantity_available = quantity_available

        
    @staticmethod
    def get(pid):
        rows = app.db.execute('''
SELECT Products.seller_id, Users.firstname, Users.lastname, Products.price, Products.quantity_available
FROM Products, Users
WHERE pid = :pid AND products.seller_id = Users.id
''',
                              pid=pid)
        return ProductSeller(*(rows[0])) if rows else None
    
    @staticmethod
    def get_all(pid):
        rows = app.db.execute('''
SELECT Products.seller_id, Users.firstname, Users.lastname, Products.price, Products.quantity_available
FROM Products, Users
WHERE pid = :pid AND products.seller_id = Users.id
''',
                              pid=pid)
        return [ProductSeller(*row) for row in rows]
    


