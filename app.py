import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv


from db import db
from blocklist import BLOCKLIST 
import models


from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint



def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()    #this is find .env file att the project and load it .


    app.config["PROPAGATE_EXEPTIONS"] = True    # flask configuration if there is an exception that occurs hidden inside an extention of flask to propagate into the main app so that we can see it .

    app.config["API_TITLE"] = "Stores REST API" # flask-smorest configuration
    app.config["API_VERSION"] = "v1"            # flask-smorest configuration
    app.config["OPENAPI_VERSION"] = "3.0.3"     # flask-smorest configuration open API is a standard for API documentation  
    app.config["OPENAPI_URL_PREFIX"] = "/"      # just tells flask-smorest where the root of the API is 

    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui" # tells flask-smorest to use swagger for the API documentaion that's in /swagger-ui
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" # load the swagger code from here so that it can use it to display the documentation
    
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)  # initializes the Flask SQLAlchmey extension, giving it our Flask app so that it can connect the flask app to SQLAlchemy

    migrate = Migrate(app, db)

    api = Api(app)   # connect the flask-smorest extention to the flask app

    app.config["JWT_SECRET_KEY"] = "mahdi"
    jwt = JWTManager(app)


    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked", "error":"token_revoked"}
            ),
            401,
        )
    

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return(
            jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required.",
            }
            ),
            401,
        )
    

    @jwt.additional_claims_loader       
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin":True}
        return {"is_admin":False}
    

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({"message": "The token has expired.", "error":"token_expired"}),
            401,
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):      # when take <<error>> there is no JWT or it's not valid .
        return(
            jsonify({"message":"Signature verification faild", "error":"invalid_token"}),
            401,
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify(
            {
                "description":"Request does not contain an access token.",
                "error":"authorization_required.",
            }
            ),
            401,
        )


    api.register_blueprint(ItemBlueprint)   #from resources.item
    api.register_blueprint(StoreBlueprint)  #from resources.store
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    
    return app
        