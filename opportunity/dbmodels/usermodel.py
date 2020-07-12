from opportunity.dbmodels.manager import connect
from flask_login import UserMixin, login_user
from opportunity import login_manager, bcrypt
import uuid

# class User:

#     def __init__(self, email, title, password):

#         self.db = connect("users")

#         self.email = email
#         self.title = title
#         self.password = password

#         self.is_authenticated = False
#         self.is_active = False
#         self.is_anonymous = False
        

#     def store(self):
#         user_obj = { 
#             "email": self.email,
#             "title": self.title,
#             "password": self.password
#         }
#         # start a collection
#         users_collection = self.db.users

#         result = users_collection.insert_one(user_obj)
#         # for now return status of db insert
#         if result.inserted_id:
#             return True
#         else:
#             return False

#     def get_id(self):
#         query = {"email":self.email}
#         user = self.db.users.find(query)[0]
#         return user['_id']

#     def __repr__(self):
#         return '<User {}>'.format(self.email)
users_db = connect('users').users

class User(UserMixin):

    def __init__(self, email, title, password, _id=None):

        self.email = email
        self.title = title
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self._id

    @classmethod
    def get_by_title(cls, title):
        data = users_db.users.find_one({"title": title})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_email(cls, email):
        data = users_db.users.find_one({"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = users_db.users.find_one({"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        verify_user = User.get_by_email(email)
        if verify_user is not None:
            return bcrypt.check_password_hash(verify_user.password, password)
        return False

    @classmethod
    def register(cls, email, title, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls( email, title, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False

    def to_json(self):
        user_obj = {
            "_id": self._id,
            "email": self.email,
            "title": self.title,
            "password": self.password
        }
        return 

    def save_to_mongo(self):
        users_db.users.insert_one({
            "_id": self._id,
            "email": self.email,
            "title": self.title,
            "password": self.password
            })