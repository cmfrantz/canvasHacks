#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Carie Frantz'
__email__ = 'cariefrantz@weber.edu'
"""Pretty4Canvas
Created on Sat Jan 15 09:18:31 2022
@author: cariefrantz
@project: Teaching

Converts formatted Google Docs to pretty Canvas pages... sort of
This is still somewhat buggy

Arguments:  None

Example in command line:
    python Pretty4Canvas.py

Dependencies Install:
    sudo apt-get install python3-pip python3-dev
    pip install os
    pip install tkinter

Copyright (C) 2022  Carie M. Frantz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
Created on

@author: cariefrantz
"""

'''
First steps:
    1. Create file text in Google Docs.
        Format text headers as such using the built-in paragraph styles
        The first row of each table is considered the table header
        Subsequent rows that span columns are considered subheaders
    2. Select everything (Ctrl+A), and paste it into a fresh Canvas page.
    3. Using Canvas's HTML editor, grab the Canvas page html,
        then copy it into a text file, and save the text file (UTF-8 encoding)
    4. Alternately, you can export the Google Docs file to HTML directly,
        but I had bad luck losing a lot of formatting when I tried this.
        Try https://www.gdoctohtml.com/), save the file.
    5. Run this script.
        You can select multiple files, and it will process all of them.
        The interface will ask you about tables and whether you want to
        format them or not. If the table is for page structure,
        not for display, choose N. If the table has a first row with headers,
        choose Y.
    6. Open the file generated (the raw filename + _prettified.txt).
        Select everything (Ctrl+A), and paste it into a blank HTML editor
        for a Canvas page. Save the page.
    7. Edit the HTML or Canvas file as needed. There will likely be errors
        because this script is still kind of buggy.
        But it hopefully saves a lot of manual coding work and Canvas
        formatting frustration! :)
    
'''


####################
# IMPORTS
####################
import os
from tkinter import *
from tkinter import filedialog



####################
# FORMATTING VARIABLES
####################

# Delimiting code for identifiying features to format
delim_h1_title = ". "  # For example, header 1 is "A. Biography"

# Table formatting - Edit these to change preferences
fmt_table_head_color_bg = "#4b4945"
fmt_table_head_color_text = "#ffffff"
fmt_table_subhead_color_bg = "#a391b1"
fmt_table_subehad_color_text = "#000000"
# fmt_table_border = 1 # Canvas overwrites table borders
      

####################
# VARIABLES
####################
# Formatting code
tab_html_head = '''
<div class="enhanceable_content tabs">
  
<ul>
'''
tab_html_prefix = '  <li><a href="#tab-'



####################
# SCRIPTS
####################

## IMPORTS
def select_files():
    # Select raw HTML files from directory (UI)
    root = Tk()
    fileList = filedialog.askopenfilenames(
        initialdir=os.getcwd(),
        filetypes=[('HTML','*.html'),('Text','*.txt')],
        title = 'Select raw HTML files')
    root.destroy()
    dirPath=os.path.dirname(fileList[0])
    return fileList, dirPath


def read_file(filepath):
    # Read in the text
    with open(file, encoding="utf8") as f:
        lines=f.readlines()
    return lines



## FILE PARSING

def find_header(html, level):
    heads = [x for x in lines if "<h" + str(level) + ">" in x]
    return heads

    
def parse_header(header, delim=delim_h1_title):
    if delim in header:        
        listval = header[0:header.index(delim)]
        title = header[len(listval)+len(delim):]
    else:
        listval = header
        title = header
    return listval, title



## HTML GENERATION
   
def find_between(text, delim1, delim2):
    try:
        start = text.index(delim1) + len(delim1)
        end = text.index(delim2, start )
        return text[start:end]
    except ValueError:
        return ""
    

def create_tabs(headers):
    # Create a list of tabs
    tablist = []
    for h in headers:
        header = find_between(h,"<h2>","</h2>")
        listval, title = parse_header(header)
        tablist.append(listval)
    
    # Build the HTML
    html = '''
<div class="enhanceable_content tabs">
  
  <ul>
'''
    for tab in tablist:
        html = html + '''
    <li><a href="#tab-''' + tab + '">' + tab + '</a></li>'
    html = html + '''
  </ul>
'''
    return tablist, html


