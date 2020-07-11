from manager import connect

class Opportunity(object):

	def __init__(self,):

		self.db = connect("opportunity")

	def add(opp_title, img, desc, link, topic, author):
		opp_obj = { 
			"title": opp_title,
			"img": img,
			"desc": desc,
			"link": link,
			"topic": topic,
			"author": author
		}

		result = posts.insert_one(post_data)
		# for now 
		if result.inserted_id:
			return True
		else:
			return False