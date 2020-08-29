# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Endpoints

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

GET '/questions'
- return a list of questions, 
  number of total questions, current category, categories
- Request Arguments: None
- Return: An object with the keys ["questions","total_questions","current_category","categories"]
{"categories":{"1":"Science","2":"Art","3":"Geography","4":"History","5":"Entertainment","6":"Sports"},
    "current_category":{"id":6,"type":"Sports"},
    "questions":[{"answer":"Brazil","category":6,"difficulty":3,"id":10,"question":"Which is the ...."},.....],
    ,"total_questions":18}
    
```

DELETE '/questions/<int:q_id>'
- DELETE question using a question ID
- Request Arguments: <q_id> the id of the question to delete
- Return: An object with the key "id" and the value of the id of the question deleted
    {"id": 4}
```
POST '/questions/add'
- POST a new question, which will require the question and answer text
- Request Arguments: None
- Return: An object with the key "question" and the value of the question that have been added
    {"question": {"answer":"Brazil","category":6,"difficulty":3,"id":10,"question":"Which is the ...."}}
```   
  
POST '/questions'
- a POST endpoint to get questions based on a search term
- Request Arguments: None
- Return: An object with the keys ["questions","total_questions","currentCategory"] with all the questions the  match the search term
    {{"current_category":{"id":6,"type":"Sports"},
    "questions":[{"answer":"Brazil","category":6,"difficulty":3,"id":10,"question":"Which is the ...."},.....],
    ,"total_questions":18}
``` 
GET "/categories/<id>/questions"
- a GET endpoint to get questions based on category
- Request Arguments: id of the category 
- Return: An object with the keys ["questions","total_questions","currentCategory"] with all the questions the  match the search term
    {{"current_category":{"id":6,"type":"Sports"},
    "questions":[{"answer":"Brazil","category":6,"difficulty":3,"id":10,"question":"Which is the ...."},.....],
    ,"total_questions":18}
``` 
POST ""/quizzes""
-  POST endpoint to get questions to play the quiz 
        return a random questions within the given category, 
  if provided, and that is not one of the previous questions

- Request Arguments: None
- Return: An object with the key "question" with a questions within the given category and that is not one of the previous questions
    {"questions": {"answer":"Brazil","category":6,"difficulty":3,"id":10,"question":"Which is the ...."}}
``` 


  
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```