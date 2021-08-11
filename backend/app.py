from flask import Flask, render_template, jsonify, request, send_from_directory, current_app
from datetime import datetime, timedelta
from functools import wraps
import json, time, jwt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect
from flask_cors import CORS
from source import Source
from mail import Email
from scheduler import Scheduler
import pdfkit, time, os
from werkzeug.utils import secure_filename
from models import Tasks, User, Reports, authenticate, db

with open('../config.json', 'r') as f:
    config = json.loads(f.read())

UPLOAD_FOLDER = '/reports'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/reports'
app.config['SECRET_KEY'] = "dTvsKE2i5$b4r15X{Zl]-YMe"
Source_ins = Source()
Scheduler_ins = Scheduler()
Email_ins = Email()

app = Flask(__name__,static_url_path='/reports',static_folder='reports')
app.config['STATIC_FOLDER'] = 'reports'

CORS(app)

@app.route('/configureDB',methods=['GET','POST'])
def configureDB():
    if request.method == "POST":
        type = request.json['type']
        user = request.json['user']
        password = request.json['password']
        address = request.json['address']
        db_name = request.json['db_name']
        d = (request.get_json())
        db_dict = { "db": d }
        try:
            print('a')
            engine = create_engine('{}://{}:{}@{}'.format(type,user,password,address))
            conn = engine.connect()
            conn.execute("commit")
            conn.execute("create database "+db_name)
            conn.close()
            print('b')
        except Exception as e:
            print(e)
            return str('Wrong  username or password')
        with open('../config.json', 'w') as json_file:
            json.dump(db_dict, json_file)
        time.sleep(0.2)
        with open('../config.json', 'r') as f:
            config = json.loads(f.read())
        time.sleep(0.2)
        SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}/{}'.format(config['db']['type'],config['db']['user'],config['db']['password'],config['db']['address'],config['db']['db_name'])
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        db = SQLAlchemy(app)
        class User(db.Model):
            __tablename__ = 'user'
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(80), unique=True)
            email = db.Column(db.String(120), unique=True, nullable=False)
            password = db.Column(db.String(120), nullable=False)
            image = db.Column(db.Text)
            department = db.Column(db.String(80))

            def __repr__(self):
                return '<User %r>' % self.username

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
        db.create_all()
    return str('OK')

@app.route('/configuredDB',methods=['GET','POST'])
def configuredDB():
    return config['db']

@app.route('/register/', methods=('POST',))
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/login/', methods=('POST',))
def login():
    data = request.get_json()
    
    return jsonify({ 'token': 1 })

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify

@app.route('/')
@token_required
def index():
    return render_template('index.html')

@app.route('/saveUser',methods=['GET','POST'])
def saveUser():
    if request.method == "POST":
        user = User.query.filter_by(id='1').first()
        user.username = request.get_json()['user']['name']
        user.email = request.get_json()['user']['email']
        user.image = request.get_json()['user']['image']
        user.department = request.get_json()['user']['department']
        #user = User(username=name, email=email, image=image, department=department)
        db.session.add(user)
        db.session.commit()
        return 'OK'
    return 'user'

@app.route('/getUserInfos',methods=['GET','POST'])
def getUserInfos():
    l = User.query.all()
    infos = []
    for row in l:
        d = {}
        d['id'] = row.id
        d['name'] = row.username
        d['image'] = row.image
        d['department'] = row.department
        d['email'] = row.email
        infos.append(d)
    return jsonify(infos)


@app.route('/uniqueID',methods=['GET','POST'])
def uniqueID():
    all = Reports.query.with_entities(Reports.id).all()
    if not all:
        return str(1)
    uid = all[len(all)-1][0] + 2
    return str(uid)

def uniqueIDTask():
    all = Tasks.query.with_entities(Tasks.id).all()
    if not all:
        return str(1)
    uid = all[len(all)-1][0] + 1
    return str(uid)
    
@app.route('/createReport',methods=['GET','POST'])
def createReport():
    if request.method == "POST":
        js = request.json['graph']
        id = request.json['id']
        ctrl = Reports.query.filter_by(id=id)
        if(ctrl):
            print('if')
            report = Reports.query.filter_by(id=id)
            report.content = js
        else:
            print('else')
            report = Reports(id=id,content=js,user="Hüseyin erdal")
            db.session.add(report)
        db.session.commit()
        return 'OK'
    return 'asa'

@app.route('/getReportInfos',methods=['GET','POST'])
def getReportInfos():
    l = Reports.query.all()
    infos = []
    for row in l:
        d = {}
        d['id'] = row.id
        d['name'] = row.name
        d['date'] = row.date
        d['content'] = row.content
        infos.append(d)
    return jsonify(infos)

@app.route('/getReport',methods=['GET','POST'])
def getReport():
    if request.method == "POST":
        id = request.json['id']
        report = Reports.query.filter_by(id=id).first()
        print(report.content)
        i=0
        graphs = json.loads(report.content)
        try:
            for one in graphs:
                t = one['table_name']
            x = one['x_axis']
            y = one['y_axis']
            print(t,x,y)
            data=Source_ins.dataList(t,x,y)
            graphs[i]['options']['grid']['xaxis']['categories'] = data['x']
            graphs[i]['options']['grid']['yaxis']['categories'] = data['y']
            graphs[i]['series'][0]['name'] = 'isim'
            graphs[i]['series'][0]['data'] = data['y']
            i = i+1
        except:
            graphs = json.loads(report.content)
        d = {}
        d['graphs'] = json.dumps(graphs)
        d['htmls'] = report.htmls
        d['name'] = report.name
        return jsonify(d)
    return str('Bir hata oluştu')

