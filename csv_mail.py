import csv
from collections import defaultdict
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class CsvToMail:
    def send_mail(toaddr, file, pwd, fromaddr="*******@gmail.com",):
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Encrypted PDF with password"
        body = """Hi, I have attached the pdf file and the password\npassword =""" + pwd
        msg.attach(MIMEText(body, 'plain'))
        filename = "D:/"+file
        attachment = open(filename, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, "*******")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()


mail_obj = CsvToMail
columns = defaultdict(list)
with open("PDF_Encryption.csv", 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        for (k, v) in row.items():
            columns[k].append(v)

fnames = columns['File Name']
passwords = columns['Encryption Password']
emails = columns['mailid']

for (mail, file, pwd) in zip(emails, fnames, passwords):
    mail_obj.send_mail(mail, file, pwd)