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




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8100)
