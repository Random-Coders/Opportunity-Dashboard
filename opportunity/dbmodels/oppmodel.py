from opportunity.dbmodels.manager import connect

class Opportunity(object):

    def __init__(self, opp_title=None, date=None, img_url=None, desc=None, link=None, topic=None, author=None):

        self.db = connect("opportunity")

        # 
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
            return True
        else:
            return False
    def __repr__(self):
        return '<User {}>'.format(self.username)