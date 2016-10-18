import pickle
import os

preamble = "\\documentclass{article}\n\\usepackage{graphicx}\n\\usepackage{cprotect}\n\\begin{document}\n"
end = "\\end{document}"

def autoGenPDF(directory="./",exception=[]):
	for filename in os.listdir(directory):
		autocapt = "\\verb|%s|" % filename
		if filename in exception:
			print "OOPS"
			continue
		if filename.endswith(".pdf"):
			dict_ = {}
			dict_['IMAGE'] = filename
			dict_['CAPTION'] = autocapt
			pickle.dump(dict_,open(filename+".ltxobj",'w'))

def addTeXGraphic(file_,image,caption):
	file_.write("\\begin{{figure}}\n\\cprotect\\caption{{{caption}}}\n".format(caption=caption))
	file_.write("\n\\includegraphics[width=\\textwidth]{{{image}}}\n".format(image=image))
	file_.write("\\end{figure}\n")

def readPDFtoDict(directory="./"):

	dict_rep = []
	
	for filename in os.listdir(directory):

		if filename.endswith(".ltxobj"):
			x = pickle.load(open(filename,'rb'))
			assert x,"ERROR: Failed to Load File Object from %s" % filename
			dict_rep.append(x)
	return dict_rep
	
def mkreport(filename="./report",directory="./"):
	
	dict_rep = readPDFtoDict(directory)
	f = open(filename+'.tex', 'w')
	f.write(preamble)
	for element in dict_rep:
		assert element,"ERROR: Failed to Load Dictionary Item"
		addTeXGraphic(f,element['IMAGE'],element['CAPTION'])
	f.write(end)
	f.close()
	os.system("pdflatex -pdf {file_}.tex".format(file_=filename))
	os.system("rm *.aux")
	os.system("rm *.tex")
	os.system("rm *.log")
	os.system("rm *.cpt")
			
if __name__ == "__main__":
	print "Making PDF"
	autoGenPDF(exception=["Analysis_Update.pdf"])
	mkreport("./Analysis_Update","./")
