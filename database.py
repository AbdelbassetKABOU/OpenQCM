from  fastapi import FastAPI
import database as db
import os


api = FastAPI(
                 title = 'Quiz API',
                 description='An API that interact with a DB and return a set of question',
                 version='0.1'
      )

#@api.get('/hello')
#async def hello():
#    return {'data': 'w3laykom el Hello'}


import pandas as pd
import numpy as np

'''
    question: l'intitulé de la question
    subject: la catégorie de la question
    correct: la liste des réponses correctes
    use: le type de QCM pour lequel cette question est utilisée
    responseA: réponse A
    responseB: réponse B
    responseC: réponse C
    responseD: la réponse D (si elle existe)

In [18]: df.use.value_counts()
Test de validation        40
Test de positionnement    21
Total Bootcamp            15
Name: use, dtype: int64

In [19]: df.subject.value_counts()
Systèmes distribués     16
Streaming de données    13
Automation              10
Classification          10
Data Science             8
Machine Learning         7
BDD                      6
Docker                   5
Sytèmes distribués       1
Name: subject, dtype: int64
'''

from pydantic import BaseModel
from typing import Optional

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

#def get_database():
    #wget https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv
    #    import requests
    #    print('Beginning file download with requests')
    #    url = 'http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg'
    #    r = requests.get(url)
    #    with open('/Users/scott/Downloads/cat3.jpg', 'wb') as f:
    #        f.write(r.content)
    #    # Retrieve HTTP meta-data
    #    print(r.status_code)
    #    print(r.headers['content-type'])
    #    print(r.encoding)

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

    #if os.path.isfile('./questions.csv'):
    #    os.remove('./questions.csv')
    #df.to_csv('questions.csv')
    #df.to_csv('questions.csv')

    return True


def get_uses():
    df = get_df()
    return np.unique(df.use.values).tolist()

def get_subjects():
    df = pd.read_csv('questions.csv')
    return np.unique(df.subject.values).tolist()

def get_questions(use: str, subjects: list) -> list:
    '''
    '''
    df = pd.read_csv('questions.csv')

    print (' get_qcm -->')
    print (f'df[(df.use=={use}) & (df.subject.isin({subjects}))\
             ].question.tolist() get_qcm\n')

    # df[((df.use=='Test de validation') & 
    #     (df.subject=='Systèmes distribués')
    #    )].question.tolist
    #mylist = df[(df.use.isin(use)) & 
    mylist = df[(df.use == use) & 
                (df.subject.isin(subjects))
             ].question.tolist()
    print (' get_qcm -->')
    print (f'df[(df.use=={use}) & (df.subject.isin({subjects}))\
             ].question.tolist() get_qcm\n')
    print (mylist)
    return mylist
