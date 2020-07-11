from manager import connect

class Opportunity(object):

	def __init__(self,):

		self.db = connect("opportunity")
		