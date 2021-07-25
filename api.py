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


'''

from  fastapi import FastAPI, Depends
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
@api.get("/questions/{use}/{subject}/{number}")
async def get_qcm(use, subjects, number):
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
