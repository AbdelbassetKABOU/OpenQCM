
# ------------------------------------------------------------------
#   /===============\
#  |   HTTP  Auth    |
#   \===============/
#
# For authentification, let us opt for a simplest scenario. The app expects a 
# header containing a username and password. 
# If not the case, it returns an HTTP 401 "Unauthorized" error.
# The app returns a header WWW-Authenticate with a value of Basic and optional 
# realm parameter telling the browser to show the integrated prompt for 
# a username/password --> when you type username/passwd, the browser sends them 
# in header automatically ... More details in [1]
#


# We use the Python standard module secrets to check the username and password. 
# More specefically, using secrets.compare_digest() would be an efficient way to 
# secure against "timing attacks", c.f. [1].

# [1] https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
# -----------------------------------------------------------------


import secrets

from fastapi import Depends, FastAPI, HTTPException, status 
from fastapi.security import HTTPBasic, HTTPBasicCredentials


api = FastAPI()
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "coucou")
    correct_password = secrets.compare_digest(credentials.password, "coucou")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
            headers = {"WWW-Authenticate" : "Basic"},
        )
    return credentials.username


@api.get("/users/me")
#def authenticate_user(credentials: HTTPBasicCredentials = Depends(get_current_username)):
def authenticate_user(username: str = Depends(get_current_username)):
    return {
                "username": username,
                #"username": credentials.username,
                #"password": credentials.password
    }




if __name__ == '__main__': 
    import uvicorn
    uvicorn.run(api, host="localhost", port=8100)