def create_content(html_orig, headlist, tablist):
    content_html=''
    for i  in list(range(len(headlist))):
        index1 = html_orig.index(headlist[i])
        if i == len(headlist)-1: index2 = len(html_orig)-1
        else: index2 = html_orig.index(headlist[i+1])
        content_html = content_html+'''
  <div id = "tab-''' + tablist[i] + '''">
'''
        for line in html_orig[index1:index2]:
            content_html = content_html + '    ' + line
        content_html = content_html + '''
  </div>
'''
    return content_html



## STYLING - WHOLE DOCUMENT
            
def increase_hlevel(html):
    # Find and increase all of the headers in the html
    delims = ['<h','</h']
    for n in list(range(8,0,-1)):
        for delim in delims:
            html = [
                s.replace(delim+str(n)+">",delim+str(n+1)+">") for s in html]
    return html
    

def gen_styling(
        text_color='', background_color='', text_align='', vert_align=''):
    if text_color:
        text_color = 'color:' + text_color
    if background_color:
        background_color = 'background-color:' + background_color
    if text_align:
        text_align = 'text-align:' + text_align
    if vert_align:
        vert_align = 'vertical-align:' + vert_align
    parameter_list = [text_color,background_color,text_align,vert_align]
    if any(parameter_list):
        style_text = ' style="' + '; '.join(parameter_list) + ';"'
    else: style_text = ''
    return style_text


def body_formatting(html, fmt_map):
    # do stuff
    return html


# STYLING - TABLES
def format_tables(html):
    # Generate styling
    th_styling = gen_styling(
        text_color = fmt_table_head_color_text,
        background_color = fmt_table_head_color_bg, text_align='left',
        vert_align='top')
    td_s_styling = gen_styling(
        text_color = fmt_table_subehad_color_text,
        background_color = fmt_table_subhead_color_bg)
    
    # Loop through and look for tables
    table_starts, table_ends = find_sections(html, 'table')
    
    # Format each table
    for table, start in enumerate(table_starts):
        table_lines = html[start:table_ends[table]+1].copy()
        
        # Format the table
        table_lines = [
            x.replace(
                '<table>',
                '<table style="border-collapse: collapse; width: 100%; '
                + 'border-color: black; border-style: solid;">')
            for x in table_lines]
        table_lines = delete_tags(table_lines, ['p'])
        table_lines = format_td(table_lines)

        # Format table heads
        table_lines = format_table_heads(table_lines, th_styling, td_s_styling)
        
        # Format all cells
        table_lines = [
            x.replace('<td>','<td style="vertical-align: top">')
            for x in table_lines]
        
        # Remove old table HTML
        html=html[0:start] + table_lines + html[table_ends[table]+1:]
        
        
        table_starts, table_ends = find_sections(html, 'table')
       
    return html

def format_table_heads(table_html, th_styling, td_s_styling):
    # Get row starts
    row_starts, row_ends = find_sections(table_html, 'tr')
    
    # If there is no existing header row, make it the first row
    if not find_indices(table_html, '<thead>'):
         # Ask the user if the first row should be formatted
         firstrowtext = ' | '.join(table_html[row_starts[0]:row_ends[0]])
         questiontext = '''Format the first row in the table below as a header?
''' + firstrowtext + '''
Enter Y or N.  > '''         
         # If yes, format it
         if input(questiontext) in ['Y','y']:
             table_html = format_th(table_html, row_starts, row_ends)
    
    # Format any th
    table_html = [
            x.replace('<th>','<th' + th_styling + '>') for x in table_html]
    
    # Identify and format any subheader rows
    row_starts, row_ends = find_sections(table_html, 'tr')
    table_html = format_subhead(table_html, row_starts, row_ends, td_s_styling)
                    
    return table_html


