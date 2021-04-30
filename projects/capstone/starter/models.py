import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine
from datetime import datetime

database_name = "capstone"
database_path = "postgres://{}:{}@{}/{}".format('saadshamim', 'hello', 'localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Actors(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        self.session.add(self)
        self.session.commit()

    def update(self):
        self.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'age': self.age,
        'gender': self.gender
        }

#    def __repr__(self):
#        return f'<Actors ID: {self.id} Name: {self.name} Age: {self.age} Gender: {self.gender}>'

class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    release_date = db.Column(db.DateTime)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date

    def insert(self):
        self.session.add(self)
        self.session.commit()

    def update(self):
        self.session.commit()

    def delete(self):
        self.session.delete(self)
        self.session.commit()

    def format(self):
        return{
        'title': self.title,
        'release_date': self.release_date
        }

    def __repr__(self):
        return f'<Movies ID: {self.id} Title: {self.title} release_date: {self.release_date}>'



