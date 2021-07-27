#


'''
  /----------------------/
 /   #  Description     /
/----------------------/

      o L'utilisateur doit pouvoir choisir un type de test (use) ainsi qu'une ou plusieurs 
        catégories (subject). 
      o L'application peut produire des QCMs de 5, 10 ou 20 questions. 
      o L'API doit donc être en mesure de retourner ce nombre de questions. 
      o Les questions doivent être retournées dans un ordre aléatoire: ainsi, une requête 
        avec les mêmes paramètres pourra retourner des questions différentes.

      o Les utilisateurs devant avoir créé un compte, il faut que nous soyons en mesure de 
        vérifier leurs identifiants. Pour l'instant l'API utilise une authentification basique, 
        à base de nom d'utilisateur et de mot de passe: la chaîne de caractères contenant 
        Basic username:password devra être passée dans l'en-tête Authorization (en théorie, 
        cette chaîne de caractère devrait être encodée mais pour simplifier l'exercice, 
        on peut choisir de ne pas l'encoder)


      o L'API devra aussi implémenter un point de terminaison pour vérifier que l'API est bien 
        fonctionnelle. 
      o Une autre fonctionnalité doit pouvoir permettre à un utilisateur admin dont le mot 
        de passe est 4dm1N de <<créer>> une nouvelle question.

  /------------------/
 /   # ToDo List :  /
/------------------/

     -> Authentification sys
     -> 
        Base Model, 

'''

from  fastapi import FastAPI, Depends, Query, HTTPException, status
from typing import List, Optional
import database as db
import authentification as auth
import qcm

# -------------
api = FastAPI(
                 title = 'Quiz API',
                 description='An API that interact with a DB and return a set of question',
                 version='0.1'
      )
# --------------------------------------------------------------------------------------------

var = "Hola"

# ----------------
@api.get('/hello')
async def hello(username: str = Depends(auth.get_current_username)):
    return {
               'data': 'w3laykom el Hello',
               'user': username
    }
# ------------------------------------------



# ----------------
@api.get('/status')
async def status():
    return {
               'status': 1
    }
# ------------------------------------------



# -------------------
@api.get("/users/me")
#def authenticate_user(credentials: HTTPBasicCredentials = Depends(get_current_username)):
async def authenticate_user(username: str = Depends(auth.get_current_username)):
    return {
                "username": username,
                #"username": credentials.username,
                #"password": credentials.password
    }
# ----------------------------------------------------------------------------------------




# -------------------
@api.get("/subjects")
async def get_subjects():
    available_subjects = db.get_subjects()
    return available_subjects
# TO BE CONTINUED
# ---------------------



# -------------------
@api.get("/uses")
async def get_uses():
    available_uses = db.get_uses()
    return available_uses
# TO BE CONTINUED
# ---------------------

#@api.get("/questions/subjects")
#async def read_subjects(subjects: Optional[List[str]] = Query(None)):
#    query_subjects = {"subjects": subjects}
#    return query_subjects



# More details on
# https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#query-parameter-list-multiple-values-with-defaults
# Python fastapi.Query() Examples -->
# https://www.programcreek.com/python/example/113514/fastapi.Query
@api.get("/qcm/")
async def get_qcm(
         # number: int,
          number: int = Query(
                  5,
                  title = "Number (Nombre de questions)",
                  description = "Please choose among [5, 10, 20]",
                  #max_length = 1,
                  #min_length = 1,
              ), 
         # use: str,
         # use: Optional[List[str]] = Query(
           use:  str = Query(
                 #db.get_uses(),
                 "Test de positionnement",
                 title = "Use (type de questions)",
                 description = f"Available Cases from database, <br> \
                                 {db.get_uses()}",
                 #max_length = 2,
                 #min_length = 1,
             ), 
         # number: List[str] = Query(
         #         ['5', '10', '20'],
         #         title = "number of questions",
         #         description = "Available scenarios",
         #         max_length = 1,
         #         min_length = 1,
         #     ), 
          #number: int, 
          subjects: 
              Optional[List[str]] = Query(
                  db.get_subjects(),
                  title = "Subject (Catégories de questions)",
                  description = "Available subjects are provided bellow. <br>\
                                 Choose the one to delete using <h1> - </h1>",
                  #max_length = 3,
              )
    ):
    #async def get_qcm(use: str, number: int, subjects: Optional[List[str]] = Query(None)):
    #results = qcm.get_qcm_random('Test de validation', 'BDD', 11)
    #if type(subjects) == str : subjects = [subjects]

    if not (qcm.is_validated(number, use, subjects)):
        raise HTTPException(
            status_code = 422,
            detail = "Incorrect (Unprocessable) parameter, please check again",
            headers={"X-Error": "There goes my error"},
        )
         #status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,

    results = qcm.get_qcm_random(use, subjects, int(number))
    #results = qcm.get_qcm(use, subjects, int(number))
    return {
                "use": use,
                "subject": subjects,
                "number": int(number),
                "results": results
            }

# ----------------------------------------------------------------------------------------




# More details on
@api.post("/qcm/add/")
async def add_qcm(
         question: str, subject: str, correct: str, use: str,\
         responseA: str, responseB: str, responseC: str, responseD: str, \
         username: str = Depends(auth.is_admin)) :
    #async def get_qcm(use: str, number: int, subjects: Optional[List[str]] = Query(None)):
    #results = qcm.get_qcm_random('Test de validation', 'BDD', 11)
    #if type(subjects) == str : subjects = [subjects]
    request = qcm.add_question(question, subject, correct, use, \
                              responseA, responseB, responseC, responseD)
    if request :        
        return {
                   'response_code' : 0,
                   'results' : {
                               'username': username,
                               'question':question, 'subject':subject, 'correct':correct,
                               'use':use, 'responseA': responseA, 'responseB': responseB,
                               'responseC': responseC, 'responseD': responseD
                   }
         }

# ----------------------------------------------------------------------------------------






# -------------------
#@api.get("/questions/{use}/{subjects}/{number}")
async def get_qcm_simple(use, subjects, number):
    #results = qcm.get_qcm_random('Test de validation', 'BDD', 11)
    if type(subjects) == str : subjects = [subjects]
    #results = qcm.get_qcm_random(use, subjects, int(number))
    results = qcm.get_qcm(use, subjects, int(number))
    return {
                "use": use,
                "subject": subjects,
                "number": number,
                "results": results
    }
# ----------------------------------------------------------------------------------------

'''
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8100)
'''
