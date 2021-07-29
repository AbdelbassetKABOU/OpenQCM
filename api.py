
#
#   /===============\
#  |     api.py      |
#   \===============/
#
# This is the tip of the icebirg for our proposed architecture. 
# The current module, along with data access/management, authentification 
# and logic modules, constitute the basic components of an n-tier architecture.
# This architecture (referred to as multi-tier arch also) is an architectural 
# pattern in which presentation, application processing (logic) and data 
# management functions are separated [1]. More details are provided later.
#
# This module 
#
# The current module consists on a set of functions accessible via a restful API. 
# The implementation is based mainly on FastAPI [2], the new emerged frameword 
# that is causing a considerable amount of buzz these days. 
#
# AbdelbasetKABOU
#
# [1] https://fastapi.tiangolo.com/
# [2] https://en.wikipedia.org/wiki/Multitier_architecture

#


from  fastapi import FastAPI, Depends, Query, HTTPException, status
from typing import List, Optional
import database as db
import authentification as auth
import qcm

# -------------
api = FastAPI(
                 title = 'OpenQCM API',
                 description=' A simple HTTP RESTful API interecting with a database and \
                               returning a set of Multiple Choice Question (MCQ)',
                 version='0.1'
      )
# --------------------------------------------------------------------------------------------




# --------------------------------------
# - Verify that the API is functional.
# ------------------------
@api.get('/status')
async def status():
    return {
               'status': 1
    } # ------------------------
# ----


# ------------------------
# - Get the current user :
# ------------------------
@api.get("/users/me")
async def authenticate_user(username: str = Depends(auth.get_current_username)):
    return {
                "username": username,
    } #-----------------------------
# ---


# ----------------------------------------
# List available subjects in the database
# --------------------------------------------
@api.get("/uses")
async def get_uses():
    available_uses = db.get_uses()
    return available_uses
# ---------------------



# ----------------------------
# - Get a MCQ from database :
# ----------------------------
#
#    - Containing 5,10 or 20 questions 
#    - Related to one or more subject
#      (category)
#    - Related to one use (e.g. Test de 
#      positionnement, Test de validation, etc)
#
#    + It include a random rendering making results
#       differ each time
# -----------------------------------------------
@api.get("/qcm/")
async def get_qcm(
          number: int = Query(
                  5,
                  title = "Number (Nombre de questions)",
                  description = "Please choose among [5, 10, 20]",
                  #max_length = 1,
                  #min_length = 1,
              ), 
           use:  str = Query(
                 #db.get_uses(),
                 "Test de positionnement",
                 title = "Use (type de questions)",
                 description = f"Available Cases from database, <br> \
                                 {db.get_uses()}",
                 #max_length = 2,
                 #min_length = 1,
             ), 
          subjects: 
              Optional[List[str]] = Query(
                  db.get_subjects(),
                  title = "Subject (Catégories de questions)",
                  description = "Available subjects are provided bellow. <br>\
                                 Choose the one to delete using <h1> - </h1>",
                  #max_length = 3,
              )
    ):
    if not (qcm.is_validated(number, use, subjects)):
        raise HTTPException(
            status_code = 422,
            detail = "Incorrect (Unprocessable) parameter, please check again",
            headers={"X-Error": "There goes my error"},
        )

    results = qcm.get_qcm_random(use, subjects, int(number))
    return {
                "use": use,
                "subject": subjects,
                "number": int(number),
                "results": results
            }
    # -----------------
    # - More details on
    # https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#query-
    #  parameter-list-multiple-values-with-defaults
    # - Python fastapi.Query() Examples -->
    # https://www.programcreek.com/python/example/113514/fastapi.Query
    # -----------------------------------------------------------------




# --------------------------
# - Create a new question 
# -------------------------
#
# (requires admin privileges). 
#
# -----------------------------------------------
@api.post("/qcm/add/")
async def add_qcm(
         question: str, subject: str, correct: str, use: str,\
         responseA: str, responseB: str, responseC: str, responseD: str, \
         username: str = Depends(auth.is_admin)) :
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
         } # --------------------------------------------
# ----------




# ----------------------------
# - Get a MCQ from database :
#    - The same thing as the previous route, however
#      it's now consist on simple (not random) request
# -----------------------------------------------
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
    } # --------------------------
#------


'''
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8100)
'''
