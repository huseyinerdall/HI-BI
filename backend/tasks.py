from requests_html import HTMLSession, AsyncHTMLSession
from mail import Email
import json
Email_ins = Email()

with open('../config.json', 'r') as f:
    config = json.loads(f.read())

class Tasks():

    def exportPdf(self,report_id):
        session = HTMLSession()

        r = session.get('http://localhost:8080/export/'+report_id)
        r.html.render()
    
    def mailing(self,report_id):
        print('a')
        session = HTMLSession()
        print('b')
        r = session.get('http://localhost:8080/export/'+report_id)
        print('c')
        r.html.render()
        print('d')

        messageOptions = {
            "subject": "Konu",
            "body": "Body",
            "user_email": "huseyinerdal@protonmail.com",
            "attachment": "report.pdf"
        }
        Email_ins.sendMail(config['mail'],messageOptions)
        print('e')

def mailing(report_id):
    print('a')
    session = HTMLSession()
    print('b')
    r = session.get('http://localhost:8080/export/'+report_id)
    print('c')
    r.html.render()
    print('d')

    messageOptions = {
        "subject": "Konu",
        "body": "Body",
        "user_email": "huseyinerdal@protonmail.com",
        "attachment": "report.pdf"
    }

    Email_ins.sendMail(config['mail'],messageOptions)
    print('e')