def format_th(table_html, row_starts, row_ends):
    # Define the first row as the header row
    table_html.insert(row_starts[0],"<thead" + ">")
    table_html.insert(row_ends[0]+2,"</thead>")
    ctr = 3
    # In the header row, replace all td with formatted th in the header row
    table_html[row_starts[0]:row_ends[0]+ctr] = [
        x.replace('<td>','<th>').replace('</td>','</th>') for x in
        table_html[row_starts[0]:row_ends[0]+ctr]]
    # Move tbody
    # Delete existing tbody
    tbody = find_indices(table_html, '<tbody>')
    if tbody:                    
        table_html.pop(tbody[0])
        ctr=ctr-1
    else:
        table_html.insert(row_ends[-1]+ctr,"</tbody>")
    # Add in tbody to the end
    table_html.insert(row_ends[0]+ctr,"<tbody>")
    
    # Return
    return table_html


def format_subhead(table_html, row_starts, row_ends, td_s_styling):
    for j, row in enumerate(row_starts):
        # If the first line indicates a subheader, format it
        if '<td colspan=' in table_html[row+1]:
            row_html = table_html[row:row_ends[j]+1]
            td_starts, td_ends = find_sections(row_html, 'td', flex=True)
            for k, td in enumerate(td_starts):
                td_pieces = row_html[td].split('>')
                row_html[td] = td_pieces[0] + ' ' + td_s_styling + '>' + td_pieces[1]
            table_html[row:row_ends[j]+1] = row_html
    return table_html


def format_td(table_html):
    td_starts, td_ends = find_sections(table_html, 'td')
    th_starts, th_ends = find_sections(table_html, 'th')
    
    for i, start in enumerate(td_starts):
        # If there is more than one line, line break all but the last
        if td_ends[i]-start > 1:
            lines = [x.replace('\n','<br />\n') for x in table_html[start+1:td_ends[i]-1]]
            table_html[start+1:td_ends[i]-1] = lines
    return table_html


## FIND & REPLACE

def find_sections(html, tag, flex=False):
    if flex: end = ''
    else: end = '>'
    starts = find_indices(html, '<' + tag + end)
    ends = find_indices(html, '</' + tag)
    return starts, ends


def find_indices(str_list, search_str):
    indices = []
    for i, string in enumerate(str_list):
        if search_str in string:
            indices.append(i)
    return indices


def delete_tags(html, tags, flex=False):
    for tag in tags:
        if flex:
            # Search for the tag in any rows
            tag_starts, tag_ends = find_sections(html, tag, flex=True)
            rows = list(set(tag_starts + tag_ends))
            for row in rows:
                row_text = html[row]
                # Split up all tags
                splits = row_text.split('<' + tag)                    
                clean_text=splits[0]
                for s in splits[1:]:
                    junk, s = s.split('>',1)
                    clean_text = clean_text + s.replace('</' + tag + '>','')
                html[row] = clean_text
        else:
            html = [x.replace('<' + tag + '>','') for x in html]
            html = [x.replace('</' + tag + '>', '') for x in html]
    return html

#%%
####################
# MAIN FUNCTION
####################
if __name__ == '__main__': 
    
    # Select files (UI)
    fileList, dirPath = select_files()
    
    # Read in and parse files
    for file in fileList:
        print('Processing ' + file)
        
        # Read in the file
        lines = read_file(file)
        
        # Clean up the formatting
        # Incerase the header levels to account for Canvas formatting
        html = increase_hlevel(lines)
        # Delete any spans
        html = delete_tags(html,['span'],flex=True)
        
        # Format tables
        html = format_tables(html)
        
        # Find the top level headers
        headers = [x for x in html if "<h2>" in x]
        
        # Build the tabs
        tablist, tab_html = create_tabs(headers)
        
        # Build the content
        content_html = create_content(html, headers, tablist)

        # More formatting
        content_html = body_formatting(content_html, fmt_map)
        
        # Finish HTML
        html_text = tab_html + content_html + '''
</div>
'''       
        
        
        # Save the HTML
        with open(file.split('.')[0]+'_prettified.txt','wb') as f:
            f.write(html_text.encode('utf-8'))
            
