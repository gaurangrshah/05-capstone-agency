import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import db_drop_and_create_all, setup_db, db, Actor, Movie  # 🚨 IMPORT MODELS
from auth import AuthError, requires_auth  # ✅ IMPORT AUTH
# from app import app # 🚨 IMPORT APP

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

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
@app.route('/movies', methods=['GET'])
def get_movies():
    """Returns a list of objects with a short-form representation of movies or actors"""
    all_movies = Movie.query.all()

    if all_movies is None:
        abort(404, 'There are no movies available')

    short_movie = [movie.short() for movie in all_movies]

    return jsonify({
        'success': True,
        'movies': short_movie
    }), 200


@app.route('/actors', methods=['GET'])
def get_actors():
    """Returns a list of objects with a short-form representation of actors"""
    all_actors = Actor.query.all()

    if all_actors is None:
        abort(404, 'There are no actors available')

    short_actor = [actor.short() for actor in all_actors]

    return jsonify({
        'success': True,
        'actors': short_actor
    }), 200


# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


@app.errorhandler(500)
def internal_sever_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500


@app.errorhandler(401)
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


@app.errorhandler(404)
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


@app.errorhandler(AuthError)
def invalid_claims(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": error.__dict__
