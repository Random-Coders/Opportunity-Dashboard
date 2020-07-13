from opportunity.dbmodels.manager import connect
from bson.objectid import ObjectId

class CommManager(object):

    def __init__(self):

        self.db = connect("community")


    def create(self, title, desc, img):

        # start a comm collection
        comm_col = self.db.comm

        comm_obj = {
                "title": title,
                "description": desc,
                "img": img,
                "count": 0,
                "follow": 0,
            }
        comm_col.insert_one(comm_obj)

    def upcount(self, _id):
        # get's the comm and post id of the most recent post in a community

        # start a collection
        comms = self.load_all()
        identification = ObjectId(_id)

        for comm in comms:
            if identification == comm['_id']:
                comm_obj = {
                    "title": comm['title'],
                    "description": comm['description'],
                    "img": comm['img'],
                    "count": comm['count']+1,
                    "follow": comm['follow'],
                }
                self.db.comm.update_one({'_id': comm['_id']}, {"$set" : comm_obj})
                break

    def downcount(self, _id):
        # get's the comm and post id of the most recent post in a community

        # start a collection
        comms = self.load_all()
        identification = ObjectId(_id)

        for comm in comms:
            if identification == comm['_id']:
                comm_obj = {
                    "title": comm['title'],
                    "description": comm['description'],
                    "img": comm['img'],
                    "count": comm['count']-1,
                    "follow": comm['follow'],
                }
                self.db.comm.update_one({'_id': comm['_id']}, {"$set" : comm_obj})
                break

    def load_all(self):
        return self.db.comm.find()

    def edit(self, identification, thing, value):
        item = { "_id" : identification }
        newvalues = { "$set": { thing : value } }

        self.db.comm.update_one(item, newvalues)


    def getTop(self, top=3):
        return self.db.comm.find().sort('count', -1).limit(top)


    def getleaders(self, top=3):
        comm_col = self.db.comm

        toptopic = comm_col.find().sort("count", -1).limit(top)

        opp_ids = [opp['post_id'] for opp in toptopic]

        opp_posts = []

        opp_col = connect('opportunity').opps
        for _id in opp_ids:
            opp_posts.append(opp_col.find_one({"_id": _id}))

        return opp_posts


