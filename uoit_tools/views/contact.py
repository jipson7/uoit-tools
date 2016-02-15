from flask import Blueprint, request, jsonify
import smtplib, base64
from email.mime.text import MIMEText
from validate_email import validate_email

contact = Blueprint('contact', __name__)

@contact.route('', methods=['POST'])
def send_email():
    name = request.form.get('name', None)
    email = request.form.get('email', None)
    message = request.form.get('message', None)

    if not name or not email or not message:
        return 'Must supply Name, Email, and a message to send', 400
    if not validate_email(email):
        return email + ' is not a valid email', 400

    body = 'From: ' + email + '\n\n Message: ' + message

    password = (base64.b64decode('dW9pdHRvb2xzOTcxMQ==')).decode('utf-8')
    username = 'uoit.tools@gmail.com'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    msg = MIMEText(body)
    msg['Subject'] = 'Regarding Uoit-Tools'
    msg['From'] = 'uoit.tools@gmail.com'
    msg['To'] = 'uoit.tools@gmail.com'
    server.send_message(msg)
    server.quit()
    return 'Message Sent Successfully', 200

