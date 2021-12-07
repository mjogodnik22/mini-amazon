\COPY Users FROM 'data/Users.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);
\COPY Sellers FROM 'data/Sellers.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Category FROM 'data/Categories.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM 'data/Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_pid_seq',
                         (SELECT MAX(pid)+1 FROM Products),
                         false);
\COPY OrderInformation FROM 'data/OrderInformation.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orderinformation_oid_seq',
                         (SELECT MAX(oid)+1 FROM OrderInformation),
                         false);
\COPY ItemsInOrder FROM 'data/ItemsInOrder.csv' WITH DELIMITER ',' NULL '' CSV
\COPY ProductReview FROM 'data/ProductReview.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SellerReview FROM 'data/SellerReview.csv' WITH DELIMITER ',' NULL '' CSV
\COPY CARTS FROM 'data/Carts.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SaveForLater FROM 'data/SaveForLater.csv' WITH DELIMITER ',' NULL '' CSV
\COPY DiscountCode FROM 'data/DiscountCode.csv' WITH DELIMITER ',' NULL '' CSV