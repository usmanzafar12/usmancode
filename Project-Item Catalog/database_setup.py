""" This file sets up the database with some dummy data"""
from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey
from sqlalchemy import Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method


db_String = "postgresql:///cat"
Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50))


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50))
    desc = Column(Text())
    user = Column(Text())
    category_id = Column(Integer(), ForeignKey('category.id'))


def make_db():
    Base = declarative_base()
    engine = create_engine(db_String)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session
