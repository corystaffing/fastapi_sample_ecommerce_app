from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DECIMAL, Text, DateTime
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from ..db_setup import Base
from .mixins import Timestamp # adds created_at, updated_at cols

# a user can have multiple addresses, orders
# an order has a user, billing & shipping addresses, and a product
# each order will only contain one product (unlike many ecommerce sites)

class Customer(Timestamp, Base):
    __tablename__ = 'customers'
    id         = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name  = Column(String)
    email      = Column(String)
    password   = Column(String)
    phone      = Column(String)

    addresses = relationship("Address", back_populates="customer")
    orders    = relationship("Order", back_populates="customer")

class Product(Timestamp, Base):
    __tablename__ = 'products'
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String)
    description = Column(String)
    price       = Column(DECIMAL(10, 2))
    quantity    = Column(Integer)
    size        = Column(String)
    color       = Column(String)

class Order(Timestamp, Base):
    __tablename__ = 'orders'
    id           = Column(Integer, primary_key=True)
    date         = Column(DateTime, default=datetime.now)
    quantity     = Column(Integer)
    review_score = Column(Integer)
    review_text  = Column(Text)

    customer_id         = Column(Integer, ForeignKey('customer.id'))
    product_id          = Column(Integer, ForeignKey('product.id'))
    billing_address_id  = Column(Integer, ForeignKey('address.id'))
    shipping_address_id = Column(Integer, ForeignKey('address.id'))

    billing_address  = relationship("Address", foreign_keys=[billing_address_id], back_populates="billed_orders")
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id], back_populates="shipped_orders")
    customer         = relationship("Customer", back_populates="orders")
    product          = relationship("Product", back_populates="orders")

class Address(Timestamp, Base):
    __tablename__ = 'addresses'
    id           = Column(Integer, primary_key=True, index=True)
    street       = Column(String)
    city         = Column(String)
    state        = Column(String)
    zip          = Column(String)
    country_code = Column(String(2), default='US', checkconstraints=[CheckConstraint("country_code = upper(country_code)", name='valid_country_code')])
    customer_id  = Column(Integer, ForeignKey('customer.id'))

    customer = relationship("Customer", back_populates="addresses")
    # probably don't need the two below
    # would i need to know: what orders came/billed to this address?
    billed_orders  = relationship("Order", foreign_keys=[Order.billing_address_id], back_populates="billing_address")
    shipped_orders = relationship("Order", foreign_keys=[Order.shipping_address_id], back_populates="shipping_address")


engine = create_engine('sqlite:///sample.db')
Base.metadata.create_all(engine)
