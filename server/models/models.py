from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)
    phone = Column(String)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(DECIMAL(10, 2))
    quantity = Column(Integer)
    size = Column(String)
    color = Column(String)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    date = Column(String)
    quantity = Column(Integer)

    customer = relationship("Customer", backref=backref("orders", order_by=id))
    product = relationship("Product", backref=backref("orders", order_by=id))

engine = create_engine('sqlite:///sample.db')
Base.metadata.create_all(engine)
