# canvasHacks
scripts to make using Canvas easier

## List of scripts
<table>
<tr><th>Script</th><th>Description</th><th>Data files used</th><th>Other requirements</th><th>Notes</th></tr>
<tr><td>Pretty4Canvas.py</td><td>Converts unformatted tagged HTML to formatted HTML for making pretty Canvas pages from large documents</td><td>One or more *.html or *.txt HTML files</td><td></td><td>Right now, it makes tabs from top-level headings, and pretties up tables. This is the stuff I find myself going crazy doing manually, so this automates it. The script is still sort of buggy, and the HTML docs produced need some cleanup either in Canvas or in a text editor.</td></tr>
</table>

## Setting up
The code for this project requires the following list of packages in order to run.
<ul>
<li>os</li>
<li>tkinter</li>
</ul>

To install using conda, execute the command:

	conda install os
	conda install tkinter
	
...and so on

To install using pip, execute the command:

	pip install os
	pip install tkinter
	
...and so on

## Running
Once python and the packages listed above have been installed, to run a script from command line, execute the command:

	python Pretty4Canvas.py
