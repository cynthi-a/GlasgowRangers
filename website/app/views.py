import os
from flask import render_template, request, redirect, url_for
from app import app
from werkzeug.utils import secure_filename

#  @app.route('/')
#  @app.route('/index')
#  def index():
    #  user = {'nickname': 'Miguel'}  # fake user
    #  return render_template('index.html',title='Home',user=user)

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
    return render_template('upload.html')

