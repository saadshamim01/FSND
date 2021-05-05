import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS

from flask_migrate import Migrate
from flask import abort
import random

from models import setup_db, Actor, Movie
from auth import requires_auth, AuthError

from datetime import datetime

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
#    CORS(app)
#
#    @app.after_request
#    def after_request(response):
#        response.headers.add(
#            'Access-Control-Allow-Headers', 'Content-Type, Authorization, true'
#        )
#        response.headers.add(
#            'Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS'
#        )
#        response.headers.add('Access-Control-Allow-origins', '*')
#        return response


    @app.route('/')
    def hello():
        return jsonify({
                       "success": True,
                       "message": "Hello world"
                       }), 200


####################### Two get requests

    @app.route('/actors')
    @requires_auth('get: actors')
    def get_actors(payload):
        actors = Actor.query.order_by('id').all()
        actor = [actor.format() for actor in actors]

        if len(actor) == 0:
            abort(404)

        return jsonify({
                       "success": True,
                       "Actor": actor
                           }), 200

        #curl -X GET http://127.0.0.1:5000/actors
        #curl -X GET http://127.0.0.1:5000/actors --header 'authorization: Bearer {YOUR_ACCESS_TOKEN}'

    @app.route('/movies')
    @requires_auth('get: movies')
    def get_movies(payload):
        movies = Movie.query.order_by('id').all()
        movie = [movie.format() for movie in movies]


        if len(movie) == 0:
            abort(404)

        return jsonify({
                       "success": True,
                       "Movie": movie
                       }), 200
        #curl -X GET http://127.0.0.1:5000/movies
        #curl -X GET http://127.0.0.1:5000/movies --header 'authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5pdUhhd0JjNmxoeExFV1BULVY2aiJ9.eyJpc3MiOiJodHRwczovL2ZzbmQxOTk4LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDhjYmU5NGUzNTI1NjAwNzE3NmE3N2MiLCJhdWQiOiJjYXBzdG9uZV9hcGkiLCJpYXQiOjE2MjAxMDE1NjksImV4cCI6MTYyMDEwODc2OSwiYXpwIjoiWlpSeWVpVGNmSExNbGNTQldYcGdaSnJlUzNiTmRFdmIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTogYWN0b3IiLCJkZWxldGU6IG1vdmllIiwiZ2V0OiBhY3RvcnMiLCJnZXQ6IG1vdmllcyIsInBhdGNoOiBhY3RvciIsInBhdGNoOiBtb3ZpZSIsInBvc3Q6IGFjdG9yIiwicG9zdDogbW92aWUiXX0.JR8drN93slBiVCJ46_7S2yua7AVgeC0WlMjoV_vrKh5tBSk5Kv9diY2FP5QYX1x0NspqMqO6gp1roUC4M2JnPsAYrcWXcdyfgOGK-AeRv9uSkj4uQfc77vReGAbTRte-_K3VOBgUGrcRJUXJHrk9T50nd53Z3taQaNH9EEDRA6qnYPn-QRdB8rla_n6ctStBWloC6MXCPJ4_gcC0JaGhNbRoT_EoiVG9Kz2AyEov4Hn8marLs2tR4LRo7YluRePcQ57bx37OVbmPmypj2PgDV5ShByxU_DVIWKRcOKs-ZU6lMeScIAjDcp1hDP3rO1LVCeT-th2kmzmL1pdDyaWb7g'

