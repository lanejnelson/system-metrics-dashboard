from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import redis

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


r = redis.Redis(host='localhost', port=6379, decode_responses=True)