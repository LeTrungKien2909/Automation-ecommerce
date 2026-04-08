-- =============================================================
-- AutoTech E-Commerce Database Schema
-- MariaDB / MySQL
-- Engine: InnoDB, Charset: utf8mb4
-- =============================================================

CREATE DATABASE IF NOT EXISTS automation_ecommerce
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE automation_ecommerce;

-- -------------------------------------------------------------
-- Users
-- -------------------------------------------------------------

CREATE TABLE IF NOT EXISTS users_user (
    id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    password      VARCHAR(128)    NOT NULL,
    last_login    DATETIME(6)     NULL,
    is_superuser  TINYINT(1)      NOT NULL DEFAULT 0,
    username      VARCHAR(150)    NOT NULL,
    first_name    VARCHAR(150)    NOT NULL DEFAULT '',
    last_name     VARCHAR(150)    NOT NULL DEFAULT '',
    email         VARCHAR(254)    NOT NULL DEFAULT '',
    is_staff      TINYINT(1)      NOT NULL DEFAULT 0,
    is_active     TINYINT(1)      NOT NULL DEFAULT 1,
    date_joined   DATETIME(6)     NOT NULL,
    phone         VARCHAR(20)     NOT NULL DEFAULT '',
    address       LONGTEXT        NOT NULL DEFAULT '',
    city          VARCHAR(100)    NOT NULL DEFAULT '',
    role          VARCHAR(20)     NOT NULL DEFAULT 'customer',
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_user_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS users_userprofile (
    id        BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id   BIGINT UNSIGNED NOT NULL,
    avatar    VARCHAR(100)    NULL,
    bio       LONGTEXT        NOT NULL DEFAULT '',
    company   VARCHAR(200)    NOT NULL DEFAULT '',
    tax_code  VARCHAR(50)     NOT NULL DEFAULT '',
    PRIMARY KEY (id),
    UNIQUE KEY uq_userprofile_user (user_id),
    CONSTRAINT fk_userprofile_user
        FOREIGN KEY (user_id) REFERENCES users_user (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- -------------------------------------------------------------
-- Products
-- -------------------------------------------------------------

CREATE TABLE IF NOT EXISTS products_category (
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(200)    NOT NULL,
    slug        VARCHAR(50)     NOT NULL,
    description LONGTEXT        NOT NULL DEFAULT '',
    image       VARCHAR(100)    NULL,
    parent_id   BIGINT UNSIGNED NULL,
    created_at  DATETIME(6)     NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_category_slug (slug),
    KEY idx_category_parent (parent_id),
    CONSTRAINT fk_category_parent
        FOREIGN KEY (parent_id) REFERENCES products_category (id)
        ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS products_product (
    id             BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT,
    name           VARCHAR(300)     NOT NULL,
    slug           VARCHAR(50)      NOT NULL,
    category_id    BIGINT UNSIGNED  NULL,
    description    LONGTEXT         NOT NULL,
    specifications LONGTEXT         NOT NULL DEFAULT '',
    price          DECIMAL(15,0)    NOT NULL,
    discount_price DECIMAL(15,0)    NULL,
    stock          INT UNSIGNED     NOT NULL DEFAULT 0,
    main_image     VARCHAR(100)     NULL,
    is_active      TINYINT(1)       NOT NULL DEFAULT 1,
    is_featured    TINYINT(1)       NOT NULL DEFAULT 0,
    created_at     DATETIME(6)      NOT NULL,
    updated_at     DATETIME(6)      NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_product_slug (slug),
    KEY idx_product_category (category_id),
    KEY idx_product_active (is_active),
    KEY idx_product_featured (is_featured),
    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id) REFERENCES products_category (id)
        ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS products_productimage (
    id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_id BIGINT UNSIGNED NOT NULL,
    image      VARCHAR(100)    NOT NULL,
    alt_text   VARCHAR(200)    NOT NULL DEFAULT '',
    PRIMARY KEY (id),
    KEY idx_productimage_product (product_id),
    CONSTRAINT fk_productimage_product
        FOREIGN KEY (product_id) REFERENCES products_product (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS products_productreview (
    id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_id BIGINT UNSIGNED NOT NULL,
    user_id    BIGINT UNSIGNED NOT NULL,
    rating     INT             NOT NULL,
    comment    LONGTEXT        NOT NULL,
    created_at DATETIME(6)     NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_review_product_user (product_id, user_id),
    KEY idx_review_product (product_id),
    KEY idx_review_user (user_id),
    CONSTRAINT fk_review_product
        FOREIGN KEY (product_id) REFERENCES products_product (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_review_user
        FOREIGN KEY (user_id) REFERENCES users_user (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- -------------------------------------------------------------
-- Orders
-- -------------------------------------------------------------

CREATE TABLE IF NOT EXISTS orders_cart (
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id     BIGINT UNSIGNED NULL,
    session_key VARCHAR(40)     NOT NULL DEFAULT '',
    created_at  DATETIME(6)     NOT NULL,
    updated_at  DATETIME(6)     NOT NULL,
    PRIMARY KEY (id),
    KEY idx_cart_user (user_id),
    KEY idx_cart_session (session_key),
    CONSTRAINT fk_cart_user
        FOREIGN KEY (user_id) REFERENCES users_user (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS orders_cartitem (
    id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    cart_id    BIGINT UNSIGNED NOT NULL,
    product_id BIGINT UNSIGNED NOT NULL,
    quantity   INT UNSIGNED    NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    UNIQUE KEY uq_cartitem_cart_product (cart_id, product_id),
    KEY idx_cartitem_product (product_id),
    CONSTRAINT fk_cartitem_cart
        FOREIGN KEY (cart_id) REFERENCES orders_cart (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_cartitem_product
        FOREIGN KEY (product_id) REFERENCES products_product (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS orders_order (
    id               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id          BIGINT UNSIGNED NOT NULL,
    order_number     VARCHAR(20)     NOT NULL,
    status           VARCHAR(20)     NOT NULL DEFAULT 'pending',
    total_amount     DECIMAL(15,0)   NOT NULL,
    shipping_address LONGTEXT        NOT NULL,
    phone            VARCHAR(20)     NOT NULL,
    notes            LONGTEXT        NOT NULL DEFAULT '',
    created_at       DATETIME(6)     NOT NULL,
    updated_at       DATETIME(6)     NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_order_number (order_number),
    KEY idx_order_user (user_id),
    KEY idx_order_status (status),
    CONSTRAINT fk_order_user
        FOREIGN KEY (user_id) REFERENCES users_user (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS orders_orderitem (
    id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    order_id   BIGINT UNSIGNED NOT NULL,
    product_id BIGINT UNSIGNED NOT NULL,
    quantity   INT UNSIGNED    NOT NULL,
    price      DECIMAL(15,0)   NOT NULL,
    PRIMARY KEY (id),
    KEY idx_orderitem_order (order_id),
    KEY idx_orderitem_product (product_id),
    CONSTRAINT fk_orderitem_order
        FOREIGN KEY (order_id) REFERENCES orders_order (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_orderitem_product
        FOREIGN KEY (product_id) REFERENCES products_product (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS orders_invoice (
    id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    order_id       BIGINT UNSIGNED NOT NULL,
    invoice_number VARCHAR(20)     NOT NULL,
    issued_date    DATE            NOT NULL,
    due_date       DATE            NOT NULL,
    total          DECIMAL(15,0)   NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_invoice_number (invoice_number),
    UNIQUE KEY uq_invoice_order (order_id),
    CONSTRAINT fk_invoice_order
        FOREIGN KEY (order_id) REFERENCES orders_order (id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- -------------------------------------------------------------
-- Maintenance
-- -------------------------------------------------------------

CREATE TABLE IF NOT EXISTS maintenance_servicecategory (
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(200)    NOT NULL,
    description LONGTEXT        NOT NULL DEFAULT '',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS maintenance_servicerequest (
    id                  BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id             BIGINT UNSIGNED NOT NULL,
    product_id          BIGINT UNSIGNED NULL,
    service_category_id BIGINT UNSIGNED NULL,
    title               VARCHAR(300)    NOT NULL,
    description         LONGTEXT        NOT NULL,
    status              VARCHAR(20)     NOT NULL DEFAULT 'pending',
    priority            VARCHAR(10)     NOT NULL DEFAULT 'medium',
    assigned_staff_id   BIGINT UNSIGNED NULL,
    requested_date      DATETIME(6)     NOT NULL,
    scheduled_date      DATETIME(6)     NULL,
    completed_date      DATETIME(6)     NULL,
    notes               LONGTEXT        NOT NULL DEFAULT '',
    created_at          DATETIME(6)     NOT NULL,
    updated_at          DATETIME(6)     NOT NULL,
    PRIMARY KEY (id),
    KEY idx_sr_user (user_id),
    KEY idx_sr_product (product_id),
    KEY idx_sr_category (service_category_id),
    KEY idx_sr_staff (assigned_staff_id),
    KEY idx_sr_status (status),
    KEY idx_sr_priority (priority),
    CONSTRAINT fk_sr_user
        FOREIGN KEY (user_id) REFERENCES users_user (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_sr_product
        FOREIGN KEY (product_id) REFERENCES products_product (id)
        ON DELETE SET NULL,
    CONSTRAINT fk_sr_category
        FOREIGN KEY (service_category_id) REFERENCES maintenance_servicecategory (id)
        ON DELETE SET NULL,
    CONSTRAINT fk_sr_staff
        FOREIGN KEY (assigned_staff_id) REFERENCES users_user (id)
        ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS maintenance_servicehistory (
    id                  BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    service_request_id  BIGINT UNSIGNED NOT NULL,
    technician_id       BIGINT UNSIGNED NULL,
    work_done           LONGTEXT        NOT NULL,
    materials_used      LONGTEXT        NOT NULL DEFAULT '',
    cost                DECIMAL(12,0)   NOT NULL DEFAULT 0,
    date                DATETIME(6)     NOT NULL,
    PRIMARY KEY (id),
    KEY idx_sh_request (service_request_id),
    KEY idx_sh_technician (technician_id),
    CONSTRAINT fk_sh_request
        FOREIGN KEY (service_request_id) REFERENCES maintenance_servicerequest (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_sh_technician
        FOREIGN KEY (technician_id) REFERENCES users_user (id)
        ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- End of schema