######################### Two delete requests

    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete: actor')
    def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                print(sys.exc_info())
                abort(404)

            actor.delete()
            return jsonify({
                           'success': True,
                           'delete': actor.format()

                           }), 200

        except Exception as e:
          print(e)
          abort(422)

            #curl -X DELETE http://127.0.0.1:5000/actors/1

    @app.route('/movies/<movie_id>', methods=['DELETE'])
    @requires_auth('delete: movie')
    def delete_movies(payload, movie_id):
      try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
          print(sys.exc_info())
          abort(404)

        movie.delete()
        return jsonify({
                       'success': True,
                       'delete': movie.format()
                       })
      except:
        abort(422)

        #curl -X DELETE http://127.0.0.1:5000/movies/1
        #curl -X DELETE http://127.0.0.1:5000/movies/4 --header 'authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im5pdUhhd0JjNmxoeExFV1BULVY2aiJ9.eyJpc3MiOiJodHRwczovL2ZzbmQxOTk4LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDhjYmU5NGUzNTI1NjAwNzE3NmE3N2MiLCJhdWQiOiJjYXBzdG9uZV9hcGkiLCJpYXQiOjE2MTk5NTY3NjcsImV4cCI6MTYxOTk2Mzk2NywiYXpwIjoiWlpSeWVpVGNmSExNbGNTQldYcGdaSnJlUzNiTmRFdmIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTogYWN0b3IiLCJkZWxldGU6IG1vdmllIiwiZ2V0OiBtb3ZpZXMiLCJwYXRjaDogYWN0b3IiLCJwYXRjaDogbW92aWUiLCJwb3N0OiBhY3RvciIsInBvc3Q6IG1vdmllIl19.iH_hTM7TImsP02tQdyXGprPXdtRMXelnzSGAwRZha4Fg3uRXQlSQbEKRv1ubkhW-gqhiS7lSdNySyuP50iVyijTvJljdtC5bNn3yAn_9FK7he5l6FFaWTRAYZj4woXdOQAPGY7wv5xyuQEeyUKJEk86H4ErQQPapqcaJrOHYXlOlXfjdcqae2efR-WJBp6AS7HYDPwiBX6igKyzS6y7XviPqyAe_IvCTH2hVmBAbtrmOToTJPSol4v0qXl0cn0gV2xKfr4zSFYSt9tumdiJmfvftSS5UcW3zCZxz9hUv_IF5qccjzgdzcc13nM_fvmy0uqVSXe269G_s1BnsVP4qyA'


########################## 2 post requests

    @app.route('/actors', methods=['POST'])
    @requires_auth('post: actor')
    def create_actors(payload):
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        if new_name is None:
          print('Something is None')
          abort(404)

        try:
          actor = Actor(name=new_name,age=new_age,gender=new_gender)

          print(actor.name)
          actor.insert()
          return jsonify({
                           'success': True,
                           'create': actor.format()

                           }), 200
        except Exception as e:
          print(e)
          abort(422)

#curl -X POST -H "Content-Type: application/json" -d '{"name":"saad","age":"23","gender":"Male"}' http://127.0.0.1:5000/actors
#curl -X POST -H "Content-Type: application/json" -d '{"name":"saad","age":"23","gender":"Male"}' http://127.0.0.1:5000/actors

    @app.route('/movies', methods=['POST'])
    @requires_auth('post: movie')
    def create_movies(payload):
      body = request.get_json()
      new_title = body.get('title', None)
      new_release_date = body.get('release_date', None)
      print(new_title)
      print(new_release_date)

      try:
        if (new_title is None):
          abort(404)

        movie = Movie(title=new_title,release_date=new_release_date)
        movie.insert()
        return jsonify({
                       'success': True,
                       'create': movie.format()
                       })

      except Exception as e:
        print (e)
        abort(422)

#curl -X POST -H "Content-Type: application/json" -d '{"title":"Iron Man 2","release_date":"12-12-2002 00:00:00"}' http://127.0.0.1:5000/movies

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch: actor')
    def edit_actor(payload, actor_id):
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.name = new_name
            actor.age = new_age
            actor.gender = new_gender
            actor.update()
            return jsonify({
                           'success': True,
                           'edit': actor.format()
                           }), 200

        except Exception as e:
          print(e)
          abort(422)

#curl http://127.0.0.1:5000/actors/4 -X PATCH -H "Content-Type: application/json" -d '{"name":"ruby", "age": "21", "gender": "Female"}'

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch: movie')
    def edit_movie(payload, movie_id):
        body = request.get_json()
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.title = new_title
            movie.release_date = new_release_date
            movie.update()
            return jsonify({
                           'success': True,
                           'edit': movie.format()
                           }), 200
        except Exception as e:
            print (e)
            abort(422)

#curl http://127.0.0.1:5000/movies/10 -X PATCH -H "Content-Type: application/json" -d '{"title":"Age of Ultron"}'


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

# JWT Errors
    @app.errorhandler(401)
    def unauthorized_request(error):
      return jsonify({
                     "success": False,
                     "error": 401,
                     "message": "unauthorized request"
                     })

    @app.errorhandler(403)
    def forbidden_request(error):
      return jsonify({
                     "success": False,
                     "error": 403,
                     "message": "forbidden request"
                     })



    @app.errorhandler(AuthError)
    def handle_auth_error(e):
      response = jsonify(e.error)
      response.status_code = e.status_code
      return response

    return app

#    app = create_app()
app = create_app()

#    if __name__ == '__main__':
#        APP.run(host='0.0.0.0', port=8080, debug=True)