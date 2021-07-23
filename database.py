

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
             

