from flask_restful import Resource, reqparse
import sqlite3

class Users:

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_name(cls, username):

        try:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()

            query = "SELECT * FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            res = cursor.fetchone()

            if res:
                user = cls(*res)
            else:
                user = None

            connection.close()
            return user

        except:
            return {"message": "Internal server error when getting users details using username"},500

    @classmethod
    def find_by_id(cls, id):

        try:
            connection = sqlite3.connect("data.db")
            cursor.execute(query, (username,))
            res = cursor.fetchone()

            if res:
                user = cls(*res)
            else:
                user = None

            connection.close()
            return user

        except:
            return {"message": "Internal server error"},500


class CreateUsers(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username",
        type=str,
        required=True,
        help="username is required"
    )
    parser.add_argument("password",
        type=str,
        required=True,
        help="password is required"
    )

    def post(self):

        data = CreateUsers.parser.parse_args()

        try:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()

            insert_query = "INSERT INTO users(username, password) VALUES(?, ?)"
            search_query = "SELECT id, username, password FROM users WHERE username = ?"

            cursor.execute(search_query, (data["username"],))
            res = cursor.fetchone()

            if res:
                return {"message": "User exists in database"}
            else:
                cursor.execute(insert_query,(data["username"], data["password"],))
                connection.commit()
                connection.close()
                return {"message": "user created successfully thank you."}
        except:
            return {"message": "interval server error"},500
        finally:
            connection.close()


class ListUsers(Resource):

    def get(self):

        try:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()

            query = "SELECT id, username, password FROM users"
            cursor.execute(query)

            users = []
            res = cursor.fetchall()

            if res:
                for row in res:
                    users.append({"user_id": row[0], "username": row[1], "password": row[2]})
                    connection.close()
                return {"users": users},200
            else:
                return {"message": "no user found in database"},404

        except:
            return {"message": "iInternal server error"}, 500