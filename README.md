# noteTeX
Wouldn't it be great to put all your PDFs into a single directory and then quickly make a report out of them for easy presentation? Well now you can with noteTeX! Create a directory and move all your PDF files to this directory before either calling an instance of `noteTeX`:
```
noteTeX(directory="./",outputfilename="Analysis_Update.tex",captions=[],filestoignoreList=[],keepBuildFiles=False)
```
or simply running within the folder:
```
python /address/to/noteTeX/noteTeX.py
```

## Setting Captions

By default noteTeX simply takes the filename to be the caption for the attached PDF, however the user can specify captions as an argument. The ID for each element at definition is an integer starting from 0 assigned to each file when the files are ordered alphabetically. You can view the elements as a table after running the script by:
```
report = noteTeX()
report.printElements()
```

## Prerequisites
For noteTeX to work you require `latexmk` to be installed on your machine. `tabulate` is used to produce the table of elements contained, these are printed using the `printElements()` function.

## Future Development

+ noteTeX will soon have the feature to add existing TeX files (such as tables) into the report.
