from flask import Flask
from flask_pymongo import PyMongo

app=Flask(__name__)
app.config['MONGO_URI']="mongodb+srv://Soumesh:SOUMESH2611@cluster0.m1zkdpg.mongodb.net/Pymongo?retryWrites=true&w=majority"

db=PyMongo(app).db
from src import routes