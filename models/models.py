# this is where you write the code to create tables and columns.
from time import time
from database import db

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    # Foreign Key - serves as the bridge between table 1 and table 2
    login_id = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)


class Login(db.Model):
    __tablename__ = 'logins'
    # this id is primary key
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(5), nullable=False)
    # this is the key code(or invisible column) that connect primary key and foreign key
    # colum name = table name i want to connect
    accounts = db.relationship("Account", uselist=False, backref="logins")
    reservations = db.relationship("Reservation", uselist=False, backref="logins")
    orders = db.relationship("Order", uselist=False, backref="logins")


class Reservation(db.Model):
    __tablename__ ='reservations'

    id = db.Column(db.Integer, primary_key=True)
    res_date = db.Column(db.Date, nullable=False)
    res_time = db.Column(db.String(50), nullable=False)
    num_guest = db.Column(db.String(10), nullable=False)
    login_id = db.Column(db.Integer, db.ForeignKey('logins.id'), nullable=False)
    orders = db.relationship("Order", uselist=False, backref="reservations")


class Category(db.Model):
    __tablename__ = 'categories'
    # this is PK for Menu
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    menus = db.relationship("Menu", uselist=False, backref="categories")


class Menu(db.Model):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    menu_name = db.Column(db.String(50), nullable=False)
    menu_price = db.Column(db.Integer, nullable=False)
    menu_pic = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    orders = db.relationship("Order", uselist=False, backref="menus")


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    # all FK
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'), nullable=False)
    login_id = db.Column(db.Integer,  db.ForeignKey('logins.id'),nullable=False)



    