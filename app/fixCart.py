from flask import current_app as app
from cart import *
from generic_queries import *

def fixCart():
    deleted_products = app.db.execute('''
SELECT Products.pid
FROM Products
WHERE Products.pid = :pid AND Products.pid = AverageProductRating.pid
''')
    for product in deleted_products:
        print(product)



    

if __name__ == __main__:
    fixCart()