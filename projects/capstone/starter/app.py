import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from flask_migrate import Migrate
from flask import abort
import random

from models import setup_db, Actors, Movies

from datetime import datetime

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    #db = SQLAlchemy(app)
    #migrate = Migrate(app, db)
    #CORS(app)


    @app.route('/')
    def hello():
        return jsonify({
                       "success": True,
                       "message": "Hello world"
                       })


# Two get requests

    @app.route('/actors')
    def get_actors():
        actors = Actors.query.order_by('id').all()
        actor = [actor.format() for actor in actors]

        if len(actor) == 0:
            abort(404)

        return jsonify({
                       "success": True,
                       "Actor": actor
                           }), 200

        #curl -X GET http://127.0.0.1:5000/actors

    @app.route('/movies')
    def get_movies():
        movies = Movies.query.order_by('id').all()
        movie = [movie.format() for movie in movies]


        if len(movie) == 0:
            abort(404)

        return jsonify({
                       "success": True,
                       "Movie": movie
                       }), 200
        #curl -X GET http://127.0.0.1:5000/movies


    @app.route('/actors/<actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        try:
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

            if actor is None:
                print(sys.exc_info())
                abort(404)

            actor.delete()
            return jsonify({
                           'success': True,
                           'delete': actor_id
                           }), 200
        except:
            abort(422)

            #curl -X DELETE http://127.0.0.1:5000/actors/1



    @app.route('/actors', methods=['POST'])
    def create_actors():
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        try:
            new_actor = Actors(name=new_name, age=new_age, gender=new_gender)
            Actors.insert(new_actor)

            return jsonify({
                           'success': True,
                           'created': 'ss'
                           }), 200
        except:
            abort(422)

#curl -X POST -H "Content-Type: application/json" -d '{"name":"saad","age":23,"gender":"Male"}' http://127.0.0.1:5000/actors
#curl -X POST -H "Content-Type: application/json" -d '{"name":"saad","age":23,"gender":"Male"}' http://127.0.0.1:5000/actors/add

    @app.route('/actors/<actor_id>')
    def edit_actor(actor_id):
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.name = new_name
            actor.age = new_age
            actor.gender = new_gender
            actor.update()
            return jsonify({
                           'success': True,
                           'actor': actor
                           })

        except Exception as e:
            print(e)
            abort(422)

#curl http://127.0.0.1:5000/actors/2 -X PATCH -H "Content-Type: application/json" -d '{"name":"Saasdd"}'



#@app.route('/drinks/<int:id>', methods=['PATCH'])
#@requires_auth("patch:drinks")
#def update_drink(payload, id):
#    body = request.get_json()
#    new_title = body.get('title', None)
#    new_recipe = body.get('recipe', None)
#
#    drink = Drink.query.filter(Drink.id == id).one_or_none()
#
#    if drink is None:
#        abort(404)
#
#    try:
#        drink.title = new_title
#        drink.recipe = json.dumps(new_recipe)
#        drink.update()
#        return jsonify({
#                       'success': True,
#                       'drinks': [drink.long()]
#                       }), 200
#    except Exception as e:
#        print(e)
#        abort(422)




#    Two GET requests
#One POST request
#One PATCH request
#One DELETE request

    return app

    APP = create_app()

    if __name__ == '__main__':
        APP.run(host='0.0.0.0', port=8080, debug=True)



## Imports
##----------------------------------------------------------------------------#
#import sys
#import json
#import dateutil.parser
#import babel
#from flask import Flask, render_template, request, Response, flash, redirect, url_for
#from flask_moment import Moment
#from flask_sqlalchemy import SQLAlchemy
#import logging
#from logging import Formatter, FileHandler
#from flask_wtf import Form
#from flask_migrate import Migrate
#from alembic import op
#from forms import *
#from flask import abort
#from datetime import datetime
##----------------------------------------------------------------------------#
## App Config.
##----------------------------------------------------------------------------#
#
#app = Flask(__name__)
#moment = Moment(app)
#app.config.from_object('config')
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)
#
## TODO: connect to a local postgresql database
#
##----------------------------------------------------------------------------#
## Models.
##----------------------------------------------------------------------------#
#
##Setting up the show Database
#class Show(db.Model):
#  __tablename__ = 'Show'
#  id = db.Column(db.Integer, primary_key=True)
#  venue_id = db.Column(db.Integer, db.ForeignKey(
#        'Venue.id'), nullable=False)
#  artist_id = db.Column(db.Integer, db.ForeignKey(
#        'Artist.id'), nullable=False)
#  start_time = db.Column(db.DateTime, nullable=False)
#
#  def __repr__(self):
#    return f'<Show Id: {self.id} Venue_ID: {self.venue_id}, Artist_ID: {self.artist_id}>'