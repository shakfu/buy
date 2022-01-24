#!/usr/bin/env python3
"""buy.py: a prototype for an online purchasing support tool

## target features

- organization and persistence of all buying data
- repl for buying support
- webscraping of vendor's prices
- inventory of purchased items
- report generation (xlsx, html, pdf..)
    - quote comparison
    - shipping costs attribution based on destination (from, to)
    - discount codes
    - sales patterns recommendation
    - budget mgmt


"""
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import (Column, Date, DateTime, Float, ForeignKey, Integer,
                        String, Table, create_engine)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func

__all__ = [  # model api

    # abstract models
    'Base',
    'Object',

    # concrete models
    'Forex',
    'Vendor',
    'Brand',
    'Product',
    'Quote',

    # helpers
    'mk_adder',
]

Base = declarative_base()


class Object:
    """A mixin class for sqlalcheny to save some typing"""
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def by_name(cls, session, name):
        """query table by name"""
        return session.query(cls).filter_by(name=name).first()

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}')"


class Forex(Base):
    """Table of fx to usd to fx rates"""
    __tablename__ = 'forex'

    id = Column(Integer, primary_key=True)
    date = Column(Date, default=func.now())
    code = Column(String)
    units_per_usd = Column(Float)
    usd_per_unit = Column(Float)

    def __repr__(self):
        return f"<Forex(USD -> {self.name}: {self.units_per_usd})>"


VendorBrand = Table(
    'vendor_brand', Base.metadata,
    Column('vendor_id', ForeignKey('brand.id'), primary_key=True),
    Column('brand_id', ForeignKey('vendor.id'), primary_key=True))


class Vendor(Object, Base):
    """Selling Entity"""

    #country = Column(String)
    currency = Column(String)
    discount_code = Column(String)
    discount = Column(Float, default=0.0)
    brands = relationship('Brand',
                          secondary=VendorBrand,
                          back_populates='vendors')
    quotes = relationship('Quote', back_populates='vendor')

    def add_product(self,
                    session,
                    brand_name,
                    product_name,
                    price,
                    discount=0.0):
        _brand = session.query(Brand).filter(Brand.name == brand_name).first()
        _product = session.query(Product).filter(
            Product.name == product_name).first()

        if not _brand:
            _brand = Brand(name=brand_name)
            self.brands.append(_brand)
            session.add(_brand)

        if not _product:
            _product = Product(name=product_name, brand=_brand)
            session.add(_product)

        if _brand and _product:
            _quote = Quote(product=_product,
                           vendor=self,
                           currency=self.currency,
                           value=price,
                           discount=discount)
            session.add(_quote)


class Brand(Object, Base):
    """Manufacturing Entity"""
    vendors = relationship('Vendor',
                           secondary=VendorBrand,
                           back_populates='brands')
    products = relationship('Product', back_populates='brand')


class Product(Object, Base):
    """Item sold by brand via vendor"""
    brand_id = Column(Integer, ForeignKey('brand.id'))
    brand = relationship('Brand', back_populates='products')
    quotes = relationship('Quote', back_populates='product')


class Quote(Base):
    """Quoted Quote of Item from a vendor"""
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    # time_created = Column(DateTime(timezone=True), default=func.now())
    date_created = Column(Date, default=func.now())
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship('Product', back_populates='quotes')
    vendor_id = Column(Integer, ForeignKey('vendor.id'))
    vendor = relationship('Vendor', back_populates='quotes')
    currency = Column(String, default='USD')
    value = Column(Float)
    discount = Column(Float, default=0.0)

    def __repr__(self):
        return f"<Quote({self.vendor.name} / {self.product.brand.name} {self.product.name} / {self.value} {self.currency})>"



def mk_adder(session, vendor):
    def _func(brand, product, price, discount=0.0):
        vendor.add_product(session, brand, product, price, discount)
        session.commit()
    return _func


if __name__ == '__main__':
    from eralchemy import render_er
    render_er(Base, 'doc/er_diagram.svg')

