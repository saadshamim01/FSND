import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)


  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  CORS(app, resources={r"/api/*": {"origins": "*"}})

#  '''
#  @TODO: Use the after_request decorator to set Access-Control-Allow
#  '''

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  @app.route('/')
  def home():
    return jsonify({
            'hello': 'home'
            })

  '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.

  '''

  @app.route("/categories")
  def get_categories():
    cat = Category.query.all()
    #categories = [category.format() for category in cat]
    categories_dict = {}
    for category in cat:
      categories_dict[category.id] = category.type
    return jsonify({
          "success": True,
          "categories": categories_dict,
          "total_categories": len(categories_dict)
      }), 200

#    #THEN CURL USING curl -X GET http://127.0.0.1:5000/categories


  '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

  @app.route('/questions')
  def get_questions():
    selection = Question.query.all()
    current_questions = paginate_questions(request, selection)
    categories = Category.query.all()
    #formatted_categories = [category.format() for category in categories]
    categories_dict = {}
    for category in categories:
      categories_dict[category.id] = category.type

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
                   'success': True,
                   'questions': current_questions,
                   'total_questions': len(Question.query.all()),
                   'categories': categories_dict,
                   'currentCategory': None
                     }), 200




#curl : curl http://127.0.0.1:5000/questions\?page\=2


  '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

  @app.route('/questions/<int:question_id>', methods =['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        print(sys.exc_info())
        abort(404)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
                     'success': True,
                     'deleted': question_id,
                     'questions': current_questions,
                     'total_questions': len(Question.query.all())
                     })
    except:
      abort(422)

#                   curl -X DELETE http://127.0.0.1:5000/questions/12


  '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    try:
      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      question.insert()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
                     'success': True,
                     'created': question.id,
                     'questions': current_questions,
                     'total_questions': len(Question.query.all())
                     })
    except:
      abort(422)

#curl -X POST -H "Content-Type: application/json" -d '{"question": "Who is the best?", "answer": "Saad Shamim", "category": "1", "difficulty": "3"}' http://127.0.0.1:5000/questions/add

  '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_question():
    body = request.get_json()
    print(body)
    search = body.get('searchTerm', None)
    if not search:
            abort(422)
    print(search)

    try:
      selection = Question.query.filter(Question.question.ilike('%{}%'.format(search))).all()
      current_questions = paginate_questions(request, selection)
      print(current_questions)
      return jsonify({
                     'success': True,
                     'questions': current_questions,
                     'total_questions': len(selection),
                     'current_category': None
                     })

    except:
      abort(404)

#  '''
#  @TODO:
#  Create a GET endpoint to get questions based on category.
#
#  TEST: In the "List" tab / main screen, clicking on one of the
#  categories in the left column will cause only questions of that
#  category to be shown.
#  '''

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_categories_questions(category_id):

    selection = Question.query.filter(Question.category == category_id).all()
    current_questions = paginate_questions(request, selection)

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
                   'success': True,
                   'questions': current_questions,
                   'total_questions': len(current_questions)
                   })

    #curl -X GET http://127.0.0.1:5000/categories/4


  '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()
    previous_questions = body.get('previous_questions', [])
    quiz_category = body.get('quiz_category', None)
    number = quiz_category['id']
    print (number)
    try:
      quiz = Question.query.filter_by(category=number).all()

      #To check if the questions are loaded, error checking.
      if not quiz:
        return abort(422)


      selected_questions = []
      for question in quiz:
        if question.id not in previous_questions:
          selected_questions.append(question.format())
      if len(selected_questions) != 0:
        results = random.choice(selected_questions)
        return jsonify({
                       'question': results
                       })
      else:
        return jsonify({
                       'question': False
                       })
    except:
      flash('Unable to load questions.')


#  '''
#  @TODO:
#  Create error handlers for all expected errors
#  including 404 and 422.
#  '''

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

  return app

