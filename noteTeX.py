import pickle
import os
from tabulate import tabulate
version = "v0.1.0"

preamble = "\\documentclass{article}\n\\usepackage[space]{grffile}\n\\usepackage{graphicx}\n\\usepackage{cprotect}\n\\begin{document}\n"
end = "\\end{document}\n"

class noteTeX:
	def __init__(self,directory='./',outputfile="Analysis_Update.tex",captions=[],exception_list=[],keepBuildFiles=False):
		self.directory = directory
		self.exceptions = exception_list
		self.file = open('%s' % outputfile,'wb')
		self.exceptions.append(outputfile)
		self.exceptions.append(outputfile.replace(".tex",".pdf"))
		self.elements = {}
		self.kBF = keepBuildFiles
		self.filest = outputfile
		self.captions = captions
	
	def autoGenPDF(self):
		ID = 0
		for filename in sorted(os.listdir(self.directory)):
			autocapt = "\\verb|%s|" % filename
			if filename in self.exceptions:
				print "Ignoring file %s which is an exception" % filename
				continue
			if filename.endswith(".pdf"):
				print "Adding PDF file %s to report" % filename
				dict_ = {}
				dict_['TYPE'] = "PDF"
				dict_['IMAGE'] = filename
				if len(self.captions) <= ID or self.captions[ID] == "":
					dict_['CAPTION'] = autocapt
				else:
					dict_['CAPTION'] = self.captions[ID]
				self.elements[ID] = dict_
			if filename.endswith(".tex"):
				print "Adding TeX file %s to report" % filename
				dict_= {}
				dict_['TYPE'] = "TeX"
				dict_['TeX'] = filename
				self.elements[ID] = dict_
			ID += 1
	def addTeXGraphic(self,image,caption):
		self.file.write("\\begin{{figure}}\n\\cprotect\\caption{{{caption}}}\n".format(caption=caption))
		self.file.write("\n\\includegraphics[width=\\textwidth]{{{image}}}\n".format(image=image))
		self.file.write("\\end{figure}\n")

	def addTeXFile(self,file_):
		self.file.write("\\input{{{file_}}}\n".format(file_=file_))

	def assembleReport(self):
		
		self.file.write(preamble)
		for ID in self.elements:
			assert self.elements[ID],"ERROR: Failed to Load Dictionary Item"
			if self.elements[ID]['TYPE'] == "PDF":
				self.addTeXGraphic(self.elements[ID]['IMAGE'],self.elements[ID]['CAPTION'])
			if self.elements[ID]['TYPE'] == "TeX":
				self.addTeXFile(self.elements[ID]['TeX'])
		self.file.write(end)
	
	def removeFiles(self,filename):
		files_to_delete = [".aux",".log",".cpt",".fls",".fdb_latexmk"]
		for ending in files_to_delete:
			if filename.endswith(ending):
				return True
		return False

	def printElements(self):
		table = []
		for ID in self.elements:
			if self.elements[ID]['TYPE'] == "PDF":
				key = "IMAGE"
				caption = self.elements[ID]['CAPTION']
			if self.elements[ID]['TYPE'] == "TeX":
				key = "TeX"
				caption = "N/A"
			table.append([ID,self.elements[ID][key],caption])

		print tabulate(table,headers=["ID","File","Caption"],tablefmt="fancy_grid")


	def compileLaTeX(self):
	
		build_command = "latexmk -pdf {file_}".format(file_=self.filest)
		print "Running LaTeX compiler as: %s" % build_command
		os.system(build_command)
	
	def build(self):
		print "WELCOME TO NOTETEX %s\n--------------------------\n" % version			
		self.autoGenPDF()
		print "Building Report......"
		self.assembleReport()
		self.file.close()
		print "\n--------------------------\n--------------------------\n\n"
		self.compileLaTeX()
		build_success = False
		for filename in os.listdir(self.directory):	
			if not self.kBF and self.removeFiles(filename):
				os.system("rm %s" % filename)
			if filename == self.filest:
				print "Build Success!\n"
				build_success = True
		if build_success == False:
			print "Build Failed"
			return

if __name__ == "__main__":

	report = noteTeX()
	report.build()
	report.printElements()
