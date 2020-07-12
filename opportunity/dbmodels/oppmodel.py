from opportunity.dbmodels.manager import connect
from opportunity.dbmodels.commmodel import CommManager

class Opportunity(object):

    def __init__(self, opp_title=None, date=None, img_url=None, desc=None, link=None, topic=None, author=None):

        self.db = connect("opportunity")

        # ability to store properties in object
        self.opp_title = opp_title
        self.date = date
        self.img_url = img_url
        self.desc = desc
        self.link = link
        self.topic = topic
        self.author = author

    def add(self, opp_title, date, img_url, desc, link, topic, author):
        opp_obj = { 
            "title": opp_title,
            "date": date,
            "imgurl": img_url,
            "desc": desc,
            "link": link,
            "topic": topic,
            "author": author
        }
        # start a collection
        opp_col = self.db.opps

        result = opp_col.insert_one(opp_obj)
        # for now return status of db insert
        if result.inserted_id:
            commmanager = CommManager()
            commmanager.upcount(topic, result.inserted_id)
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
        return '<Opportunity {}>'.format(self.username)