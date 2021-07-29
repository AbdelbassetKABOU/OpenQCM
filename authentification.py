
# ------------------------------------------------------------------
#   /=====================\
#  |  authentification.py  |
#   \=====================/
#
# For authentification, we opted for a simplest scenario. The app expects a 
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
from fastapi import Depends, HTTPException, status 
from fastapi.security import HTTPBasic, HTTPBasicCredentials

identified = {
                "alice": "wonderland",
                "bob": "builder",
                "clementine": "mandarine",
                "admin": "4dm1N"
}

security = HTTPBasic()

def is_identified(credentials: HTTPBasicCredentials = Depends(security)):
    for user, passwd in identified.items():
       if secrets.compare_digest(credentials.username, user):
           if secrets.compare_digest(credentials.password, passwd):
               return True
    return False


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    if not (is_identified(credentials)):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
            headers = {"WWW-Authenticate" : "Basic"},
        )
    return credentials.username


def is_admin(credentials: HTTPBasicCredentials = Depends(security)):
    
    if not secrets.compare_digest(credentials.username, "admin"):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Access to the requested resource is forbidden for the current user",
            headers = {"WWW-Authenticate" : "Basic"},
        )
    else :
        if not is_identified(credentials) : 
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Incorrect email or password",
                headers = {"WWW-Authenticate" : "Basic"},
            )
    return credentials.username



