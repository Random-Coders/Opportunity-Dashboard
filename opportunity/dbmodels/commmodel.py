from opportunity.dbmodels.manager import connect

class CommManager(object):

    def __init__(self):

        self.db = connect("community")


    def create(self, title, desc, topic):

        # start a comm collection
        comm_col = self.db.comm

        comm_obj = {
                "title": title,
                "description": desc,
                "topic": topic,
                "count": 0,
                "follow": 0,
                "post_id": None
            }
        comm_col.insert_one(comm_obj)

        print(f"Successfully added the community {topic}")

    def upcount(self, topic, post_id):
        # get's the comm and post id of the most recent post in a community

        # start a collection
        comm_col = self.db.comm

        # find all communities with topic
        comm_list = comm_col.find({"topic": topic})

        for comm in comm_list:
            comm_obj = {
                "title": comm['title'],
                "description": comm['description'],
                "topic": topic,
                "count": comm['count']+1,
                "follow": comm['follow'],
                "post_id": post_id
            }
            comm_col.update({'_id': comm['_id']}, {"$set" : comm_obj})



    def getleaders(self, top=3):
        comm_col = self.db.comm

        toptopic = comm_col.find().sort("count").limit(top)

        opp_ids = [opp['post_id'] for opp in toptopic]

        opp_posts = []

        opp_col = connect('opportunity').opps
        for _id in opp_ids:
            opp_posts.append(opp_col.find_one({"_id": _id}))

        return opp_posts


