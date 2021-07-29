

#
#   /===============\
#  |   Database.py   |
#   \===============/
#
# This module is responsable for data access/management in the context of multitier 
# architecture [1]. A multitier architecture or n-tier arch is architectural pattern 
# in which presentation, application processing and data management functions are 
# separated.
# This provides a model by which developers can create flexible and reusable app. 
# By segregating an application into tiers, developers acquire the option of modifying 
# or adding a specific layer, instead of reworking the entire applicationi [1]. 
#
# In the context of this project, we are concerned by a database in forms of csv file.
# This means the requirement of a set of functions regarding download, load/reload,
# and preparation of the database. 
# Once data is here, we make use of "pandas" library, the de facto standard for 
# datascience. 
#
# As a Comming soon, we can add data models to our proposal which is quite simpler 
# using FastAPI. You find the first intuitions commented in the end of this file.
#
# AbdelbasetKABOU
#
# [1] https://en.wikipedia.org/wiki/Multitier_architecture
# -----------------------------------------------------------------


import os
import pandas as pd
import numpy as np
from pydantic import BaseModel
from typing import Optional


def export_df(df, file_name):
    if os.path.isfile(file_name):
        os.remove(file_name)
    df.to_csv(file_name)
    return True 

def prepare_dataset(file_name: str):
    df = pd.read_csv(file_name)
    if 'Unnamed: 0.1' not in df.columns : 
        return True
    else :
        df.rename(columns={'Unnamed: 0':'index'}, inplace=True)
        df.drop('Unnamed: 0.1', axis=1, inplace=True)
        export_state = export_df(df, file_name)
        return export_state

def initialise_df() -> bool:
    df = pd.read_csv('questions.csv')
    return df

def get_df():
    try:
        df
    except NameError:
        prepare_dataset('questions.csv')
        df = initialise_df()
    return df

def add_question(question: str, subject: str, use: str, correct: str,\
                 responseA: str, responseB: str, responseC: str, responseD: str) -> bool:
    df = get_df()
    new_row = {'question':question, 'subject':subject, 'use':use, 'correct':correct,\
               'responseA': responseA, 'responseB': responseB, \
               'responseC': responseC, 'responseD': responseD, 'remark':''}
    df = df.append(new_row, ignore_index=True)
    export_state = export_df(df, 'questions.csv')
    return True

def get_uses():
    df = get_df()
    return np.unique(df.use.values).tolist()

def get_subjects():
    df = pd.read_csv('questions.csv')
    return np.unique(df.subject.values).tolist()

def get_questions(use: str, subjects: list) -> list:
    df = pd.read_csv('questions.csv')

    mylist = df[(df.use == use) & 
                (df.subject.isin(subjects))
             ].question.tolist()
    return mylist

'''
class Question (BaseModel):
    question: str  
    subject: str
    correct: str 
    use: str
    responseA: str 
    responseB: str
    responseC: str
    responseD: str
    
class Request (BaseModel):
    use: str  
    subject: str
    number: Optional[int] = None 
'''
