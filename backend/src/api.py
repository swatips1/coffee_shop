import os
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS

#Authentication
from .auth.auth import AuthError, requires_auth
# Exception handling
from sqlalchemy.exc import *
# Misc functions used by the routes
from .lib import *

app = Flask(__name__)
setup_db(app)

#Authentication settings
cors = CORS(app, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

''' after_request decorator: setting Access-Control-Allow '''
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

'''
Initialize the datbase
'''
db_drop_and_create_all()

# Notes: A lot of googling and research went into making different parts of the project work.
# Yet, no code has been copied from internet as is. Most of it was to understand how to apply different concepts.
# Main souces were stockoverflow, google, sqlAlchemy documentation, flask documentation, auth0 documentation and Udacity help
# Some of the code was re-purposed/re-factored from my own fyuur and trivia projects.


'''
Routes
'''

'''
-----------------------------------------------------------
This endpoint to handles GET requests for all
available drinks.
-----------------------------------------------------------
***********************************************************
Required Permissions: None. Public endpoint
Expected Inputs: None
Expected Output:
     list of all drinks from database when successful.
     The list doesnt contain details of the drinks.
     Error otherwise.
***********************************************************
-----------------------------------------------------------
Required Permissions: None. Public Route.
-----------------------------------------------------------
-----------------------------------------------------------
Linked tests:test_get_drinks
-----------------------------------------------------------
'''
@app.route('/drinks', methods=['GET'])
def drinks():
    try:
        drinks = get_drinks()
    except Exception as e:
        print(e)
        return jsonify({'success': False,
                        'message': e})
    return jsonify({'success': True,
                    'drinks' : drinks})

'''
-----------------------------------------------------------
This endpoint to handles GET requests for all
available drinks.
-----------------------------------------------------------
***********************************************************
Required Permissions: 'get:drinks-detail'
Expected Inputs: None
Expected Output:
    list of all drinks from database when successful.
    The list contains all the details of the drinks.
    Error otherwise.
***********************************************************
-----------------------------------------------------------
Required Permissions: get:drinks-detail
-----------------------------------------------------------
-----------------------------------------------------------
Linked tests:test_get_drinks_detailed
-----------------------------------------------------------
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def detailed_drinks(payload):
    try:
        drinks = get_detailed_drinks()
    except Exception as e:
        print(e)
        return jsonify({'success': False,
                        'message': e})
    return jsonify({'success': True,
                    'drinks' : drinks})


'''
-----------------------------------------------------------
This endpoint handles creation of new drink via POST
It returns the newly added drink.
-----------------------------------------------------------
***********************************************************
Required Permissions: 'post:drinks'
Expected Inputs:
title: String. Upto 80 characters
recipe: String containing color, name and parts.
        Upto 180 characters.
Expected Output:
    Newly added drink with all details of the drink.
    Error otherwise.
***********************************************************
-----------------------------------------------------------
Required Permissions: post:drinks
-----------------------------------------------------------
-----------------------------------------------------------
Linked tests:test_add_drink, test_del_drink
-----------------------------------------------------------
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    title = request.get_json()['title']
    recipe = request.get_json()['recipe']
    if title is None or recipe is None:
        abort(422)
    drink =""
    try:
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
        drinks = get_detailed_drinks()
    except IntegrityError:
        return jsonify({'success': False,
                      'message' : 'Drink with title ' + title + ' already exists. Please check the title of your drink'})
    except Exception as e:
        print(e)
        return jsonify({'success': False,
                      'message': e})
    return jsonify({'success': True,
                    'drinks' : drinks})

'''
-----------------------------------------------------------
This endpoint handles changes of a drink via POST
It returns the updated drink.
-----------------------------------------------------------
***********************************************************
Required Permissions: 'patch:drinks'
Expected Inputs:
    id: id of the drink that will be updated.
    title: Optional. String. Upto 80 characters.
    recipe: Optional. String containing color, name and parts.
            Upto 180 characters.
Expected Output:
    Updated drink with all details of the drink.
    Error 404 otherwise.
***********************************************************
-----------------------------------------------------------
Required Permissions: patch:drinks
-----------------------------------------------------------
-----------------------------------------------------------
Linked tests:test_update_drink
-----------------------------------------------------------
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)
    try:
        title = request.get_json()['title']
        recipe = request.get_json()['recipe']
        if title is not None:
            drink.title = title
        if recipe is not None:
            drink.recipe = json.dumps(recipe)
        drink.update()
    except IntegrityError:
        return jsonify({'success': False,
                        'message' : 'Update failed. Drink with title ' + title + ' already exists. Please check the title of your drink'})
    except Exception as e:
        print(e)
        return jsonify({'success': False,
                        'message': e})
    return jsonify({'success': True,
                    'drinks' : drink.long()})

'''
-----------------------------------------------------------
This endpoint handles deletion of drink via POST
It returns the id of the deleted drink.
-----------------------------------------------------------
***********************************************************
Required Permissions: 'delete:drinks'
Expected Inputs:
    id: id of the drink that will be updated.
    title: Optional. String. Upto 80 characters.
    recipe: Optional. String containing color, name and parts.
            Upto 180 characters.
Expected Output:
    Updated drink with all details of the drink.
    Error 404 otherwise.
***********************************************************
-----------------------------------------------------------
Required Permissions: delete:drinks
-----------------------------------------------------------
-----------------------------------------------------------
Linked tests:test_del_drink
-----------------------------------------------------------
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)
    try:
        print("found drink with id :", drink.id)
        drink.delete()
    except Exception as e:
        print(e)
        return jsonify({'success': False,
                        'message': e})
    return jsonify({'success': True,
                    'drinks' : id})

'''
# ***********************************************************
# Error Handler
# ***********************************************************
#-----------------------------------------------------------
 Example error handling for server error
#-----------------------------------------------------------
'''

@app.errorhandler(500)
def internal_server(error):
  return jsonify({
         "success": False,
         "error": 500,
         "message": "internal server error"
     }), 500

'''
#-----------------------------------------------------------
 Example error handling for unprocessable entity
#-----------------------------------------------------------
'''
@app.errorhandler(422)
def unprocessable(error):
  return jsonify({
           "success": False,
           "error": 422,
           "message": "unprocessable"
       }), 422

'''
#-----------------------------------------------------------
 Example error handling for resource not found
#-----------------------------------------------------------
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404
'''
#-----------------------------------------------------------
 Example error handling for bad request
#-----------------------------------------------------------
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
      }), 400

'''
#-----------------------------------------------------------
 Example error handling for AuthError
#-----------------------------------------------------------
'''
@app.errorhandler(AuthError)
def not_authorized(AuthError):
    return jsonify({
          "success": False,
          "error": AuthError.status_code,
          "message": AuthError.error['code']
      }), 401
