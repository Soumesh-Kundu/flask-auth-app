from functools import wraps
from flask import Response,request
from jwt import decode
from dotenv import load_dotenv
import os 
load_dotenv()
JWT_SECRET=os.getenv('JWT_SECRET')

def authenticate(func):
    @wraps(func)
    def middleware(*args,**kwargs):
        authToken=request.headers['authToken']
        if not authToken:
            return Response({"error":"Not a valid Token"},mimetype='application/json',status=401)
        user=decode(authToken,JWT_SECRET,algorithms='HS256')
        request.environ['user']=user['user']['id']
        return func(*args,**kwargs)
    return middleware