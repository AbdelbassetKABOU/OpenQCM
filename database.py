<<<<<<< HEAD
#


from  fastapi import FastAPI
import database as db


api = FastAPI(
                 title = 'Quiz API',
                 description='An API that interact with a DB and return a set of question',
                 version='0.1'
      )

@api.get('/hello')
async def hello():
    return {'data': 'w3laykom el Hello'}
=======


import pandas as pd
import numpy as np

df = pd.read_csv('questions.csv')



auth = {
          "alice"    : "wonderland",
          "bob"      : "builder",
         "clementine": "mandarine"
       }


def authenticate(login: str, passwd: str) -> bool:
    '''
    '''
    real_pass = auth[login]
    if real_pass :
        if real_pass == passwd : 
            return True
    return False
        #return {
        #           'response': False,
        #           'error': True
        #}
             

>>>>>>> 43cdb76ecf85cb50ae9d2e1bae643fce999987f3
