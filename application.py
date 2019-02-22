import os, sys
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from static.cnn.run import runCNN
import json


UPLOAD_FOLDER = os.path.basename('uploads')
#UPLOAD_FOLDER = os.path.basename('uploads')
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

application = Flask(__name__)
CORS(application)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
results = ""

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename): #local        
            filename = secure_filename(file.filename) #local
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename)) #local
            results = runCNN(os.path.join(application.config['UPLOAD_FOLDER'], filename)) #local
            print(file.filename)            
            results = json.dumps(results)
            os.remove(os.path.join(application.config['UPLOAD_FOLDER'], filename)) #local
            print(results)
            return results
    return  '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@application.route('/test', methods=['GET'])
def test():
    results = runCNN('https://s3.amazonaws.com/pd-tmp-upload/photo.jpg')
    results = json.dumps(results)
    return results

@application.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(application.config['UPLOAD_FOLDER'], filename)
    
@application.route('/hello', methods=['GET'])
def hello():
    hello = 'hello, world'
    hello = json.dumps(hello)
    return hello
    
if __name__ == '__main__':
    application.run(debug=True)