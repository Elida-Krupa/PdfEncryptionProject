import PyPDF2
from datetime import datetime
from datetime import timedelta
import tkinter
from tkinter import filedialog
import os
from PyPDF2 import PdfFileWriter
import sqlite3
import string
import random
import csv

root = tkinter.Tk()
root.withdraw()


class PdfEncryption:

    @staticmethod
    def file_encrypt_datetime():
        current_time = datetime.now()
        print(current_time)
        modified_time = current_time.replace(microsecond=0)
        print(modified_time)
        my_time_format = "%Y-%m-%d %H-%M-%S"
        converted_format_time = datetime.strftime(modified_time, my_time_format)
        return converted_format_time

    def encrypt_file_size(pwd_pdf_file):
        file_size = os.path.getsize(pwd_pdf_file)
        return str(file_size) + " bytes"

    def database(file_name, file_size, f_datetime, enpwd):
        connection = sqlite3.connect("PDF_data.db")
        c = connection.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS EncryptedPDF("pdf_file_name" text,
        "pdf_file_size" integer, 
        "date_time_of_encryption" integer,
        "encrypted_pwd" text)""")
        c.execute(f'INSERT INTO EncryptedPDF(pdf_file_name, pdf_file_size, date_time_of_encryption, encrypted_pwd)'\
                    f"VALUES ('{file_name}', '{file_size}', '{f_datetime}', '{enpwd}')")
        connection.commit()
        db_select = """SELECT * FROM EncryptedPDF"""
        connection.execute(db_select)
        connection.close()

    def get_password(length):
        chars = string.ascii_letters + string.digits + '!@#$%^&*()'
        random.seed = (os.urandom(1024))
        pwd = []
        for x in range(length):
            pwd.append(random.choice(chars))
            enpwd = "".join(pwd)
        return enpwd

    def random_gmail(char_num):
        return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))

    def append_to_csv(path, fieldnames, rows):
        is_write_header = not os.path.exists(path) or os.stat(path).st_size == 0
        if not is_write_header:

            with open(path, 'r') as f:
                reader = csv.reader(f)
                header = next(reader)
                if header != fieldnames:
                    raise ValueError(f'Incompatible header: expected {fieldnames}, '
                                         f'but existing file has {header}')

        with open(path, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if is_write_header:
                writer.writeheader()
            writer.writerows(rows)


pdf_obj = PdfEncryption

fname = filedialog.askopenfilename()
base_file_name = os.path.basename(fname)
file_head, file_tail = os.path.split(fname)
file_folder = file_head

filelist = []
for (root, dirs, file) in os.walk(file_folder):
    for filename in file:
        if ".pdf" in filename:
            filelist.append(filename)
length = len(filelist)

for x, file_name in enumerate(filelist):
    try:
        pdf_in_file = open(file_folder + "/" + file_name, 'rb')
        inputPdf = PyPDF2.PdfFileReader(pdf_in_file)
        pages_no = inputPdf.numPages
        output = PyPDF2.PdfFileWriter()

        file_open = False
        file_pwd = False

        for i in range(pages_no):
            inputPdf = PyPDF2.PdfFileReader(pdf_in_file)
            output.addPage(inputPdf.getPage(i))

            if not file_pwd:
                enpwd = pdf_obj.get_password(10)
                file_pwd = True
                output.encrypt(enpwd)
                print("encrypted password: " + enpwd)

                with open("D:\pwd_protected_" + file_name, "wb") as outputStream:
                    output.write(outputStream)

                    if not file_open:
                        f_datetime = pdf_obj.file_encrypt_datetime()
                        print("Date Time: " + f_datetime)

                        pwd_file_name = "D:\pwd_protected_" + file_name
                        print("Encrypted File Name:" + pwd_file_name)
                        file_size = pdf_obj.encrypt_file_size(pwd_file_name)
                        print("File Size: " + file_size)

                        pdf_obj.database("pwd_protected_" + file_name, file_size, f_datetime, enpwd)

                        mailid = pdf_obj.random_gmail(7) + "@gmail.com"
                        fieldnames_ = ['File Name', 'File Size', 'Date Time', 'Encryption Password', 'mailid']
                        rows_ = [
                            {'File Name': "pwd_protected_" + file_name, 'File Size': file_size, 'Date Time': f_datetime, 'Encryption Password': enpwd, 'mailid': mailid}
                        ]
                        pdf_obj.append_to_csv("PDF_Encryption.csv", fieldnames_, rows_)

                        file_open = True
        pdf_in_file.close()
        os.remove(file_folder + "/" + file_name)
    except Exception as ex:
        print(ex)

    else:
        print("PDF is encrypted")
