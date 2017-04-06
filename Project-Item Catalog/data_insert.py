from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey
from sqlalchemy import Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from database_setup import Item, Category


db_String = "postgresql:///cat"
Base = declarative_base()
engine = create_engine(db_String)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
q = session.query(Item)
q.delete()
q = session.query(Category)
q.delete()
session.commit()
cat = Category(name='Other')
session.add(cat)
session.commit()
f_key = cat.id
item = Item(name='test', desc="test", category_id=f_key, user='1')
session.add(item)
session.commit()
print item.user
print"*****************"
