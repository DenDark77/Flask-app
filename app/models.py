from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import String, Column, ForeignKey, Integer, Float, Boolean, DateTime
from session import Base


db = SQLAlchemy()


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    color = Column(String(50))
    weight = Column(Float)
    price = Column(Float)


class Address(Base):
    __tablename__ = "address"

    id = Column(db.Integer, primary_key=True)
    country = Column(db.String(50))
    city = Column(db.String(50))
    street = Column(db.String(100))


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    address_id = Column(Integer, ForeignKey('address.id'))
    status = Column(String(50))

    address = relationship('Address')
    products = relationship('OrderProduct', back_populates='order')


class OrderProduct(Base):
    __tablename__ = "order_product"

    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    quantity = Column(Integer)

    order = relationship('Order', back_populates='products')
    product = relationship('Product')


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    active = Column(Boolean)
    confirmed_at = Column(DateTime)

    roles = relationship('Role', secondary='user_roles')


class UserRoles(Base):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    role_id = Column(Integer, ForeignKey('role.id', ondelete='CASCADE'))
