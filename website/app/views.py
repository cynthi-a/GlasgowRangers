import os
from flask import render_template, request, redirect, url_for, g
from app import app, views, models
from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>', methods=['GET','POST'])
def index(page=1):
    user = {'nickname': 'Miguel'}  # fake user
    posts = models.Page.query.paginate(page, 1, False)
    return render_template('index.html',title='Home',user=user, posts=posts)

@app.route('/',methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            print(filename)
            print(url_for('upload_file', filename=filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

