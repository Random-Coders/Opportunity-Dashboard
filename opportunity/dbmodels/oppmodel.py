from opportunity.dbmodels.manager import connect

class Opportunity(object):

	def __init__(self,):

		self.db = connect("opportunity")

	def add(self, opp_title, img_url, desc, link, topic, author):
		opp_obj = { 
			"title": opp_title,
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
		# if result.inserted_id:
		# 	return True
		# else:
		# 	return False