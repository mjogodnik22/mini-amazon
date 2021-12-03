from flask import current_app as app
from flask_login import login_user, logout_user, current_user
from sqlalchemy import text

class Product:
    def __init__(self, pid, name, price, quantity_available,avg_rating):
        self.pid = pid
        self.name = name
        self.price = price
        self.quantity_available = quantity_available
        self.avg_rating = avg_rating

    @staticmethod
    def get(pid):
        rows = app.db.execute('''
SELECT Products.pid, name, price, quantity_available, avg_rating
FROM Products
    LEFT JOIN (
              SELECT pid, AVG(rating) avg_rating
              FROM ProductSummary 
              GROUP BY pid
            ) r ON r.pid = Products.pid
WHERE Products.pid = :pid
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
    def get_all_page(available=True, filter_by = None, sort_by = 'pid', limit = 10, page_num = 1, range_filter = 'price', bottom = -1, top = 1000000):
        offset_count = (page_num - 1) * limit
        ordering = 'ASC'
        if sort_by[-4:] == 'DESC':
            ordering = 'DESC'
            sort_by = sort_by[:-4]
        if filter_by:
            rows = app.db.execute('''
    SELECT Products.pid, name, price, quantity_available,  avg_rating
    FROM Products
    LEFT JOIN (
              SELECT pid, AVG(rating) avg_rating
              FROM ProductSummary 
              GROUP BY pid
            ) r ON r.pid = Products.pid
    WHERE category = :filter_by AND {range_filter} BETWEEN :bottom AND :top  
    ORDER BY COALESCE({sort_by},-1) {order}
    LIMIT {limit}
    OFFSET {offset}
    '''.format(sort_by = sort_by, limit = limit, offset = offset_count,range_filter = range_filter, order = ordering), bottom = bottom, top = top, filter_by = filter_by)
        else:
            rows = app.db.execute('''
    SELECT Products.pid, name, price, quantity_available,avg_rating
    FROM Products
    LEFT JOIN (
              SELECT pid ppid, AVG(rating) avg_rating
              FROM ProductSummary 
              GROUP BY pid
            ) r ON r.ppid = Products.pid
    WHERE {range_filter} BETWEEN :bottom AND :top 
    ORDER BY COALESCE({sort_by},-1) {order}
    LIMIT {limit}
    OFFSET {offset}
    '''.format(sort_by = sort_by, limit = limit, offset = offset_count,range_filter = range_filter, order = ordering), bottom = bottom, top = top)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_page_count(limit = 10):
        rows = app.db.execute('''
SELECT COUNT(*)
FROM Products
''')
        return int(rows[0][0]/limit)
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
    def get_all_search(available=True, limit = 10, page_num = 1, search_query = ""):
        query ='\'%' + search_query + '%\''
        offset_count = (page_num - 1) * limit
        rows = app.db.execute('''
    SELECT DISTINCT Products.pid, Products.name, Products.price, Products.quantity_available
    FROM Products, ProductSummary
    WHERE Products.pid = ProductSummary.pid and (Products.name LIKE {query_name} or ProductSummary.description LIKE {query_name})
    ORDER BY Products.pid ASC
    LIMIT {limit}
    OFFSET {offset}
    '''.format(query_name = query, query_desc = query,limit = limit, offset = offset_count))
        return [Product(*row) for row in rows]
    
    
    @staticmethod
    def make_new_seller():
        try:
            rows_useless = app.db.execute("""
            INSERT INTO Sellers(sid)
            VALUES(:sid)
            RETURNING sid
            """,
            sid=current_user.id)
            return 1
        except Exception:
            return None
        
    @staticmethod
    def make_new_product(name, description, category,price, quantity_available, image):
        try:
            temp = Product.make_new_seller()
            rows = app.db.execute("""
INSERT INTO Products(seller_id, name, description, category, picture,price, quantity_available)
VALUES(:seller_id, :name, :description, :category, :picture,:price, :quantity_available)
RETURNING seller_id
""",
                                  seller_id = current_user.id,
                                  name = name,
                                  description = description,
                                  category = category,
                                picture = image,
                                price = price,
                                quantity_available = quantity_available)
            id = rows[0][0]
            return 1
        except Exception:
            return None
    @staticmethod
    def update_product(name, description, category,price, quantity_available, image):
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
                                picture = image,
                                price = price,
                                quantity_available = quantity_available)
            id = rows[0][0]
            return 1
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None
        
        
    @staticmethod
    def get_all_review():
        rows = app.db.execute("""
SELECT *
FROM ProductReview
WHERE buyer_id = :id
""", id = current_user.id)
        return rows
    
    @staticmethod
    def add_review(buyer_id,product_id, review,rating):
        try:
            rows = app.db.execute("""
INSERT INTO ProductReview(buyer_id,product_id, rating,review)
VALUES(:buyer_id,:product_id,:rating,:review)
RETURNING buyer_id
""",
                                buyer_id = buyer_id,
                                 product_id = product_id,
                                 rating = rating,
                                 review = review)
            id = rows[0][0]
            return 1
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None
        
    @staticmethod
    def update_review(buyer_id,product_id, review,rating):
        try:
            rows = app.db.execute("""
UPDATE ProductReview
SET  rating = :rating, review = :review
WHERE buyer_id = :buyer_id AND product_id = :product_id
RETURNING buyer_id
""",
                                buyer_id = buyer_id,
                                 product_id = product_id,
                                 rating = rating,
                                 review = review)
            id = rows[0][0]
            return 1
        except Exception as e:
            print(e)
            # likely email already in use; better error checking and
            # reporting needed
            return None

    @staticmethod
    def delete_review(buyer_id,product_id):
        try:
            rows = app.db.execute("""
DELETE FROM ProductReview
WHERE buyer_id = :buyer_id AND product_id = :product_id
RETURNING buyer_id
""",
                                buyer_id = buyer_id,
                                 product_id = product_id)
            id = rows[0][0]
            return 1
        except Exception as e:
            print(e)
            # likely email already in use; better error checking and
            # reporting needed
            return None 
    @staticmethod
    def adjustWithOrder(pid, quantity):
        try:
            rows = app.db.execute("""
            UPDATE PRODUCTS
            SET quantity_available = quantity_available - :quantity
            WHERE pid = :pid
            """,quantity = quantity,
            pid = pid)
            return 1
        except Exception as lo:
            print("ERROR:",lo)
            return 0
        