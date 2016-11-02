# noteTeX
Wouldn't it be great to put all your PDFs into a single directory and then quickly make a report out of them for easy presentation? Well now you can with noteTeX! Create a directory and move all your PDF files to this directory before either calling an instance of `noteTeX`:
```
noteTeX(directory="./",outputfilename="Analysis_Update.tex",filestoignoreList=[],keepBuildFiles=False)
```
or simply running within the folder:
```
python /address/to/noteTeX/noteTeX.py
```

## Prerequisites
For noteTeX to work you require `latexmk` to be installed on your machine. `pickle` is used to create temporary files containing the PDF titles and captions in dictionaries

## Future Development

+ noteTeX will soon have the feature to add existing TeX files (such as tables) into the report.

+ Additional function to allow the user to attach their own captions (currently noteTeX uses the filename).
