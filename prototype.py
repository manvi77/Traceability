import inspect
import os

class TestLoader:
	def load(self, module_name):
		lst = module_name[module_name.rfind("."):]
		module = __import__(module_name, fromlist=[lst])	
		res = []
		for name, obj in inspect.getmembers(module):
			if "Test" in name:
				class_ = getattr(module, name)
				instance = class_()
				if instance.ID != None:
	 				res += [(name, instance.ID, instance.REQS)]
						
		return res
	
	def load_all(self, path_dir):
		res = []
		for f in os.listdir(path_dir):
			if f.endswith(".py"):
				module_name = f[:-3]
				tmp = self.load("%s.%s" % (path_dir, module_name))
				print tmp
				res += tmp
		return res

class Export:
	def __init__(self, requirements, tests, fail_tests, invalid_tests, not_tests):
		self.requirements = requirements
		self.tests = tests
		self.fail_tests = fail_tests
		self.invalid_tests = invalid_tests
		self.not_tests = not_tests
	
	
	
	def all_tests(self):
		res = []
		
		print "New tests are"
		for requirement in self.requirements:
			for test in requirement[1]:
				if not test in res:
					res += [test]
		
		for test in self.tests:
			if not test[1] in res:
				print "what is in: " + test[1]
				res += [test[1]]
			
		return res
		
	def new_requirements(self):
		res = []
		for test in self.tests:
			for test_req in test[2]:
				is_in = False
				for requirement in self.requirements:
					if requirement[0] == test_req:
						is_in = True
						break
				if not is_in:
					print "new: ", test_req
					res += [test_req]
				
		return res
		
	def new_tests(self):
		res = []
		for test in self.tests:
			is_in = False
			for requirement in self.requirements:
				for req_test in requirement[1]:
					if req_test == test[1]:
						is_in = True
						break
			if not is_in:
				res += [test[1]]
				
		return res
	
		
	def all_requirements(self):
		res = []
		print "New requirements are"
		for requirement in self.requirements:
			if not requirement[0] in res:
				res += [requirement[0]]
				
		for test in self.tests:
			for requirement in test[2]:
				if not requirement in res:
					print requirement
					res += [requirement]
		
		return res

	
	def newReq(self):
		tab = self.export()
		t2 = table(table)
		for j in range(len(tab[0])):
			for requirement in self.requirements:
				if not requirement[0] in tab:
					tab[j][0] = "New"
					tab+= [requirement[0]]
			

	def isMissingTest(self, test_name, tests):
		return False
		

	def export(self):
		atest = self.all_tests()
		areq = self.all_requirements()
		table  = [""] * len(areq)
		for i in range(len(table)):
			table[i] = [""]*len(atest)

		missing = export.computeMissing()
		for i in range(len(atest)):
			for j in range(len(areq)):
				#check for everything
				#if test[i] is missing in requirement[j] then
				#table[j][i]="missing test"	
				
				if self.check_test(areq[j], atest[i]) == "pass" :
					table[j][i] = "pass"
				elif self.check_test(areq[j], atest[i]) == "invalid" :
					table[j][i] = "blocked"
				elif self.check_test(areq[j], atest[i]) == "fail" :
					table[j][i] = "fail"
				elif self.check_test(areq[j], atest[i]) == "not run" :
					table[j][i] = "not run"
				elif (areq[j], atest[i]) in missing:
					table[j][i] = "missing"
				else:
					table[j][i] = "   "
		self.exportToFile("export.html", areq, atest, table)

	def check_test(self, req_id, test_id):
		for test in self.tests:
			if test[1] == test_id and test[1] in fail_tests:
				if req_id in test[2]:
						return "fail"
			elif test[1] == test_id and test[1] in blocked_tests:
				if req_id in test[2]:
						return "invalid"
			elif test[1] == test_id and test[1] in not_run:
				if req_id in test[2]:
						return "not run"
			elif test[1] == test_id:
				if req_id in test[2]:
						return "pass"
		return "Nothing"
		
	def missingReq(self):
		res = []
		print "self.requirements: ", self.requirements
		print "self.tests: ", self.tests
		#and not item[0] in res
		for item in self.requirements:
			present = False
			for tst in self.tests:
				if item[0] in tst[2]:
					present = True
			
			if not present:
				res += [item[0]]
					
		return res
	
	def computeMissing(self):
		res = []
		missingR = self.missingReq()
		for req in self.requirements:
			for missing in missingR:
				if req[0] == missing:
					for test in req[1]:
						res += [(req[0], test)]
		return res
		
	def exportToFile(self, filename, reqs, tests, table):
		f = open(filename, "w")
		f.write("<html>\n")
		f.write("<body>\n")	
		f.write("<table border='1'>\n")
		f.write("<tr>\n")
		f.write("<td></td>\n")
		for r in reqs:
			
			print "new requirements: ", r, self.new_requirements()
			print "------------"
			if r in self.new_requirements():
				f.write("<td>%s+</td>\n" % r)
			else:
				f.write("<td>%s</td>\n" % r)
			
		for i in range(len(tests)):
			print "new tests new:", i, self.new_tests()
			print "------------"
			f.write("<tr>\n")
			if tests[i] in self.new_tests():
				f.write("<td>%s+</td>\n" % tests[i])
			else:
				f.write("<td>%s</td>\n" % tests[i])
			for j in range(len(reqs)):
				clr = "white"
				if table[j][i] == "fail":
					clr = "pink"

				if table[j][i] == "pass":
					clr = "grey"
					
				if table[j][i] == "blocked":
					clr = "sky blue"
				
				if table[j][i] == "not run":
					clr = "yellow"
				
				
				color = "white"
				
				color = ""
				f.write("<td bgcolor=\"%s\"> %s </td>\n" % (clr, table[j][i]))


			f.write("</tr>\n")


		f.write("</tr>\n")

		f.write("</table>\n")
		f.write("</body>\n") 
		f.write("</html>\n")

		f.close()

	


requirements = [("R1.1", ["T1", "T2"]), ("R1.2", ["T3"]), ("R1.4", ["T4"]), ("R2.2", ["T1"]), ("R2.8", ["T5"]), ("R2.5", ["T4", "T5"]), ("R7", [])]

######
loader = TestLoader()
all_tests = loader.load_all("tests")

print all_tests
fail_tests = ['T2']
blocked_tests = ['T4']
not_run = ['T5']

###
export = Export(requirements, all_tests, fail_tests, blocked_tests, not_run)
print export.all_tests()
print export.all_requirements()
export.export()

export = Export(requirements, all_tests, fail_tests, blocked_tests, not_run)
print export.missingReq()
print export.new_requirements()
print export.computeMissing()

print export.new_tests()