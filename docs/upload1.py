import os
import polygon
from flask import Flask, render_template, request, redirect, url_for
import json
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api

UPLOAD_FOLDER = '/Users/macbook/app'
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','json','html'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    result = ""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = polygon.olon(filename)     
            #return redirect(url_for('upload_file', filename=filename))
            
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      {}<br>
        <p><input type=file name=file>
         <input type=submit value=Upload>    
      
</form>
       
    '''.format(result)


    
if __name__ == '__main__':
    app.run(debug=True)
