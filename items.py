from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Items(Resource):

    parser_1 = reqparse.RequestParser()
    parser_1.add_argument("name",
        type=str,
        required=True,
        help="Product name is required!"
    )
    parser_1.add_argument("price",
        type=float,
        required=True,
        help="Product price is required!"
    )

    parser_2 = reqparse.RequestParser()
    parser_2.add_argument("id",
        type=int,
        required=True,
        help="Please enter the products id"
    )

    @jwt_required()
    def get(self, name):
        
        try:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()

            search_query = "SELECT name, price FROM items WHERE name = ?"
            cursor.execute(search_query, (name,))
            result = cursor.fetchone()
            connection.close()

            if result:
                return {"items": 
                    {"name": result[0], "price": result[1]}
                }, 200
            else:
                return {"message": "Data does not exists in database"}, 400
        except:
            return {"message": "internal server error"}, 500

    @jwt_required()
    def post(self):

        data = Items.parser_1.parse_args()

        try:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
    
            select_query = "SELECT name, price FROM items WHERE name = ?"
            insert_query = "INSERT INTO items(name, price) VALUES(?, ?)"
    
            cursor.execute(select_query, (data["name"],))
            result = cursor.fetchone()
    
            if result:
                return {"message": "product exists in database"}, 400
            else:
                cursor.execute(insert_query, (data["name"], data["price"],))
                connection.commit()
                connection.close()
                return {"item": {
                    "name": data["name"],
                    "price": data["price"],
                    "message": "Data saved successfully"
                    } },200
        except:
            return {"message": "internal server error"}, 500

    @jwt_required()       
    def delete(self):

        try:
            data = Items.parser_2.parse_args()
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()

            select_query = "SELECT name, price FROM items WHERE id = ?"
            delete_query = "DELETE FROM items WHERE id = ?"
            cursor.execute(select_query, (data["id"],))
            result = cursor.fetchone()

            if result:
                cursor.execute(delete_query, (data["id"],))
                connection.commit()
                connection.close()
                return {"message": "Item deleted successfully thanks"}, 200
            else:
                return {"message": "Data not found in database thanks!"}, 400
        except:
            return {"message": "internal server error"}, 500

    @jwt_required()
    def put(self):

        data1 = Items.parser_1.parse_args()
        data2 = Items.parser_2.parse_args()

        try:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()

            search_query = "SELECT name, price FROM items WHERE id = ?"
            update_query = "UPDATE items SET name = ?, price = ? WHERE id = ?"

            cursor.execute(search_query, (data2["id"],))
            row = cursor.fetchone()

            if row:
                cursor.execute(update_query,(data1["name"],data1["price"],data2["id"],))
                connection.commit()
                connection.close()
                return {"message": "item updated successfully thank you."}
            else:
                return {"message": "item not found in database thank you."}
        except:
            return {"message": "internal server error"}, 500

class ListItems(Resource):

    @jwt_required()
    def get(self):
        
        try:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()

            select_query = "SELECT id, name, price FROM items"
            cursor.execute(select_query)
            result = cursor.fetchall()

            items = []
            if result:
                for row in result:
                    items.append({"id": row[0],"name": row[1],"price": row[2]})

                connection.close()
                return {"item": items}
            else:
                return {"message": "There is no item in the database"}
        except:
            return {"message": "iternal server error try again later"}, 500