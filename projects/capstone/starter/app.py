import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS

from flask_migrate import Migrate
from flask import abort
import random

from models import setup_db, Actors, Movies

from datetime import datetime

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
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
          actor = Actors(name=new_name, age=new_age, gender=new_gender)

          print(actor.name)
          actor.insert()
          return jsonify({
                           'success': True,
                           'created': actor
                           }), 200
        except:
            abort(422)

#curl -X POST -H "Content-Type: application/json" -d '{"name":"saad","age":23,"gender":"Male"}' http://127.0.0.1:5000/actors
#curl -X POST -H "Content-Type: application/json" -d '{"name":"saad","age":23,"gender":"Male"}' http://127.0.0.1:5000/actors/add

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
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
                           }), 200

        except Exception as e:
            print(e)
            abort(422)

#curl http://127.0.0.1:5000/actors/2 -X PATCH -H "Content-Type: application/json" -d '{"name":"Saasdd"}'

    @app.errorhandler(404)
    def not_found(error):
      return jsonify({
                     "success": False,
                     "error": 404,
                     "message": "resource not found"
                     }), 404

    @app.errorhandler(422)
    def unprocessable(error):
      return jsonify({
                     "success": False,
                     "error": 422,
                     "message": "unprocessable"
                     }), 422

    @app.errorhandler(400)
    def bad_request(error):
      return jsonify({
                     "success": False,
                     "error": 400,
                     "message": "bad request"
                     }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
      return jsonify({
                   "success": False,
                   "error": 405,
                   "message": "method not allowed"
                     }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
      return jsonify({
                   "success": False,
                   "error": 500,
                   "message": "internal server error."
                     }), 500

    return app

    APP = create_app()

    if __name__ == '__main__':
        APP.run(host='0.0.0.0', port=8080, debug=True)



