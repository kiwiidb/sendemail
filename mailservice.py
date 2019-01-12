import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSender():
    
    def __init__(self, password, fromaddr, templatefilepath="mail.txt"):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.from_address = fromaddr
        self.server.login(fromaddr, password)
        self.template = open(templatefilepath, 'r')
        self.template_text = self.template.read()

    def send_email(self, to_address, replacedict):
        template_text = self.template_text
        for key, value in replacedict.items():
            template_text = template_text.replace(key, value)

        msg = MIMEMultipart()
        msg['To'] = to_address
        msg['From'] = self.from_address
        msg['Subject'] = "Thanks for participating in the lightning lottery !"

        msgText = (MIMEText(template_text))
        msg.attach(msgText)

        text = msg.as_string()
        self.server.sendmail(self.from_address, to_address, text)

from flask import Flask, request, jsonify, Response
import json
from secrets import gmail_pw, from_addr
app = Flask(__name__)
ES = EmailSender(gmail_pw, from_addr)

@app.route("/sendmail", methods=['POST'])
def mailParticipant():
    try:
        requestDict = json.loads(request.data)
        email = requestDict['email']
    except (KeyError, ValueError) as e:
        resp =  jsonify({"message" : "Bad request, could not find email field"})
        resp.status_code = 402
        return resp
    try:
        operator = requestDict['operator']
    except KeyError:
        print("No operator found, invalid request")
        resp =  jsonify({"message" : "Invalid operator"})
        resp.status_code = 402
        return resp
    try:
        nickname = requestDict['nickname']
    except KeyError:
        nickname = ""
    replacedict = {"NICKNAME": nickname, "OPERATOR": operator}
    ES.send_email(email, replacedict)


