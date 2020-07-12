from opportunity.dbmodels.manager import connect

class CommManager(object):

    def __init__(self):

        self.db = connect("community")


    def create(self, title, desc, topic):
        comm_obj = {
                "title": title,
                "description": desc,
                "topic": topic,
                "count": 1,
                "follow": 1,
                "post_id": ""
            }
        topic_col.insert_one(comm_obj)

    def upcount(self, topic, post_id):
        # get's the topic and post id of the most recent post in a community

        # start a collection
        topic_col = self.db.topic

        addtopic = topic_col.find_one({"topic": topic})

        if addtopic is None:
            comm_obj = {
                "title": title,
                "description": desc,
                "topic": topic,
                "count": 1,
                "follow": 1,
                "post_id": post_id
            }
            topic_col.insert_one(comm_obj)

            print(f"Successfully added the topic {topic}")
        else:
            comm_obj = {
                "title": title,
                "description": desc,
                "topic": topic,
                "count": addtopic['count'] + 1,
                "follow": addtopic['follow'],
                "post_id": post_id
            }
            query = {"topic": topic}
            topic_col.update(query, {"$set": comm_obj})

            print(f"Successfully updated the topic {topic}")

    def getleaders(self, top=3):
        topic_col = self.db.topic

        toptopic = topic_col.find().sort("count").limit(top)

        opp_ids = [opp['post_id'] for opp in toptopic]

        opp_posts = []

        opp_col = connect('opportunity').opps
        for _id in opp_ids:
            opp_posts.append(opp_col.find_one({"_id": _id}))

        return opp_posts


