from opportunity.dbmodels.manager import connect

class CommManager(object):

    def __init__(self):

        self.db = connect("community")

    def upcount(self, topic, post_id):
        # get's the topic and post id of the most recent post in a community

        # start a collection
        topic_col = self.db.topic

        addtopic = topic_col.find_one("topic": topic)

        if addtopic is None:
            comm_obj = {
                "topic": topic,
                "count": 0,
                "post_id": post_id
            }
            topic_col.insert_one(comm_obj)

            print(f"Successfully added the topic {topic}")
        else:
            comm_obj = {
                "topic": topic,
                "count": addtopic['count'] + 1,
                "post_id": post_id
            }
            query = {"topic": topic}
            topic_col.update(query, {"$set": comm_obj})

            print(f"Successfully updated the topic {topic}")