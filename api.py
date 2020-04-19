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
@requires_auth('get:movies')
def get_movies(jwt):
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
@requires_auth('get:actors')
def get_actors(jwt):
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
@requires_auth('get:movies')
def get_movie(jwt, movie_id):
    print('getting movie for id: {}'.format(movie_id))
    movie = Movie.query.get(movie_id)
    print('found movie', movie.format())
    if movie:
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    else:
        abort(404, 'Actor with id: {} not found'.format(movie_id))


@casting_blueprint.route('/actors/<int:actor_id>', methods=['GET'])
@requires_auth('get:actors')
def get_actor(jwt, actor_id):
    actor = Actor.query.get(actor_id)
    if actor:
        return jsonify({
            'success': True,
            'actor': actor.format()
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
@requires_auth('post:movies')
def post_movie(jwt):
    """Create a new Movie with the POST method"""
    if request.method != 'POST':
        abort(405)
    data = request.get_json()
    movie = Movie(
        title=data['title'],
        year=data['year']
    )
    try:
        movie.insert()
    except Exception as e:
        db.session.rollback()
        abort(422)
    finally:
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
        db.session.close()


@casting_blueprint.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actor(jwt):
    """Create a new Actor with the POST method"""
    if request.method != 'POST':
        abort(405)
    data = request.get_json()
    actor = Actor(
        name=data['name'],
        age=data['age'],
        gender=data['gender']
    )
    try:
        actor.insert()
    except Exception as e:
        db.session.rollback()
        abort(422)
    finally:
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200
        db.session.close()


'''
@TODO implement endpoint
    PATCH /movies/<id> | PATCH /actors/<id> |
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:items' permission
        it should contain the item data representation
    returns status code 200 and json {"success": True, "movie": item} where item an array containing only the updated item
        or appropriate status code indicating reason for failure
'''
@casting_blueprint.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def patch_movie(jwt, movie_id):
    """Update a pre-existing Movie using the PATCH method"""
    data = request.get_json()
    movie = Movie.query.get(movie_id)
    if movie is None:
        abort(404, 'Movie not found')
    try:
        movie.title = data.get('title')
        movie.year = data.get('year')
        movie.update()
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        return jsonify({
            'success': True,
            'movies': [movie.format()]
        }), 200
        db.session.close()


@casting_blueprint.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def patch_actor(jwt, actor_id):
    """Update a pre-existing Actor using the PATCH method"""
    data = request.get_json()
    actor = Actor.query.get(actor_id)
    if actor is None:
        abort(404, 'Actor not found')
    try:
        actor.title = data.get('title')
        actor.name = data.get('name')
        actor.age = data.get('age')
        actor.gender = data.get('gender')
        actor.update()
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        return jsonify({
            'success': True,
            'actors': [actor.format()]
        }), 200
        db.session.close()


'''
@TODO implement endpoint
    DELETE /movies/<id> | DELETE /actors/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:item' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@casting_blueprint.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(jwt, movie_id):
    """Delete an existing movie using the DELETE method"""
    movie = Movie.query.filter(Movie.id == movie_id)
    if movie is None:
        abort(404, 'Movie not found.')
    try:
        movie.delete()
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        return jsonify({
            'success': True,
            'delete': movie_id
        }), 200
        db.session.close()


@casting_blueprint.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(jwt, actor_id):
    """Delete an existing actor using the DELETE method"""
    actor = Actor.query.filter(Actor.id == actor_id)
    if actor is None:
        abort(404, 'Actor not found.')
    try:
        actor.delete()
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        return jsonify({
            'success': True,
            'delete': actor_id
        }), 200
        db.session.close()


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


@casting_blueprint.errorhandler(AuthError)
def permission_error(exception):
    return jsonify({
        'error': exception.error,
        'status': exception.status_code
    })


@casting_blueprint.route('/seed')
def add_dummy_data():
    """ Seed Database """
    db_drop_and_create_all()
    actor1 = Actor(name="Sam Jones", age=25, gender='m')
    actor2 = Actor(name="Cynthia Jones", age=22, gender='f')
    actor3 = Actor(name="Vanna White", age=32, gender='f')

    movie1 = Movie(title="The Movie", year=2015)
    movie2 = Movie(title="The Movie 2", year=2016)
    movie3 = Movie(title="The Movie 3", year=2017)

    actor1.insert()
    actor2.insert()
    actor3.insert()
    movie1.insert()
    movie2.insert()
    movie3.insert()

    db.session.commit()
    db.session.close()

    return jsonify({
        "success": 200,
        "message": "db populated successfully"
    })
