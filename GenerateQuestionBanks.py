# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 17:05:59 2023

@author: cariefrantz

This script takes a spreadsheet containing questions (or pieces of questions)
and answers and formats them for Respondus. This was built in order to quickly
generate large question banks containing HTML (embed) code,
but could be repurposed for other types of questions.

"""

####################
# IMPORTS
####################
import os
import pandas as pd
from tkinter import *
from tkinter import filedialog


####################
# VARIABLES
####################
Respondus_columns=[
    'Type', 'Title/ID', 'Points', 'Question Wording', 'Correct Answer', 
    'Choice 1', 'Choice 2', 'Choice 3', 'Choice 4', 'Choice 5',
    'Choice 6', 'Choice 7', 'Choice 8', 'Choice 9', 'Choice 10',
    'General Feedback', 'Correct Feedback', 'Incorrect Feedback',
    'Feedback 1', 'Feedback 2', 'Feedback 3', 'Feedback 4', 'Feedback 5',
    'Feedback 6', 'Feedback 7', 'Feedback 8', 'Feedback 9', 'Feedback 10',
    'Topic', 'Difficulty Level', 'Meta 1', 'Meta 2', 'Meta 3', 'Meta 4']
Respondus_table = pd.DataFrame(columns=Respondus_columns)
MC_letters = ['a','b','c','d','e','f','g','h','i','j']

# These are the available types of question banks that this code supports.
#   Each value in the list corresponds with a script (def) below.
BankTypes = [
    'RockOrMineral3D',
    'RockCycleClassification3D',
    'Igneous Classification3D'
    ]


####################
# GENERAL SCRIPTS
####################
def getInputTable(title):
    '''
    Loads the spreadsheet used as the input table.

    Parameters
    ----------
    title : str
        Title for the file selection user interface.

    Returns
    -------
    input_table : pandas.DataFrame
        The loaded table.
    dirPath : str
        Directory where the table was found. The Respondus table will be 
        saved to the same directory.

    '''
    # Open user input file dialog to pick file
    root=Tk()
    filename=filedialog.askopenfilename(
        initialdir=os.getcwd(), title = title,
        filetypes = [('CSV', '*.csv')])
    dirPath = os.path.dirname(filename)     # Directory
    root.destroy()
    
    # Read in the table
    input_table = pd.read_csv(filename)
    
    return input_table, dirPath


def build_MC_bank(Respondus_table, fpath):
    '''    
    Generates a Respondus-formatted text file from a table containing
    Respondus variables.

    Parameters
    ----------
    Respondus_table : pandas.DataFrame
        A Respondus-formatted table for all of the questions to format to a
        text file
        
    fpath : str
        Filepath to save the text file to

    Returns
    -------
    None.

    '''
    text = ''
    
    # Loop through each question in the question table and format
    for i in range(len(Respondus_table)):
        
        # Question text
        question = Respondus_table.loc[i].copy()
        q_text = (
            'Points: ' + str(question['Points']) + '\n\n'
            'Title: ' + question['Title/ID'] + '\n' +
            str(i+1) + ') ' + question['Question Wording'] + '\n\n')
        
        # Feedback text
        # General feedback
        #   Note: Due to quirks with Respondus, there is no general feedback
        #           allowed in multiple choice questions.
        #           If general feedback is present in the table, it will be
        #           overwritten by any Correct and Incorrect Feedback.
        feedback = {
            'correct'   : '',
            'incorrect' : ''
            }
        if str(question['General Feedback']) != 'nan':
            feedback['correct']     = question['General Feedback']
            feedback['incorrect']   = question['General Feedback']
        if str(question['Correct Feedback']) != 'nan':
            feedback['correct']     = question['Correct Feedback']
        if str(question['Incorrect Feedback']) != 'nan':
            feedback['incorrect']   = question['Incorrect Feedback']
        # Write the feedback
        if feedback['correct']:
                q_text = q_text + '~ ' + feedback['correct'] + '\n'
        if feedback['incorrect']:
                q_text = q_text + '@ ' + feedback['incorrect'] + '\n'
        if any(feedback.values()):
            q_text = q_text + '\n'
            
        # Possible answer text
        answers = [x for x in question[['Choice 1', 'Choice 2', 'Choice 3',
                                        'Choice 4', 'Choice 5', 'Choice 6',
                                        'Choice 7', 'Choice 8', 'Choice 9',
                                        'Choice 10']] if str(x) != 'nan']
        for n, answer in enumerate(answers):
            # Generic answer text
            ans_text = MC_letters[n] + ') ' + answer + '\n'
            # Add a * for correct answers
            if n+1 == question['Correct Answer']:
                q_text = q_text + '*' + ans_text
            # Don't for incorrect answers
            else:
                q_text = q_text + ans_text
                
        text = text + q_text + '\n'
    
    # Save text to a text file
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(text)
        f.close()
        

####################
# QUESTION BANK SCRIPTS
####################

def format_RockOrMineral3D():
    '''
    Formats a Respondus-formatted text file
    for a "Rock or mineral?" question set that uses interactive 3D rock models.
    
    Copy and modify this def to create new question bank types.
    
    This example imports a spreadsheet with the columns
        'Type' (type of rock that students need to identify)
        'Difficulty' (difficulty of the identification, which is used in this
                      script to trim the question set to just questions with
                      a designated difficulty level)
        'Embed' (the HTML embed code containing the 3D rock model that students
                 will identify)
        'Description' (text that forms the general feedback for the question)
        
    It then generates Respondus-formatted multiple choice questions that test
    students' ability to identify the rocks they are shown.
    '''
    # Get input table
    input_table, dirPath = getInputTable(
        'Select rock and mineral 3D model list for the question bank (CSV)')
    
    # Have user select the difficulty from the difficulty list present in
    #   the input table
    diff_levels = ', '.join(list(set(input_table['Difficulty'])))
    difficulty = input(
        'Select the difficulty level for the question bank. Options are:  '
        + 'all, ' + diff_levels + '\n')
    
    # Trim the table based on the difficulty level
    in_table = input_table.copy()
    if difficulty == 'easy':
        in_table = in_table[in_table['Difficulty']=='easy']
    elif difficulty == 'moderate':
        in_table = in_table[in_table['Difficulty']=='moderate']
    in_table = in_table.reset_index(drop=True)
    
    # Fill in Respondus table
    # Type of question
    Respondus_table['Type'] = ['MC'] * len(in_table)
    # Question title
    Respondus_table['Title/ID'] = (
        ['Rock or mineral? Level ' + difficulty] * len(in_table))
    # Number of points per question
    Respondus_table['Points'] = [1] * len(in_table)
    # Wording of the question
    Respondus_table['Question Wording'] = (
        "[HTML]<p>Is this a rock or a mineral?</p>"
        + in_table['Embed'] + '[/HTML]')
    # Multiple choice possible answers
    Respondus_table['Choice 1'] = ['rock'] * len(in_table)
    Respondus_table['Choice 2'] = ['mineral'] * len(in_table)
    # Feedback
    Respondus_table['General Feedback'] = in_table['Description']
    
    # Generate correct answers from values in the input table
    answers = in_table['Type'].values
    for i in range(len(answers)):
        if answers[i]=='mineral':
            answers[i] = 2
        else:
            answers[i] = 1
    Respondus_table['Correct Answer'] = answers
    
    # Save the Respondus table file
    fname = 'Respondus_RockOrMineral'    
    Respondus_table.to_csv(dirPath + '/' + fname + '.csv',
                           index=False)
    print('Generated RockOrMineral question bank and saved it to ' + 
          dirPath + '/' + fname + '.csv')
    
    # Build and save the Respondus text file
    build_MC_bank(Respondus_table, dirPath + '/' + fname + '.txt')
    print(' and ' + fname + '.txt')
    
    return Respondus_table


def format_RockCycleClassification3D():
    '''
    Formats a Respondus-formatted text file
    for a rock cycle classification question set that uses
    interactive 3D rock models.
    
    This example imports a spreadsheet with the columns
        'Type' (type of rock that students need to identify)
        'Difficulty' (difficulty of the identification, which is used in this
                      script to trim the question set to just questions with
                      a designated difficulty level)
        'Embed' (the HTML embed code containing the 3D rock model that students
                 will identify)
        'Description' (text that forms the general feedback for the question)
        
    It then generates Respondus-formatted multiple choice questions that test
    students' ability to classify the rocks they are shown as being
    sedimentary, extrusive igneous, intrusive igneous, metamorphic, or mineral.
    '''
    # Get input table
    input_table, dirPath = getInputTable(
        'Select rock and mineral 3D model list for the question bank (CSV)')
    
    # Have user select the difficulty from the difficulty list present in
    #   the input table
    diff_levels = ', '.join(list(set(input_table['Difficulty'])))
    difficulty = input(
        'Select the difficulty level for the question bank. Options are:  '
        + 'all, ' + diff_levels + '\n')
    
    # Trim the table based on the difficulty level
    in_table = input_table.copy()
    if difficulty == 'easy':
        in_table = in_table[in_table['Difficulty']=='easy']
    elif difficulty == 'moderate':
        in_table = in_table[in_table['Difficulty']=='moderate']
    in_table = in_table.reset_index(drop=True)
    
    # Fill in Respondus table
    # Type of question
    Respondus_table['Type'] = ['MC'] * len(in_table)
    # Question title
    Respondus_table['Title/ID'] = (
        ['Rock Cycle Rock Classification Level ' + difficulty] * len(in_table))
    # Number of points per question
    Respondus_table['Points'] = [1] * len(in_table)
    # Wording of the question
    Respondus_table['Question Wording'] = (
        "[HTML]<p>What kind of rock is this?</p>"
        + in_table['Embed'] + '[/HTML]')
    # Multiple choice possible answers
    Respondus_table['Choice 1'] = ['mineral'] * len(in_table)
    Respondus_table['Choice 2'] = ['sedimentary'] * len(in_table)
    Respondus_table['Choice 3'] = ['extrusive igenous'] * len(in_table)
    Respondus_table['Choice 4'] = ['intrusive igenous'] * len(in_table)
    Respondus_table['Choice 5'] = ['metamorphic'] * len(in_table)
    # Feedback
    Respondus_table['General Feedback'] = in_table['Description']
    
    # Generate correct answers from values in the input table
    answers = in_table['Type'].values
    for i in range(len(answers)):
        if answers[i]=='mineral':
            answers[i] = 1
        if answers[i]=='sedimentary rock':
            answers[i] = 2
        if answers[i]=='extrusive igneous':
            answers[i] = 3
        if answers[i]=='intrusive igneous':
            answers[i] = 4
        if answers[i]=='metamorphic':
            answers[i] = 5
    Respondus_table['Correct Answer'] = answers
    
    # Save the Respondus table file
    fname = 'Respondus_RockCycleClassification'    
    Respondus_table.to_csv(dirPath + '/' + fname + '.csv',
                           index=False)
    print('Generated RockCycleClassification question bank and saved it to ' + 
          dirPath + '/' + fname + '.csv')
    
    # Build and save the Respondus text file
    build_MC_bank(Respondus_table, dirPath + '/' + fname + '.txt')
    print(' and ' + fname + '.txt')
    
    return Respondus_table


def format_IgneousClassification3D():
    '''
    Formats a Respondus-formatted text file
    for an igneous rock classification question set that uses
    interactive 3D rock models.
    
    This example imports a spreadsheet with the columns
        'Type' (type of rock that students need to identify)
        'Felsic-Mafic' (whether the rock composition is felsic, mafic, or 
                        intermediate)
        'Difficulty' (difficulty of the identification, which is used in this
                      script to trim the question set to just questions with
                      a designated difficulty level)
        'Embed' (the HTML embed code containing the 3D rock model that students
                 will identify)
        'Description' (text that forms the general feedback for the question)
        
    It then generates Respondus-formatted multiple choice questions that test
    students' ability to classify the igneous rocks they are shown as being
    extrusive or intrusive and felsic, intermediate, or mafic.
    '''
    # Get input table
    input_table, dirPath = getInputTable(
        'Select rock and mineral 3D model list for the question bank (CSV)')
    
    # Have user select the difficulty from the difficulty list present in
    #   the input table
    diff_levels = ', '.join(list(set(input_table['Difficulty'])))
    difficulty = input(
        'Select the difficulty level for the question bank. Options are:  '
        + 'all, ' + diff_levels + '\n')
    
    # Trim the table to igneous rocks only
    in_table = input_table.copy()
    in_table = in_table[in_table['Type'].str.contains('igneous')==True]
    
    # Trim the table based on the difficulty level
    if difficulty == 'easy':
        in_table = in_table[in_table['Difficulty']=='easy']
    elif difficulty == 'moderate':
        in_table = in_table[in_table['Difficulty']=='moderate']
    in_table = in_table.reset_index(drop=True)
    
    # Fill in Respondus table
    # Type of question
    Respondus_table['Type'] = ['MC'] * len(in_table)
    # Question title
    Respondus_table['Title/ID'] = (
        ['Igneous Rock Classification Level ' + difficulty] * len(in_table))
    # Number of points per question
    Respondus_table['Points'] = [1] * len(in_table)
    # Wording of the question
    Respondus_table['Question Wording'] = (
        "[HTML]<p>How did this rock form?</p>"
        + in_table['Embed'] + '[/HTML]')
    
    # Multiple choice possible answers
    answer_set = {
        'extrusive igneous felsic'          :  {
            'choice'        : 1,
            'type'          : 'extrusive igneous',
            'composition'   : 'felsic',
            'formation'     : ('Formed during an eruption ' + 
                               '(extrusive igneous) of felsic lava')
            },
        'extrusive igneous intermediate'    :  {
            'choice'        : 2,
            'type'          : 'extrusive igneous',
            'composition'   : 'intermediate',
            'formation'     : ('Formed during an eruption ' + 
                               '(extrusive igneous) of lava ' +
                               'of intermediate composition')
            },
        'extrusive igneous mafic'           :  {
            'choice'        : 3,
            'type'          : 'extrusive igneous',
            'composition'   : 'mafic',
            'formation'     : ('Formed during an eruption ' + 
                               '(extrusive igneous) of mafic lava')
            },
        'intrusive igneous felsic'          :  {
            'choice'        : 4,
            'type'          : 'intrusive igneous',
            'composition'   : 'felsic',
            'formation'     : ('Felsic magma cooled slowly inside the Earth')
            },
        'intrusive igneous intermediate'    :  {
            'choice'        : 5,
            'type'          : 'intrusive igneous',
            'composition'   : 'intermediate',
            'formation'     : ('Intermediate composition magma ' +
                               ' cooled slowly inside the Earth')
            },
        'intrusive igneous mafic'           :  {
            'choice'        : 6,
            'type'          : 'intrusive igneous',
            'composition'   : 'mafic',
            'formation'     : ('Mafic magma cooled slowly inside the Earth')
            }
        }
    for ans in answer_set:
        Respondus_table['Choice ' + str(answer_set[ans]['choice'])] = (
            answer_set[ans]['formation']
            )

    # Feedback
    Respondus_table['General Feedback'] = in_table['Description'].values
    
    # Generate correct answers from values in the input table
    for i in in_table.index:
        ans = in_table.loc[i]['Type'] + ' ' + in_table.loc[i]['Felsic-Mafic']
        Respondus_table.at[i,'Correct Answer'] = answer_set[ans]['choice']
    
    # Save the Respondus table file
    fname = 'Respondus_IgneousClassification'    
    Respondus_table.to_csv(dirPath + '/' + fname + '.csv',
                           index=False)
    print('Generated IgneousClassification question bank and saved it to ' + 
          dirPath + '/' + fname + '.csv')
    
    # Build and save the Respondus text file
    build_MC_bank(Respondus_table, dirPath + '/' + fname + '.txt')
    print(' and ' + fname + '.txt')
    
    return Respondus_table
#%%
####################
# MAIN FUNCTION
####################
if __name__ == '__main__':
    bank_type = input(
        'What type of question bank do you want to generate? Options are: ' +
        ', '.join(BankTypes) + '\n')
    
    Respondus_table = globals()['format_'+ bank_type]()

