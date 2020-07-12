from opportunity.dbmodels.manager import connect

class CommManager(object):

    def __init__(self, opp_title=None, date=None, img_url=None, desc=None, link=None, topic=None, author=None):

        self.db = connect("community")

    def upcount(self, topic, post_id):
        # get's the topic and post id of the most recent post in a community

        # start a collection
        topic_col = self.db.topic

        addtopic = topic_col.find_one(topic_col) 

        result = opp_col.insert_one(opp_obj)
        # for now return status of db insert
        if result.inserted_id:
            return True
        else:
            return False

    def load_recent_posts(self, num=1):
        # returns a cursor but data can be accessed through a for loop or through indices
        # load the most recent posts going up to num
        return self.db.opps.find().sort("date", -1).limit(num)

    def load_spliced(self, skip=0, batch_size=5):
        test = self.db.opps.find().sort("date", -1).limit(batch_size).skip(skip)
        for i in test:
            print(i)
        return 'as'

    def __repr__(self):
        return '<User {}>'.format(self.username)