@app.route('/sendGraphList',methods=['GET','POST'])
def sendGraphList():
    l = Reports.query.all()
    #print(l)
    return 'asa'

@app.route('/createHTML',methods=['GET','POST'])
def createHTML():
    if request.method == "POST":
        print(request.json)
        js = request.json['html']
        ctrl = Reports.query.filter_by(id=id)
        if(ctrl):
            print('if')
            report = Reports.query.filter_by(id=id)
            report.htmls = js
        else:
            print('else')
            report = Reports(id=id,htmls=js,user="Hüseyin erdal")
            db.session.add(report)
        db.session.commit()
        return 'OK'
    return 'asa'

@app.route('/sendHTMLList',methods=['GET','POST'])
def sendHTMLList():
    l = Reports.query.all()
    #print(l)
    return 'asa'

@app.route('/saveReport',methods=['GET','POST'])
def saveReport():
    if request.method == "POST":
        id = int(request.json['id'])
        if(id<0):
            id = 1
        graphList = request.json['graphList']
        htmlList = request.json['htmlList']
        #print(graphList)
        graphsStr = json.dumps(graphList)
        htmlsStr = json.dumps(htmlList)
        ctrl = Reports.query.filter_by(id=id).first()
        if(ctrl is None):
            try:
                name = request.json['name']
                newreport = Reports(id=id,content=graphsStr,user="Hüseyin erdal",date=datetime.utcnow(),htmls = htmlsStr,name=name)
                db.session.add(newreport)
                db.session.commit()
                return 'OK'
            except:
                return 'FAIL'
        else:
            print(ctrl is not None)
            report = Reports.query.filter_by(id=id).first()
            report.content = graphsStr
            report.htmls = htmlsStr
            db.session.commit()
            return 'UPDATED'
    return 'asa'

@app.route('/deleteReport',methods=['GET','POST'])
def deleteReport():
    if request.method == "POST":
        id = int(request.json['id'])
        try:
            report = Reports.query.filter_by(id=id).first()
            db.session.delete(report)
            db.session.commit()
            return 'OK'
        except:
            return 'FAIL'
    return "DELETE"

def runTasks():
    print(Scheduler_ins.running())
    l = Tasks.query.all()
    tasksNumber = len(l)
    for row in l:
        Scheduler_ins.runTask(row.crontab, row.type, row.report_name,row.report_id)
    if not Scheduler_ins.running():
        Scheduler_ins.startTasks()
runTasks()
@app.route('/setTask' ,methods=['GET','POST'])
def setTask():
    id = uniqueIDTask()
    if request.method == "POST":
        try:
            crontab = request.json['crontab']
            task = request.json['task']
            report = request.json['report']
            color = request.json['color']
            print(request.json['report_id'])
            report_id = request.json['report_id']
            print(report_id)
            newtask = Tasks(id=id,crontab=json.dumps(list(crontab.values())),color=color,user="Hüseyin erdal",type=task,date=datetime.utcnow(),report_name=report,report_id=report_id)
            db.session.add(newtask)
            db.session.commit()
            runTasks()
            return 'OK'
        except Exception as e:
            print(e)
            return 'FAIL'
    return 'TASK'

@app.route('/getTasks' ,methods=['GET','POST'])
def getTasks():
    i = 0
    taskList = Scheduler_ins.taskList()
    l = Tasks.query.all()
    tasks = []
    for row in l:
        d = {}
        d['type'] = row.type
        d['start'] = row.crontab
        d['report'] = row.report_name
        d['color'] = row.color
        d['date'] = row.date
        d['nextRunDate'] = taskList[i].next_run_time
        d['id'] = taskList[i].id
        tasks.append(d)
        i+=1
    return jsonify(tasks)

@app.route('/tableNames' ,methods=['GET','POST'])
def tableNames():
    return jsonify(Source_ins.tableNames())


@app.route('/columnNames' ,methods=['GET','POST'])
def columnNames():
    if request.method == "POST":
        t = request.json['table']
    return jsonify(Source_ins.columnNames(t))

#this function create pdf
@app.route('/getHTML',methods=['GET','POST'])
def getHTML():
    if request.method == "POST":
        print(request.json)
        html = request.json['aaaa']
        doneHtml = html.replace('hibi-report-','')
        a="<html style='height: 100%'><head><meta charset='UTF-8'></head><body style='background-color:lightgray'>"
        b="</body></html>"
        full=a+doneHtml+b
        f = open(APP_ROOT+"/reports/report.html","w+")
        f.write(full)
        f.close()
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "utf-8"
        }
        css = APP_ROOT + '/clean.css'
        time.sleep(2)
        pdfkit.from_file(APP_ROOT+'/reports/report.html',APP_ROOT+'/reports/report.pdf',options=options,css=css)
