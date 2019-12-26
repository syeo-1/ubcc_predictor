#confession object
#date, number, the post, number of likes, number of comments, number of shares
import re
import random

# should be close enough: (January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}) .*\n\#(\d{5})\n\n(.*)\n(\d+)
# provides grouping as well, but will need to format likes within the code to extract that data point

# even closer!!! : (January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}) .*\n\#(\d{5})(\n\n.*)+\n(See More\n)?\d+

#should be the closest: (January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}) .*\n\#(\d{5})((\n\n.*)+)\n(See More\n)?\d+
# group 4 and 5 will consist of post, but if only 1 block then just group 5


class Confession:
	"""docstring for ClassName"""
	def __init__(self, month, date, number, post=None, reactions=None):
		self.month = month
		self.date = date
		self.number = number
		self.post = post
		self.reactions = reactions
		self.classification = None

class Classification:
	GREATER = "GREATER"
	LESS = "LESS"

class ConfessionContainer:
	def __init__(self, confessions):
		self.confessions = confessions

	def get_all_posts(self):
		return [confession.post for confession in self.confessions]

	def get_all_classifications(self):
		return [confession.classification for confession in self.confessions]

	def evenly_distribute(self):
		less_than = list(filter(lambda confession: confession.classification == Classification.LESS, self.confessions))
		greater_than = list(filter(lambda confession: confession.classification == Classification.GREATER, self.confessions))

		if len(less_than) < len(greater_than):
			g_small = greater_than[:len(less_than)]
			self.confessions = g_small + less_than
		elif len(greater_than) > len(less_than):
			l_small = less_than[:len(greater_than)]
			self.confessions = l_small + greater_than

		random.shuffle(self.confessions)

class Processor:
	"""docstring for ClassName"""
	def __init__(self, text):
		self.text = text
		self.output = ""
		self.avg_num_reactions = 0

		self.confession_obj = re.compile("(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}) .*\n\#(\d{5})((\n\n.*)+)\n(See More\n)?(\d+)")
		# self.reactions_obj = re.compile("\b(\d+)\1\b")
		self.see_more_obj = re.compile("[ ]\S*\.{3}")
		self.confessions = []
		self.process_text()
		self.calculate_avg_num_reactions()
		self.classify_confessions()
		self.remove_none_classifications()

	def remove_none_classifications(self):
		self.confessions = [confession for confession in self.confessions if confession.classification is not None]

	def calculate_avg_num_reactions(self):
		sum_reactions = 0
		for confession in self.confessions:
			if confession.reactions is None:
				continue
			sum_reactions += confession.reactions
		self.avg_num_reactions = sum_reactions / len(self.confessions)


	def classify_confessions(self):
		i = 0
		while i < len(self.confessions):
			if self.confessions[i].reactions is None:
				i += 1
				continue
			elif self.confessions[i].reactions > self.avg_num_reactions:
				self.confessions[i].classification = Classification.GREATER
			elif self.confessions[i].reactions < self.avg_num_reactions:
				self.confessions[i].classification = Classification.LESS
			i += 1

	def process_text(self):
		#TODO: check out re.findall or re.finditer
		# check this link: https://stackoverflow.com/questions/4697882/how-can-i-find-all-matches-to-a-regular-expression-in-python
		all_confession_data = re.findall(self.confession_obj,self.text)
		for confession_data in all_confession_data:
			confession = Confession(confession_data[0], confession_data[1], confession_data[2])

			#should actually replace newlines in between blocks with space, or else words smushed together
			no_line_break_post = confession_data[3].replace("\n\n", "")
			confession.post = re.sub(self.see_more_obj, "", no_line_break_post)

			if len(confession_data[6])%2 == 0 and len(confession_data[6]) >= 2:# returns correct num of reactions!
				reaction_num_as_list = []
				for i in range(int(len(confession_data[6])/2)):
					reaction_num_as_list.append(confession_data[6][i])
				confession.reactions = int("".join(reaction_num_as_list))
			# print(confession.reactions)


			# print("----------------")

			self.confessions.append(confession)

	def get_confessions(self):
		return self.confessions

	def get_avg_num_reactions(self):
		return self.avg_num_reactions


		
		