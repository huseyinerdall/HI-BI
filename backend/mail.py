import email, smtplib, ssl, json

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

with open('../mail.json', 'r') as f:
    config = json.loads(f.read())
    print(config['mail'])

class Email():

    def sendMail(self,messageOptions):
        
        sender_email = config['mail']['sender'] or "hi.business.intelligence@gmail.com"
        password = config['mail']['password'] or "hibiHIBI"

        subject = messageOptions['subject'] or "This is default subject"
        body = messageOptions['body'] or "This is default body"
        receiver_email = messageOptions['user_email'] or "huseyinerdal@protonmail.com"
        if(receiver_email is None):
            Exception("Your email address is not defined.")
        

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email

        message.attach(MIMEText(body, "plain"))

        filename = "reports/" + messageOptions['attachment'] or "reports/report.pdf"
        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)