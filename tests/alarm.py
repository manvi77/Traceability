"""
This is the Alarm test
"""

from common.test import BaseTest

class AlarmTest(BaseTest):
	"""Simple alarm test
	"""

	ID = "T1"
	REQS = ["R1.1", "R2.2"]

	def hello(self):
		print "hello"


