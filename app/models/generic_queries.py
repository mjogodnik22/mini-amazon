from flask import current_app as app
from flask.globals import current_app
from flask_login import current_user
from datetime import datetime


def get_sellers_orders():
    rows = app.db.execute('''
Select DISTINCT oid, time_purchased
FROM Products NATURAL JOIN ItemsInOrder NATURAL JOIN OrderInformation
WHERE seller_id = :current_user_id
ORDER BY oid, time_purchased
''',
    current_user_id = current_user.id)     
    return rows

def order_fulfilled(oid):
        rows = app.db.execute('''
        SELECT fulfilled
        FROM Products NATURAL JOIN ItemsInOrder
        WHERE oid = :oid
        ''',
        oid = oid)
        for row in rows:
            if row.fulfilled == 'Not Fulfilled':
                return 'Not Fulfilled'
        return 'Fulfilled'


def seller_order_fulfilled(oid):
    rows = app.db.execute('''
    SELECT fulfilled
    FROM Products NATURAL JOIN ItemsInOrder
    WHERE oid = :oid
    AND seller_id = :current_user_id
    ''',
    oid = oid,
    current_user_id = current_user.id)
    for row in rows:
        if row.fulfilled == 'Not Fulfilled':
            return False
    return True


def fulfillProduct(oid,pid,Fulfilled):
    rows = app.db.execute('''
Update ItemsInOrder
SET fulfilled = :Fulfilled, date_time=:now 
WHERE oid = :oid
AND pid = :pid
Returning *
''',
    pid = int(pid),
    oid = int(oid),
    Fulfilled = Fulfilled,
    now = datetime.now())  
    return rows


def get_sellers_order_details(oid):
    rows = app.db.execute('''
Select pid, name, price, quantity, fulfilled, date_time
FROM Products NATURAL JOIN ItemsInOrder
WHERE seller_id = :current_user_id
AND  oid = :oid
''',
    current_user_id = current_user.id,
    oid = oid)     
    return rows

def get_order_purchase_details(oid):
    orderer = app.db.execute('''
Select Distinct firstname, order_address
FROM OrderInformation, Users
WHERE oid = :oid
AND Users.id = OrderInformation.uid
''',
    oid = oid)     
    return orderer[0]

def get_seller_information(id):
    rows = app.db.execute('''
    SELECT buyer_id, firstname, lastname, rating, review
    FROM Users, SellerReview
    WHERE id = :id
    AND seller_id = :id
    AND id = seller_id
    ORDER BY rating DESC
    ''',
    id = id)
    return rows

def get_seller_products(id):
    rows = app.db.execute('''
    SELECT pid, name, price
    FROM Products
    WHERE seller_id=:id
    AND Deleted = False
    ''',
    id=id)
    return rows

def get_all_seller_products(id):
    rows = app.db.execute('''
    SELECT pid, name, price
    FROM Products
    WHERE seller_id=:id

    ''',
    id=id)
    return rows

def add_seller_review(buyer_id,seller_id, review,rating):
    rows = app.db.execute("""
INSERT INTO SellerReview(buyer_id,seller_id, rating,review, time_rev)
VALUES(:buyer_id,:seller_id,:rating,:review,:time_rev)
RETURNING buyer_id
""",
    buyer_id = buyer_id,
    seller_id = seller_id,
    rating = rating,
    review = review,
    time_rev = datetime.now())
    
    id = rows[0][0]
    return 1

def update_seller_review(buyer_id,seller_id, review,rating):
    
    rows = app.db.execute("""
    UPDATE SellerReview
    SET  rating = :rating, review = :review, time_rev = :time_rev
    WHERE buyer_id = :buyer_id AND seller_id = :seller_id
    RETURNING buyer_id
    """,
    buyer_id = buyer_id,
    seller_id = seller_id,
    rating = rating,
    review = review,
    time_rev = datetime.now())

    id = rows[0][0]
    return 1

def delete_seller_review(buyer_id,seller_id):
    rows = app.db.execute("""
DELETE FROM SellerReview
WHERE (buyer_id = :buyer_id) AND (seller_id = :seller_id)
RETURNING buyer_id;
""",
    buyer_id = buyer_id,
    seller_id = seller_id)
    return 1

def who_sells(id):
    rows = app.db.execute("""
    SELECT seller_id
    FROM Products
    WHERE pid= :pid
    """, 
    pid=id)
    return rows[0][0]

def save_for_later(uid, pid, quantity):
    rows0 = app.db.execute("""
    SELECT *
    FROM SaveForLater
    WHERE uid = :uid
    AND pid = :pid
    """,
    uid = uid,
    pid = pid)
    if len(rows0) == 0:
        rows = app.db.execute("""
        INSERT INTO SaveForLater(uid, pid, quantity)
        VALUES(:uid, :pid, :quantity)
        RETURNING uid
        """,
        uid = uid,
        pid = pid,
        quantity = quantity)
    else:
        rows = app.db.execute("""
        UPDATE SaveForLater
        SET quantity = :quantity
        WHERE uid = :uid
        AND pid = :pid
        RETURNING uid
        """,
        quantity = rows0[0].quantity + int(quantity),
        uid = uid,
        pid = pid)
    rows2 = app.db.execute("""
    DELETE FROM CARTS
    WHERE uid = :uid
    AND pid = :pid
    RETURNING uid
    """,
    uid = uid,
    pid = pid)
    return 1
  
