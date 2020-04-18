from flask import Blueprint, request, jsonify, abort
import json
from models import db_drop_and_create_all, setup_db, db, Actor, Movie
from auth import AuthError, requires_auth
casting_blueprint = Blueprint('gsprod-api', __name__)


# ROUTES
'''
@TODO implement endpoint
    GET /movies | GET /actors
        it should be a public endpoint
        it should contain only the item's data representation
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


'''
@TODO implement endpoint
    GET /actors/<id> | GET /movies/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should contain the item's data representation
    returns status code 200 and json {"success": True, "item": item} where item is dictonary containing only the requested item
        or appropriate status code indicating reason for failure
'''


@casting_blueprint.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        return jsonify({
            'success': True,
            'movie': [movie.format()]
        }), 200
    else:
        abort(404, 'Actor with id: {} not found'.format(movie_id))


@casting_blueprint.route('/actors/<int:actor_id>', methods=['GET'])
def get_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor:
        return jsonify({
            'success': True,
            'actor': [actor.format()]
        }), 200
    else:
        abort(404, 'Actor with id: {} not found'.format(actor_id))


'''
@TODO implement endpoint
    POST /movies | POST /actors
        it should create a new row in the correct table
        it should require the 'post:item' permission
    returns status code 200 and json {"success": True, "items": item} where items is an array containing only the newly created item
        or appropriate status code indicating reason for failure
'''
@casting_blueprint.route('/movies', methods=['POST'])
# @requires_auth('post:movies')
# def post_movie(jwt):
def post_movie():
    """Create a new Movie with the POST method"""
    if request.method != 'POST':
        abort(405)
    data = request.get_json()
    title = data['title']
    # release_date = data['release_date']
    print('title/release_date', title)  # release_date
    if title:  # and release_date
        movie = Movie(
            title=title
            # release_date=release_date
        )
        print('adding', movie)
        try:
            movie.insert()
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(422)
        finally:
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200
            db.session.close()

    else:
        abort(404)


@casting_blueprint.route('/actors', methods=['POST'])
# @requires_auth('post:actors')
# def post_movie(jwt):
def post_actor():
    """Create a new Actor with the POST method"""
    if request.method != 'POST':
        abort(405)
    data = request.get_json()
    name = data['name']
    age = data['age']
    gender = data['gender']
    print('name/age/gender', name, age, gender)
    if name and gender:
        actor = Actor(
            name=name,
            age=age,
            gender=gender
        )
        print('adding', actor)
        try:
            actor.insert()
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(422)
        finally:
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200
            db.session.close()

    else:
        abort(404)


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
# def permission_error(exception):
#     return jsonify({
#         'error': exception.error,
#         'status': exception.status_code
#     })
