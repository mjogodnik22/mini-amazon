from flask import current_app as app

class ProductSummary:
    def __init__(self, pid, name, description, category, price, review, rating, image):
        self.pid = pid
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.review = review
        self.rating = rating
        self.image = image
        
    @staticmethod
    def get(pid):
        rows = app.db.execute('''
SELECT pid, name, description, category, price, review, rating, picture
FROM ProductSummary
WHERE pid = :pid
ORDER BY rating DESC
''',
                              pid=pid)
        return ProductSummary(*(rows[0])) if rows else None
    
    @staticmethod
    def get_all(pid):
        rows = app.db.execute('''
SELECT pid, name, description, category, price, review, rating, picture
FROM ProductSummary
WHERE pid = :pid
ORDER BY rating DESC
''',
                              pid=pid)
        return [ProductSummary(*row) for row in rows]

