import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Shop, Stock, Sale

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

login = os.environ.get("login")
password = os.environ.get("password")
host_name = os.environ.get("host_name")
port = os.environ.get("port")
db_name = os.environ.get("db_name")

DSN = f'postgresql://{login}:{password}@{host_name}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

models = {'publisher': Publisher, 'book': Book, 'shop': Shop, 'stock': Stock, 'sale': Sale}

with open('tests_data.json') as f:
    data = json.load(f)

for info in data:
    model = models.get(info['model'])
    session.add(model(id=models.get(info['pk']), **info['fields']))
    session.commit()

enter = input('Введите имя или идентификатор издателя: ')

print(f'\nМагазины, продающие книги издателя {enter}:')
if enter.isdigit():
    for c in session.query(Publisher, Shop).join(Book).join(Stock).\
        join(Shop).filter(Publisher.id == int(enter)).all():
        print(c.Shop.name)
else:
    for c in session.query(Publisher, Shop).join(Book).join(Stock).\
        join(Shop).filter(Publisher.name == enter).all():
        print(c.Shop.name)

print(f'\nФакты покупки книг издателя {enter}:')
if enter.isdigit():
    for c in session.query(Publisher, Book, Shop, Sale).join(Book).join(Stock).\
        join(Shop).join(Sale).filter(Publisher.id == int(enter)).all():
        print('|'.join([c.Book.title.ljust(40), c.Shop.name.ljust(10),\
                         c.Sale.price.ljust(10), c.Sale.date_sale.ljust(25)]))
else:
    for c in session.query(Publisher, Book, Shop, Sale).join(Book).join(Stock).\
        join(Shop).join(Sale).filter(Publisher.name == enter).all():
        print('|'.join([c.Book.title.ljust(40), c.Shop.name.ljust(10),\
                         c.Sale.price.ljust(10), c.Sale.date_sale.ljust(25)]))

