#


from  fastapi import FastAPI, Depends
import database as db
import authentification as auth


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




'''
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8100)
'''
