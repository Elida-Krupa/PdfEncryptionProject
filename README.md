# PdfEncryptionProject
Project is PDF Encryption. 
Encrypting the PDF with the password
Class is PdfEncrytion.
Functions are to get date time, get file size, create database, get password, get random Gmail, write to csv file
Try, except, else block 

Select the project “.pdf” file by using tkinter and all the “.pdf” files in that folder is accessed by using os.walk
Output encrypted file contains datetime stamp
The encrypted file details are stored in sqlite3 PDF_data.db database. In the EncryptedPDF table with ‘file name’, ‘file size’, ‘time and date of encryption’, ‘encrypted password’
The input file once it is encrypted, it is deleted.
The encrypted file is stored in a different folder (D:\)
The encrypted file details are stored in PDF_Encryption.csv file with ‘file name’, ‘file size’, ‘time and date of encryption’, ‘encrypted password’ and ‘Gmail ID’

A CsvToMail python file is created, which reads the PDF_Encryption.csv file.
It triggers mail from the mail id given in the PDF_Encryption.csv file through the send_mail function
The mail contains the PDF file and the encrypted password.
