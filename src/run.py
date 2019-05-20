from flask import Flask, Response
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from decouple import config
import json


application = Flask(__name__)
api = Api(application)
application.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = config('SECRET_KEY')

db = SQLAlchemy(application)
application.config['JWT_SECRET_KEY'] = config('JWT_SECRET_KEY')
jwt = JWTManager(application)

application.config['JWT_BLACKLIST_ENABLED'] = True
application.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


from . import models, resources


@application.route("/", methods=["GET"])
def health_check():
    return Response(
        response=json.dumps({'error': 'none', 'data': 'Health check good.'}),
        status=200,
        mimetype='application/json'
    )


api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/graphql')