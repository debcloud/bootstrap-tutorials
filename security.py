from users import Users

def authenticate(username, password):
    user = Users.find_by_name(username)
    if user and user.password == password:
        return user

def identity(payload):
    user_payload = payload["identity"]
    return Users.find_by_id(user_payload)