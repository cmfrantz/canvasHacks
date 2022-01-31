# canvasHacks
Scripts to make using Canvas easier

## List of scripts
<table>
<tr><th>Script</th><th>Description</th><th>Data files used</th><th>Other requirements</th><th>Notes</th></tr>
<tr><td>Pretty4Canvas.py</td><td>Converts unformatted tagged HTML to formatted HTML for making pretty Canvas pages from large documents</td><td>One or more *.html or *.txt HTML files</td><td></td><td>Right now, it makes tabs from top-level headings, and pretties up tables. This is the stuff I find myself going crazy doing manually, so this automates it. The script is still sort of buggy, and the HTML docs produced need some cleanup either in Canvas or in a text editor.</td></tr>
</table>

## Example
<table>
	<tr>
		<td><img src="https://github.com/cmfrantz/canvasHacks/blob/main/images/Screenshot_GoogleDoc.png" height="250 px"></td>
		<td><img src="https://github.com/cmfrantz/canvasHacks/blob/main/images/Screenshot_HTML-before.png" height="250 px"></td>
		<td><img src="https://github.com/cmfrantz/canvasHacks/blob/main/images/Screenshot_cmd.png" height="250 px"></td>
	</tr>
	<tr>
		<td>A nice, formatted Google doc, a few hundred pages long, that needs to be converted to a Canvas page.</td>
		<td>The over-styled HTML produced when the doc is pasted straight into a new Canvas page. The good formatting is lost, and bad formatting is added.</td>
		<td>Pretty4Canvas to the rescue! Here it is running through the tables in one of the files and asking whether or not to format the header row.</td>
	</tr>
	<tr>
		<td colspan=3></td>
	</tr>
	<tr>
		<td><img src="https://github.com/cmfrantz/canvasHacks/blob/main/images/Screenshot_HTML-after.png" height="250 px"></td>
		<td><img src="https://github.com/cmfrantz/canvasHacks/blob/main/images/Screenshot_Canvas-after.png" height="250 px"></td>
		<td><img src="https://github.com/cmfrantz/canvasHacks/blob/main/images/Screenshot_Table-after.png" height="250 px"></td>
	</tr>
	<tr>
		<td>Cleaned up and re-formatted HTML post-processing</td>
		<td>A beautiful Canvas page! With tabs!</td>
		<td>A pretty table in university colors as displayed in Canvas. The only thing edited here after Pretty4Canvas script was applied was to add a table caption</td>
	</tr>
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