def delete_saved(uid, pid):
    rows = app.db.execute("""
    DELETE FROM SaveForLater
    WHERE uid = :uid
    AND pid = :pid
    RETURNING uid
    """,
    uid = uid,
    pid = pid)
    return 1

def back_in_cart(uid, pid, quantity):
    rows0 = app.db.execute("""
    SELECT *
    FROM CARTS
    WHERE uid = :uid
    AND pid = :pid
    """,
    uid = uid,
    pid = pid)
    if len(rows0) == 0:
        rows = app.db.execute("""
        INSERT INTO CARTS(uid, pid, quantity)
        VALUES(:uid, :pid, :quantity)
        RETURNING :uid
        """,
        uid = uid,
        pid = pid,
        quantity = quantity)
    else:
        rows = app.db.execute("""
        UPDATE CARTS
        SET quantity = :quantity
        WHERE uid = :uid
        AND pid = :pid
        RETURNING :uid
        """,
        quantity = rows0[0].quantity + int(quantity),
        uid = uid,
        pid = pid)
    rows2 = app.db.execute("""
    DELETE FROM SaveForLater
    WHERE uid = :uid
    AND pid = :pid
    RETURNING :uid
    """,
    uid = uid,
    pid = pid)
    return 1
def users_reviews(uid):
    product_reviews = app.db.execute("""
    SELECT product_id, name, rating, review, time_rev
    FROM ProductReview, Products 
    WHERE buyer_id= :id AND pid = product_id
    ORDER BY time_rev DESC
    """, 
    id=uid)
    seller_reviews = app.db.execute("""
    SELECT seller_id, firstname, lastname, rating, review, time_rev
    FROM SellerReview, Users
    WHERE buyer_id= :uid AND users.id = seller_id
    ORDER BY time_rev DESC
    """, 
    uid=uid) 
    return (product_reviews, seller_reviews)


def delete_product(pid):
    UpdateProduct = app.db.execute("""
    UPDATE Products
    SET deleted = True
    WHERE pid = :pid AND seller_id = :seller_id
    RETURNING :pid
    """,pid = pid, seller_id = current_user.id)
    RemoveFromSaved = app.db.execute("""
    DELETE FROM SaveForLater
    WHERE pid = :pid
    RETURNING :pid
    """,
    pid =pid)
    RemoveFromCart = app.db.execute("""
    DELETE FROM Carts
    WHERE pid = :pid
    RETURNING :pid
    """,
    pid =pid)
    return 1

def restore_product(pid):
    UpdateProduct = app.db.execute("""
    UPDATE Products
    SET deleted = False
    WHERE pid = :pid AND seller_id = :seller_id
    RETURNING :pid
    """,pid = pid, seller_id = current_user.id)
    return 1

def is_deleted(pid):
    val = app.db.execute("""
    Select deleted
    From Products
    WHERE pid = :pid
    """,pid = pid)
    return val[0]

def discount(code,pid,old_price):
    amt = app.db.execute("""
    SELECT Products.price*DiscountCode.discount_amount 
    FROM Products, DiscountCode
    WHERE Products.pid= :pid AND DiscountCode.code = :code AND (allItems = True or DiscountCode.pid = :pid 
    or products.seller_id = DiscountCode.seller)
    """, 
    pid=pid, code=code)
    if amt == []:
        return (old_price, 0)
    return (round(float(old_price)-amt[0][0],2), round(amt[0][0],2))

def good_code(code):
    rows = app.db.execute("""
    SELECT * 
    FROM DiscountCode
    WHERE DiscountCode.code = :code""",
    code=code)
    if rows == []:
        return False
    return True

def getUsersDiscounts(id):
    prods = app.db.execute("""
    SELECT Products.name, DiscountCode.code, DiscountCode.Pid, DiscountCode.discount_amount*100
    FROM DiscountCode, Products
    WHERE Products.pid = DiscountCode.pid AND Products.seller_id = :id
    ORDER BY DiscountCode.Pid
    """,
    id=id)
    seller = app.db.execute("""
    SELECT DiscountCode.code, DiscountCode.discount_amount*100
    FROM DiscountCode
    WHERE DiscountCode.seller = :id""",
    id=id)
    return (prods, seller)

def add_discount_code_product(code, product, amount):
    try:
        rows = app.db.execute("""
        INSERT INTO DiscountCode(code, pid, seller, allItems, discount_amount)
        VALUES(:code, :pid, :seller, :allItems, :discount_amount)
        RETURNING :code
        """,
        code=code, pid = product, seller = None, allItems  = False, discount_amount=amount)
        return rows
    except Exception:
        return False


def add_discount_code_seller(code, seller, amount):
    try:
        rows = app.db.execute("""
        INSERT INTO DiscountCode(code, pid, seller, allItems, discount_amount)
        VALUES(:code, :pid, :seller, :allItems, :discount_amount)
        RETURNING :code
        """,
        code=code, pid = None, seller = seller, allItems  = False, discount_amount=amount)
        return rows
    except Exception:
        return False

    

def remove_discount_code(code):
    RemoveCode = app.db.execute("""
    DELETE FROM DiscountCode
    WHERE code = :code
    RETURNING :code
    """,
    code =code)
    return RemoveCode

def remove_seller_code(code):
    RemoveCode = app.db.execute("""
    DELETE FROM DiscountCode
    WHERE code = :code AND Seller = :sid
    RETURNING :code
    """,
    code =code, sid = current_user.id)
    return RemoveCode