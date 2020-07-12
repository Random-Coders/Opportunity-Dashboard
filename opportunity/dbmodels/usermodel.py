from opportunity.dbmodels.manager import connect

class User(object):

    def __init__(self, email, title, password):

        self.db = connect("users")

        self.email = email
        self.title = title
        self.password = password

        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = False
        

    def store(self):
        user_obj = { 
            "email": self.email,
            "title": self.title,
            "password": self.password
        }
        # start a collection
        users_collection = self.db.users

        result = users_collection.insert_one(user_obj)
        # for now return status of db insert
        if result.inserted_id:
            return True
        else:
            return False

    def get_id(self):
        self.

    def __repr__(self):
        return '<User {}>'.format(self.email)