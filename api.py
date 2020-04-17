from flask import Blueprint, request, jsonify, abort
import json
from models import db_drop_and_create_all, setup_db, db, Actor, Movie  # 🚨 IMPORT MODELS
from auth import AuthError, requires_auth  # ✅ IMPORT AUTH
casting_blueprint = Blueprint('gsprod-api', __name__)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

print(db)


# ROUTES
'''
@TODO implement endpoint
    GET /movies GET /actors
        it should be a public endpoint
        it should contain only the item.short() data representation
    returns status code 200 and json {"success": True, "item": items} where items is the list of movies or actors
        or appropriate status code indicating reason for failure
'''
@casting_blueprint.route('/movies', methods=['GET'])
def get_movies():
    """Returns a list of objects with a short-form representation of movies or actors"""
    all_movies = Movie.query.all()

    if all_movies is None:
        abort(404, 'There are no movies available')

    movie_titles = [movie.title for movie in all_movies]

    return jsonify({
        'success': True,
        'movies': movie_titles
    }), 200


@casting_blueprint.route('/actors', methods=['GET'])
def get_actors():
    """Returns a list of objects with a short-form representation of actors"""
    all_actors = Actor.query.all()

    if all_actors is None:
        abort(404, 'There are no actors available')

    actor_names = [actor.name for actor in all_actors]

    return jsonify({
        'success': True,
        'actors': actor_names
    }), 200

# '''
# @TODO implement endpoint
#     GET /drinks-detail
#         it should require the 'get:drinks-detail' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
#         or appropriate status code indicating reason for failure
# '''
# @app.route('/drinks-detail', methods=['GET'])
# @requires_auth('get:drinks-detail')
# def get_drinks_detail(jwt):
#     """Returns a list of objects containing a long-form representation of Drinks """
#     all_drinks = Drink.query.all()

#     if all_drinks is None:
#         abort(404, 'There are no drinks available')

#     long_drink = [drink.long() for drink in all_drinks]

#     return jsonify({
#         'success': True,
#         'drinks': long_drink
#     }), 200


# '''
# @TODO implement endpoint
#     POST /drinks
#         it should create a new row in the drinks table
#         it should require the 'post:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
#         or appropriate status code indicating reason for failure
# '''
# @app.route('/drinks', methods=['POST'])
# @requires_auth('post:drinks')
# def post_drink(jwt):
#     """Create a new Drink with the POST method"""
#     if request.method != 'GET' and request.method != 'POST':
#         abort(405)

#     try:
#         data = request.get_json()

#         drink = Drink(
#             title=data.get('title', None),
#             recipe=json.dumps(data.get('recipe', None))
#         )

#         drink.insert()
#     except Exception:
#         db.session.rollback()
#         abort(422)
#     finally:
#         return jsonify({
#             'success': True,
#             'drinks': [drink.long()]
#         }), 200
#         db.session.close()


# '''
# @TODO implement endpoint
#     PATCH /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should update the corresponding row for <id>
#         it should require the 'patch:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
#         or appropriate status code indicating reason for failure
# '''
# @app.route('/drinks/<int:drink_id>', methods=['PATCH'])
# @requires_auth('patch:drinks')
# def patch_drink(jwt, drink_id):
#     """Update a pre-existing Drink using the PATCH method"""
#     data = request.get_json()

#     drink = Drink.query.get(drink_id)

#     if drink is None:
#         abort(404, 'Drink not found')

#     try:
#         drink.title = data.get('title')
#         drink.recipe = data.get('recipe')
#         drink.update()
#     except Exception:
#         db.session.rollback()
#         abort(422)
#     finally:
#         return jsonify({
#             'success': True,
#             'drinks': [drink.long()]
#         }), 200
#         db.session.close()


# '''
# @TODO implement endpoint
#     DELETE /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should delete the corresponding row for <id>
#         it should require the 'delete:drinks' permission
#     returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
#         or appropriate status code indicating reason for failure
# '''
# @app.route('/drinks/<int:drink_id>', methods=['DELETE'])
# @requires_auth('delete:drinks')
# def delete_drink(jwt, drink_id):
#     """Delete an existing drink using the DELETE method"""
#     drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

#     if drink is None:
#         abort(404, 'Drink not found.')

#     try:
#         drink.delete()
#     except Exception:
#         db.session.rollback()
#         abort(422)
#     finally:
#         return jsonify({
#             'success': True,
#             'delete': drink_id
#         }), 200
#         db.session.close()


# Error Handling
'''
Example error handling for unprocessable entity
'''
@casting_blueprint.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @casting_blueprint.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@casting_blueprint.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@casting_blueprint.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


@casting_blueprint.errorhandler(500)
def internal_sever_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500


@casting_blueprint.errorhandler(401)
def permission_error(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Authentication error"
    }), 401


'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@casting_blueprint.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


# @casting_blueprint.errorhandler(AuthError)
# def invalid_claims(error):
#     return jsonify({
#         'success': False,
#         'error': 401,
#         'message': error.__dict__
#     })


@casting_blueprint.errorhandler(AuthError)
def handle_auth_error(exception):
    return jsonify({
        'error': exception.error,
        'status': exception.status_code
    })
