# db-architecture

Estructura desarrollada en [dbdiagram.io](https://dbdiagram.io)

## Definición de tablas

```dbml
Table users {
  id int [pk, increment]
  email varchar(255) [unique, not null]
  hashed_password varchar(255) [not null]
  role varchar(50) [not null, default: 'user']
  created_at timestamp [not null, default: `now()`]
}

Table categories {
  id int [pk, increment]
  name varchar(100) [unique, not null]
  description text
}

Table products {
  id int [pk, increment]
  category_id int [ref: > categories.id, not null]
  name varchar(255) [not null]
  description text
  price decimal(10, 2) [not null]
  stock int [not null, default: 0]
  is_active bool [not null, default: true]
}

Table orders {
  id int [pk, increment]
  user_id int [ref: > users.id, not null]
  status varchar(50) [not null, default: 'pending']
  total_amount decimal(10, 2) [not null]
  created_at timestamp [not null, default: `now()`]
}

Table order_items {
  id int [pk, increment]
  order_id int [ref: > orders.id, not null]
  product_id int [ref: > products.id, not null]
  quantity int [not null]
  unit_price decimal(10, 2) [not null]

  Indexes {
    (order_id, product_id) [unique]
  }
}
```

