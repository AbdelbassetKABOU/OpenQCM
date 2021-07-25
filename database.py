

import pandas as pd
import numpy as np



'''
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

#def get_questions(use: str, subjects: list, nbr: int) -> list:
def get_questions(use: str, subjects: list) -> list:
    '''
    '''
    df = pd.read_csv('questions.csv')
    # df[((df.use=='Test de validation') & 
    #     (df.subject=='Systèmes distribués')
    #    )].question.tolist
    mylist = df[(df.use==use) & 
                (df.subject.isin(subjects))
             ].question.tolist()
    print (' get_qcm -->')
    print (f'df[(df.use=={use}) & (df.subject.isin({subjects}))\
             ].question.tolist() get_qcm\n')

    print (mylist)
    return mylist
