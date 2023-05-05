-- Database : 'IOT';

DROP TABLE IF EXISTS user,user_address,user_payment,shoppping_session,cart_item,order_detils,order_item,payment_details,product,product_category,product_inventory,discount;

CREATE TABLE user (
    ID int (50) NOT NULL,
    username varchar(100) NOT NULL,
    first_name decimal(100) NOT NULL,
    last_name varchar(100) NOT NULL,
    telephone int (20) NOT NULL,
    create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE user_address(
    ID int (50) NOT NULL,
    user_id int (50)  NOT NULL,
    address_line1 varchar(250)  NOT NULL,
    address_line2 varchar(250)  NOT NULL,
    city varchar(200) NOT NULL,
    postal_code varchar(6) NOT NULL,
    country varchar(50) NOT NULL, 
    telephone int(20) NOT NULL,
    mobile int(10) NOT NULL
);

-- CREATE TABLE user_payment(
--     ID int (50) NOT NULL,
--     user_id int (50)  NOT NULL,
--     payment_type varchar(100) NOT NULL,
--     provider varchar(100) NOT NULL,
--     account_no int(50) NOT NULL,
--     expiry_date int(50) NOT NULL
-- );

-- CREATE TABLE shoppping_session(
--     ID int (50) NOT NULL,
--     user_id int (50)  NOT NULL,
--     total int(50)  NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE cart_item(
--     ID int (50) NOT NULL,
--     session_id int(50) NOT NULL,
--     product_id int(50) NOT NULL,
--     quantity int(50) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE order_detils(
--     ID int (50) NOT NULL,
--     user_id int (50) NOT NULL,
--     total int (50) NOT NULL,
--     payment_id int(50) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE order_item(
--     ID int (50) NOT NULL,
--     order_id int(50) NOT NULL,
--     product_id int(50) NOT NULL,
--     quantity int(50) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE payment_details(
--     ID int (50) NOT NULL,
--     order_id int(50) NOT NULL,
--     amount int(50) NOT NULL,
--     provider varchar(100) NOT NULL,
--     status varchar(100) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE product(
--     ID int (50) NOT NULL,
--     name varachar(100) NOT NULL,
--     desc varchar(250) NOT NULL,
--     SKU varchar(100) NOT NULL,
--     category_id int(50) NOT NULL,
--     inventory_id int(50) NOT NULL,
--     price int(50) NOT NULL,
--     discount_id int(50) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE product_category(
--     ID int (50) NOT NULL,
--     name varachar(100) NOT NULL,
--     desc varchar(250) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE product_inventory(
--     ID int (50) NOT NULL,
--     quantity int(50) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE discount(
--     ID int (50) NOT NULL,
--     name varchar(100) NOT NULL,
--     desc varchar(100) NOT NULL,
--     discount_percent int(50) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );