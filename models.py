from sqlalchemy import Column, Integer, String, REAL, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column

from database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50), unique=True)
    password = Column(String(50))
    ipn = Column(Integer, unique=True)
    full_name = Column(String(150))
    contacts = Column(String(150))
    photo = Column(String(150))
    passport = Column(String(150))

    def __init__(self, login, password, ipn, full_name, contacts, photo, passport):
        self.login = login
        self.password = password
        self.ipn = ipn
        self.full_name = full_name
        self.contacts = contacts
        self.photo = photo
        self.passport = passport

    def __repr__(self):
        return f'<User {self.name!r}>'

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo = Column(String(150))
    name = Column(String(150))
    description = Column(String(250))
    price_hour = Column(REAL)
    price_day = Column(REAL)
    price_week = Column(REAL)
    price_month = Column(REAL)
    owner = mapped_column(ForeignKey('user.id'))
    available = Column(Integer)

    def __init__(self, photo, name, description, price_hour, price_day, price_week, price_month, owner, available):
        self.photo = photo
        self.name = name
        self.description = description
        self.price_hour = price_hour
        self.price_day = price_day
        self.price_week = price_week
        self.price_month = price_month
        self.owner = owner
        self.available = available

class Contract(Base):
    __tablename__ = 'contract'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(250))
    start_date = Column(String(20))
    end_date = Column(String(20))
    contract_num = Column(Integer)
    leaser = mapped_column(ForeignKey('user.id'))
    taker = mapped_column(ForeignKey('user.id'))
    item = mapped_column(ForeignKey('item.id'))
    status = Column(String(10))

    def __init__(self, text, start_date, end_date, contract_num, leaser, taker, item, status):
        self.text = text
        self.start_date = start_date
        self.end_date = end_date
        self.contract_num = contract_num
        self.leaser = leaser
        self.taker = taker
        self.item = item
        self.status = status

class Favourites(Base):
    __tablename__ = 'favourites'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = mapped_column(ForeignKey('user.id'))
    item = mapped_column(ForeignKey('item.id'))

    def __init__(self, user, item):
        self.user = user
        self.item = item

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = mapped_column(ForeignKey('user.id'))
    user = mapped_column(ForeignKey('user.id'))
    text = Column(String(250))
    grade = Column(Integer)
    contract = mapped_column(ForeignKey('contract.id'))

    def __init__(self, author, user, text, grade, contract):
        self.author = author
        self.user = user
        self.text = text
        self.grade = grade
        self.contract = contract

class Search_History(Base):
    __tablename__ = 'search_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = mapped_column(ForeignKey('user.id'))
    search_text = Column(String(250))
    timestamp = Column(DateTime)

    def __init__(self, user, search_text, timestamp):
        self.user = user
        self.search_text = search_text
        self.timestamp = timestamp
