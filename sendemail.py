import argparse
from argparse import ArgumentParser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-code', '--amazon_code')
    parser.add_argument('-address', '--email_address')
    parser.add_argument('-password', '--password')
    parser.add_argument('-fromaddress', '--fromaddress')
    args = parser.parse_args()

    amazon_code = args.amazon_code
    email_address = args.email_address
    attachment = 'LLT.jpg'

    input  = open('mail.txt', 'r')
    clean  = input.read().replace("number", amazon_code)

    fromaddr = args.fromaddress
    msg = MIMEMultipart()
    msg[email_address] = email_address
    msg['Subject'] = "Congratulations !"

    msgText = (MIMEText(clean, attachment))
    msg.attach(msgText)

    fp = open(attachment, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    img.add_header('Content-ID', '<{}>'.format(attachment))
    msg.attach(img)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, args.password)
    text = msg.as_string()
    server.sendmail(fromaddr, email_address, text)
    server.quit()

if __name__=="__main__":
	main()