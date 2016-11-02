import pickle
import os

version = "v0.1.0"

preamble = "\\documentclass{article}\n\\usepackage{graphicx}\n\\usepackage{cprotect}\n\\begin{document}\n"
end = "\\end{document}\n"

class noteTeX:
	def __init__(self,directory='./',outputfile="Analysis_Update.tex",exception_list=[],keepBuildFiles=False):
		self.directory = directory
		self.exceptions = exception_list
		self.file = open('%s' % outputfile,'wb')
		self.exceptions.append(outputfile)
		self.kBF = keepBuildFiles
		self.filest = outputfile
	
	def autoGenPDF(self):
		for filename in os.listdir(self.directory):
			autocapt = "\\verb|%s|" % filename
			if filename in self.exceptions:
				print "Ignoring file %s which is an exception" % filename
				continue
			if filename.endswith(".pdf"):
				print "Adding file %s to report" % filename
				dict_ = {}
				dict_['IMAGE'] = filename
				dict_['CAPTION'] = autocapt
				pickle.dump(dict_,open(filename.replace('.pdf','')+".ltxobj",'w'))

	def addTeXGraphic(self,image,caption):
		self.file.write("\\begin{{figure}}\n\\cprotect\\caption{{{caption}}}\n".format(caption=caption))
		self.file.write("\n\\includegraphics[width=\\textwidth]{{{image}}}\n".format(image=image))
		self.file.write("\\end{figure}\n")

#	def addTeXFile(self):

	def readPDFtoDict(self):

		dict_rep = []
	
		for filename in os.listdir(self.directory):

			if filename.endswith(".ltxobj"):
				x = pickle.load(open(filename,'rb'))
				assert x,"ERROR: Failed to Load File Object from %s" % filename
				dict_rep.append(x)
		return dict_rep

	def assembleReport(self):
		
		dict_rep = self.readPDFtoDict()
		self.file.write(preamble)
		for element in dict_rep:
			assert element,"ERROR: Failed to Load Dictionary Item"
			self.addTeXGraphic(element['IMAGE'],element['CAPTION'])
		self.file.write(end)
	
	def removeFiles(self,filename):
		files_to_delete = [".aux",".ltxobj",".log",".cpt",".fls",".fdb_latexmk"]
		for ending in files_to_delete:
			if filename.endswith(ending):
				return True
		return False

	def build(self):
		print "WELCOME TO NOTETEX %s\n--------------------------\n" % version			
		self.autoGenPDF()
		print "Building Report......"
		self.assembleReport()
		self.file.close()
		build_command = "latexmk -pdf {file_}".format(file_=self.filest)
		print "Running LaTeX compiler as: %s" % build_command
		print "\n--------------------------\n--------------------------\n\n"
		os.system(build_command)
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
