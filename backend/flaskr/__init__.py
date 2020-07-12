import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs --> done
  '''
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow --> done
  '''

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE")
        return response

    # helper func

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories. --> done
  '''

    @app.route('/categories', methods=['GET'])
    def categories():
        try:
            response = {
                "categories": {c.id: c.type for c in Category.query.all()}
            }
            return jsonify(response)
        except:
            abort(500)

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. --> done
  '''

    @app.route('/questions', methods=['get'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        questions = [q.format() for q in Question.query.order_by(Question.id).all()]
        if len(questions[start:end]) == 0:
            abort(404)
        current_q = questions[-1]
        response = {
            "questions": questions[start:end],
            "total_questions": Question.query.count(),
            "current_category": Category.query.get(current_q["category"]).format(),
            "categories": {c.id: c.type for c in Category.query.all()}
        }
        return jsonify(response)

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
    
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    @app.route('/questions/<int:q_id>', methods=["DELETE"])
    def delete_q(q_id):
        try:
            q = Question.query.get(q_id)
            q.delete()
            return jsonify({"id": q_id})
        except:
            abort(400)

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  --> ???
  '''

    @app.route("/questions/add", methods=['POST'])
    def create_q():
        try:
            q = Question(
            question=request.json['question'],
            answer=request.json['answer'],
            category=request.json['category'],
            difficulty=request.json['difficulty']
        )

            q.insert()

            questions = Question.query.order_by(Question.id).all()
            return jsonify(
                {
                    "question": questions[-1].format(),
                }
            )
        except:
            abort(400)
    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    @app.route("/questions", methods=['POST'])
    def search():
        word = request.json['searchTerm']

        questions = [q.format() for q in Question.query.filter(Question.question.ilike(
            "%" + word + "%")).all()]
        if len(questions) > 0:
            current_q = questions[-1]
            return jsonify(
                {
                    "questions": questions,
                    "total_questions": Question.query.filter(Question.question.ilike(
                        "%" + word + "%")).count(),
                    "currentCategory": Category.query.get(current_q["category"]).format()

                }
            )
        else:
            return jsonify(
                {
                    "questions": [],
                    "total_questions": 0,
                    "currentCategory": {"id": 0, "type": ""}

                }
            )

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route("/categories/<id>/questions", methods=['GET'])
    def category_questions(id):
        try:
            questions = Question.query.filter(Question.category == id).all()
            questions = [q.format() for q in questions]

            return jsonify(
                {
                    "questions": questions,
                    "totalQuestions": Question.query.filter(Question.category == id).count(),
                    "currentCategory": Category.query.get(id).format()
                }
            )
        except:
            abort(404)
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

    @app.route("/quizzes", methods=["POST"])
    def quiz():
        try:
            category = request.json['quiz_category']
            previous = request.json['previous_questions']
            if category['id'] != 0:
                questions = Question.query.filter(Question.id.notin_(previous)).filter(
                    Question.category == category['id']).all()
            else:
                questions = Question.query.filter(Question.id.notin_(previous)).all()
            if len(questions) > 0:
                return jsonify(
                    {
                        "question": questions[random.randint(1, len(questions)) - 1].format()
                    }
                )
            return jsonify(
                {
                    "question": False
                }
            )
        except:
            abort(400)
    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 404,
                "message": "Not Found"
            }
        ), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 422,
                "message": "Unprocessable"
            }
        ), 422

    @app.errorhandler(400)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 400,
                "message": "Bad Request"
            }
        ), 400

    @app.errorhandler(500)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 500,
                "message": "server error"
            }
        ), 500

    return app
