from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from werkzeug.security import generate_password_hash, check_password_hash

with open('../config.json', 'r') as f:
    config = json.loads(f.read())

app = Flask(__name__)


SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}/{}'.format(config['db']['type'],config['db']['user'],config['db']['password'],config['db']['address'],config['db']['db_name'])
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image = db.Column(db.Text)
    department = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')

    def to_dict(self):
        return dict(id=self.id, username=self.username)
"""
    def __repr__(self):
        return '<User %r>' % self.username
"""
class Reports(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    htmls = db.Column(db.Text)
    name = db.Column(db.Text)
    user = db.Column(db.String(120),nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    def __init__(self, id,content,htmls, user, name , date):
        self.id = id
        self.content = content
        self.htmls = htmls
        self.user = user
        self.name = name
        self.date = date

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.Text)
    color = db.Column(db.Text)
    report_name = db.Column(db.Text)
    report_id = db.Column(db.Integer)
    crontab = db.Column(db.Text)
    user = db.Column(db.String(120),nullable=False)
    date = db.Column(db.DateTime,default='datetime.utcnow')
    def __init__(self,id,type,color,report_name, report_id, user, crontab , date):
        self.id = id
        self.type = type
        self.color = color
        self.report_name = report_name
        self.report_id = report_id
        self.crontab = crontab
        self.user = user
        self.date = date

def authenticate(data):
    print(data.get('username'))
    print(data.get('password'))
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return None
        
    user = User.query.filter_by(username=username).first()
    if not user:# or not check_password_hash(user.password, password):
        return None
    return user

def createDB():
    db.create_all()
createDB()