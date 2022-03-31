import os
from fpdf import FPDF
import pdfx
import weasyprint
from PIL import Image
import smtplib
import time
import glob
import PyPDF2
import re
from urllib import request
from celery import Celery
from flask import Flask, request, render_template, session, url_for, flash, redirect
from flask_mail import Message, Mail
from celery_utils import get_celery_app_instance


from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = '/home/dell/Desktop/task/celery_flask/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
SAVE_FOLDER = '/home/dell/Desktop/task/celery_flask/save'
app.config['SAVE_FOLDER'] = SAVE_FOLDER

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = get_celery_app_instance(app)

@app.route('/url', methods=['GET'])
def file():
    if request.method == 'GET':
        return render_template('file.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
      x=f.filename
      url_finding.delay(x)
      return 'file uploaded successfully'

@celery.task(name="hii")
def url_finding(y):
    x = pdfx.PDFx(os.path.join(app.config['UPLOAD_FOLDER'], y))
    u=x.get_references_as_dict()
    u=u.values()
    for i in u:
        for j in i:
            name=j[0]+".pdf"
            weasyprint.HTML(j).write_pdf(os.path.join(app.config['SAVE_FOLDER'], name))


@app.route('/process/<name>')
def process(name):
    reverse.delay(name)
    return "i sent a async request"

@celery.task(name='celery_basic')
def reverse(string):
    return string[::-1]

if __name__ == "__main__":
    app.secret_key = 'SECRET KEY'
    app.run(debug=True)