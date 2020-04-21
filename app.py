import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, setup_db
from api import (
    casting_blueprint, unprocessable, bad_request, method_not_allowed, internal_sever_error, not_found, permission_error
)


def create_app(test_config=None):
    app = Flask(__name__)
    app.register_blueprint(casting_blueprint, url_prefix='/api')
    app.register_error_handler(422, unprocessable)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, internal_sever_error)
    app.register_error_handler(404, not_found)
    app.register_error_handler(401, permission_error)

    setup_db(app)
    migrate = Migrate(app, db)
    # cors = CORS(app)
    cors = CORS(app, resources={r"/api*": {"origins": "*"}})


    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello"
        if excited == 'true':
            greeting = greeting + "!!!!!"
        else:
            greeting = greeting + "?????"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app


app = create_app()


if __name__ == '__main__':
    app.run()

# starter:
# https://github.com/udacity/FSND/tree/master/projects/capstone/heroku_sample/starter
