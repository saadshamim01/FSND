# Udacity Capstone Casting Agency

You can setup the website by following the setup instructions.

## Setup

Clone the repository in your computer using this [link](). Before starting the project you need to download the necessary plugins using.

```
pip install -r requirements.txt
```

After installing the dependencies you can start working on the project.

Navigate to the starter folder. The project can be started using

```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --reload
```

## Endpoints

- List of endpoints

GET '/actors'
GET '/movies'
POST '/actors'
POST '/movies'
PATCH '/actors/<int:actor_id>'
PATCH '/movies/<int:movie_id>'
DELETE '/actors/<int:actor_id>'
DELETE '/movies/<int:movie_id>'


- The endpoints can be accessed by

Casting Assistant
Casting Director
Executive Producer


#### GET '/actors'

- Returns an array of actors with their id, name, age,gender and success status.
- Request Arguments: None
- Curl sample: curl -X GET http://127.0.0.1:5000/actors

```
{
  "Actor": [
    {
      "age": 22,
      "gender": Male,
      "id": 1,
      "name": "Actor 1"
    },
    {
      "age": 22,
      "gender": Male,
      "id": 1,
      "name": "Actor 2"
    }
  ],
  "success": true
}
```

#### GET '/movies'
- Returns an array of actors with their id, title, release date and success status.
- Request Arguments: None
- Curl sample: curl -X GET http://127.0.0.1:5000/movies

```
{
  "Movie": [
    {
      "id": 1,
      "release_date": "12-12-2012",
      "title": "Movie 1"
    },
    {
      "id": 2,
      "release_date": "12-12-2012",
      "title": "Movie 2"
    }
  ],
  "success": true
}
```

#### POST '/actors'
- Returns an array of actors with their id, name, age, gender and success status.
- Request Arguments: {"name" : "Actor 1", "age" : "22", "gender" : "Male"}
- Curl sample: curl -X POST -H "Content-Type: application/json" -d '{"name":"Movie 1","age":"22","gender":"Male"}' http://127.0.0.1:5000/actors

```
{
  "create": {
    "age": 22,
    "gender": "Male",
    "id": 1,
    "name": "Actor 1"
  },
  "success": true
}
```

#### POST '/movies'
- Creates an object with their id, title, release date and success status.
- Request Arguments: {"title" : "Movie 1","release_date" : "12-12-2012"}
- Curl sample: curl -X POST -H "Content-Type: application/json" -d '{"title":"Iron Man 2","release_date":"12-12-2002 00:00:00"}' http://127.0.0.1:5000/movies

```
{
  "create": {
    "id": 1,
    "release_date": "12-12-2012",
    "title": "Movie 1"
  },
  "success": true
}
```

#### PATCH '/actors/1'

- Creates an object with id, name, age, gender and success status.
- Request Arguments: "name" : "Actress 1", "age" : "22", "gender" : "Female"
- Curl sample: curl http://127.0.0.1:5000/actors/2 -X PATCH -H "Content-Type: application/json" -d '{"name":"Actress", "age": "23", "gender": "Female"}'

```
{
  "edit": {
    "age": 22,
    "gender": "Female",
    "id": 4,
    "name": "Actress 1"
  },
  "success": true
}
```
#### PATCH '/movies/1'

- Creates an object with id, title, release date and success status.
- Request Arguments: "title": "Movie 2", "release_date": "12-12-2002 00:00:00"
- Curl sample: curl http://127.0.0.1:5000/movies/2 -X PATCH -H "Content-Type: application/json" -d '{"title":"Movie 2","release_date":"2002-12-12 00:00:00"}'

```
{
  "edit": {
    "id": 1,
    "release_date": "Thu, 12 Dec 2002 00:00:00 GMT",
    "title": "Movie 2"
  },
  "success": true
}
```

#### DELETE '/questions/<int:question_id>'
- Fetches the questions list after deleting a selected question
- Request Arguments: question_id
- Results are paginated.
- Returns an object with questions deleted question id, list, success status and total number of questions.

- Curl sample: curl -X DELETE http://127.0.0.1:5000/questions/5


## Authentication

#### Casting Assistant

- Can GET actors and movies list only

Username: saad_basic@udacity.com

Password: Ironman@321

#### Casting Director

- Can GET, POST, PATCH actors and movies list

Username: saad_intermediate@udacity.com

Password: Ironman@321

#### Executive Producer

- Can GET, POST, PATCH and DELETE actors & movies list

Username: saad_advance@udacity.com

Password: Ironman@321



## Error Handling


When the APIs failed to do what they design to do, we get errors. Errors are returned in the following format (JSON object). In this project, we will get four types of errors types when the requests fail:

- 400: Bad Request
```
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
                   "success": False,
                   "error": 400,
                   "message": "bad request"
                   }), 400
```

- Resource not found
```
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
                   "success": False,
                   "error": 404,
                   "message": "resource not found"
                   }), 404
```

- 422: Not Processable
```
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
                   "success": False,
                   "error": 422,
                   "message": "unprocessable"
                   }), 422
```

- 405: Method not allowed
```
  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
                 "success": False,
                 "error": 405,
                 "message": "method not allowed"
                   }), 405
```

- 500: Internal Server Error
```
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
                 "success": False,
                 "error": 405,
                 "message": "internal server error."
                   }), 405
```

## Testing
To run the tests, run the following codes:
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
