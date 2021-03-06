from flask import Blueprint, request, jsonify, abort
import json
from models import db_drop_and_create_all, setup_db, db, Actor, Movie
from auth import AuthError, requires_auth

casting_blueprint = Blueprint('gsprod-api', __name__)


# ROUTES
'''
    GET /movies | GET /actors
        it should be a authorized endpoint for avialable to all roles except 'public'
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

    formatted_movies = [movie.format() for movie in all_movies]

    return jsonify({
        'success': True,
        'movies': formatted_movies
    }), 200


@casting_blueprint.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(jwt):
    """Returns a list of objects with a short-form representation of actors"""
    all_actors = Actor.query.all()

    if all_actors is None:
        abort(404, 'There are no actors available')

    formatted_actor = [actor.format() for actor in all_actors]

    return jsonify({
        'success': True,
        'actors': formatted_actor
    }), 200


'''
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
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
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
        print('success')
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
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
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


'''
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
        return jsonify({
            'success': True,
            'movies': [movie.format()]
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
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
        return jsonify({
            'success': True,
            'actors': [actor.format()]
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


'''
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
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404, 'Movie not found.')
    try:
        movie.delete()
        return jsonify({
            'success': True,
            'delete': movie_id
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@casting_blueprint.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(jwt, actor_id):
    """Delete an existing actor using the DELETE method"""
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404, 'Actor not found.')
    try:
        actor.delete()
        return jsonify({
            'success': True,
            'delete': actor_id
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


# Error Handling

@casting_blueprint.errorhandler(422)
def unprocessable(error):
    '''error handler for unprocessable entity'''
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422



@casting_blueprint.errorhandler(400)
def bad_request(error):
    '''error handler for bad request'''
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@casting_blueprint.errorhandler(405)
def method_not_allowed(error):
    '''error handler for method not allowed'''
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


@casting_blueprint.errorhandler(500)
def internal_sever_error(error):
    '''error handler for internal server error'''
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500





@casting_blueprint.errorhandler(404)
def not_found(error):
    '''error handler for resource not found'''
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404




@casting_blueprint.errorhandler(AuthError)
def permission_error(exception):
    '''error handler for AuthError'''
    return jsonify({
        'error': exception.error['description'],
        'status': exception.status_code
    }), 401


@casting_blueprint.route('/seed')
def add_dummy_data():
    '''Seed Database'''
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


@casting_blueprint.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization,true'
    )
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,PATCH,POST,DELETE,OPTIONS'
    )
    print('✅ response after_request', response)
    return response
