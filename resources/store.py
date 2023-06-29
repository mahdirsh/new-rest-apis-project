import uuid 
from flask import request
from flask.views import MethodView          #used for ceating a class and the methods of that class, route to specific endpoints.
from flask_smorest import Blueprint, abort  #Blueprint is used to divide an API into multiple segments

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema


blp = Blueprint("stores", __name__, description="Operations on stores")



@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
        

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message" : "Store deleted ."}
        

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):        #store_data can be called  whatever you want
        store = StoreModel(**store_data)
        
        try:                     
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="An store with that name already exist ."
            )    
        except SQLAlchemyError :
            abort(500, message="An error occurred while inserting the store .")

        return store, 201          # marshmallow can turn any object to JSON
                                   # for example in here store is a list
                                   # but marshmallow turn it to the JSON
    

