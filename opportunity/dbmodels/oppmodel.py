from opportunity.dbmodels.manager import connect
from opportunity.dbmodels.commmodel import CommManager

class Opportunity(object):

    def __init__(self, opp_title=None, date=None, img_url=None, desc=None, link=None, topic=None, author_name=None, authorid=None):

        self.db = connect("opportunity")

        # ability to store properties in object
        self.opp_title = opp_title
        self.date = date
        self.img_url = img_url
        self.desc = desc
        self.link = link
        self.topic = topic
        self.author_name = author_name
        self.authorid = authorid

    def add(self, opp_title, date, img_url, desc, link, topic, author, authorid):
        opp_obj = { 
            "title": opp_title,
            "date": date,
            "imgurl": img_url,
            "desc": desc,
            "link": link,
            "topic": topic,
            "authorname": author,
            "authorid": authorid
        }
        # start a collection
        opp_col = self.db.opps

        result = opp_col.insert_one(opp_obj)
        # for now return status of db insert
        if result.inserted_id:
            #commmanager = CommManager()
            #commmanager.upcount(topic, result.inserted_id)
            return result
        return None

    def delete(self, identification):
        item = { "_id" : identification }
        self.db.opps.delete_one(item)

    def edit(self, identification, thing, value):
        item = { "_id" : identification }
        newvalues = { "$set": { thing : value } }

        self.db.opps.update_one(item, newvalues)

    def load_all(self):
        return self.db.opps.find().sort("date", -1)

    def load_recent_posts(self, num=1):
        # returns a cursor but data can be accessed through a for loop or through indices
        # load the most recent posts going up to num
        return self.db.opps.find().sort("date", -1).limit(num)

    def load_spliced(self, skip=0, batch_size=5):
        return self.db.opps.find().sort("date", -1).limit(batch_size).skip(int(skip))

    def __repr__(self):
        return '<Opportunity {}>'.format(self.username)