from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from items import Items, ListItems
from security import authenticate, identity
from users import CreateUsers, ListUsers

app=Flask(__name__)
api=Api(app)
app.secret_key = "whothefuckdoyouthinkyouarebro"
jwt = JWT(app, authenticate, identity)

api.add_resource(Items, "/api/v1/items", "/api/v1/items/<string:name>")
api.add_resource(ListItems, "/api/v1/items/list")
api.add_resource(CreateUsers, "/api/v1/users/create")
api.add_resource(ListUsers, "/api/v1/users/list")

if __name__=="__main__":
    app.run(port=5000, debug=True)