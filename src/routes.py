from src.app import app,db
from flask import request
from flask_bcrypt import generate_password_hash,check_password_hash
from jwt import encode
from src.middleware import authenticate
from bson.objectid import ObjectId
from bson import json_util
import os
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET=os.getenv('JWT_SECRET')

@app.route('/')
def index():
    return {
        "hello":'world'
    }

@app.route('/register',methods=['POST'])
def register():
    if request.method=='POST':
        try: 
            body=dict(request.get_json())
            username=body['username']
            password=body['password']
            insertingBody=body.copy()
            hash_password=generate_password_hash(password,10).decode('utf-8')
            user=db.users.find_one({"username":username})
            if user is not None:
                return {
                    "error":"user already exist"
                },400
            insertingBody['password']=hash_password
            user=db.users.insert_one(insertingBody)
            data={
                "user":{
                    "id":str(user.inserted_id)
                }
            }
            authToken=encode(data,JWT_SECRET)
            return {
            "authToken":authToken
            }
        except Exception as e:
            print(e)
            return {
                "error":'Server Erorr'
            },500


@app.route('/login',methods=['POST'])
def login():
    if request.method=='POST':
        try:
            body=request.get_json()
            username=body['username']
            password=body['password']
            user=db.users.find_one({"username":username})
            if not user:
                return {
                    "error":"username/password is invalid"
                },400
            hash_password=user['password']
            if not ( verified := check_password_hash(hash_password,password)):
                return {
                    "error":"username/password is invalid"
                },400
            data={
                "user":{
                    "id":str(user.get('_id'))
                }
            }
            authToken=encode(data,JWT_SECRET)
            return {
                "verified":verified,
                "authToken":authToken
            }
        except Exception as e:
            print(e)
            return {
                "error":"server error"
            }


@app.route('/getUser')
@authenticate
def getUser():
    try:
        user=request.environ['user']
        user=db.users.find_one({"_id":ObjectId(user)},{"password":0})
        if not user:
            return {
                "error":"user doesn't exist"
            }
        resp=json_util.dumps(user)
        return resp
    except Exception as e:
        print(e)
        return{
            "error":"server error"
        }