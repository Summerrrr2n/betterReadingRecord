# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import time
from datetime import datetime
from betterReadingRecord.extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    locale = db.Column(db.String(20))
    items = db.relationship('Item', back_populates='author', cascade='all')


    read_records = db.relationship('ReadRecord', back_populates='user', cascade='all')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='items')


class ReadRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='read_records')
    book_name = db.Column(db.String)



    def as_dict(self):

        def get_column(self, name):
            if name is 'start_time' or 'end_time':
                return datetime.strftime(getattr(self, name),'%Y-%m-%d %H:%M:%S')
            else:
                return getattr(self, name)
                
        return {c.name: str(get_column(self, c.name)) for c in self.__table__.columns}


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String)
