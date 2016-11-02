# noteTeX
Wouldn't it be great to put all your PDFs into a single directory and then quickly make a report out of them for easy presentation? Well now you can with noteTeX! Create a directory and move all your PDF files to this directory before either calling an instance of `noteTeX`:
```
noteTeX(directory="./",outputfilename="Analysis_Update.tex",filestoignoreList=[],keepBuildFiles=False)
```
or simply running within the folder:
```
python /address/to/noteTeX/noteTeX.py
```
