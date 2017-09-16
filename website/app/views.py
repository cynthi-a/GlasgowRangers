import os
import time
from flask import render_template, request, redirect, url_for, g
from app import app, models, db
from werkzeug.utils import secure_filename
from pdf2jpeg import multiple_pdf2jpeg
from models import Page
#new import statements
import sys, os
from pocketsphinx import *
import pyaudio

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',title='Home')

@app.route('/upload',methods=['GET', 'POST'])
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
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            path = path.replace('.pdf','{}.pdf')
            jpeg_path = path.replace('.pdf','.jpeg')
            output_names = multiple_pdf2jpeg(path,jpeg_path)
            models.delete_all()
            models.create_from_names(output_names)
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/pages')
@app.route('/pages/<int:page>', methods=['GET','POST'])
def display_pages(page=1):
    posts = models.Page.query.paginate(page, 1, False)

    #CHANGES START
    if page > 1:
        modeldir = get_model_path()

        config = Decoder.default_config()
        config.set_string('-hmm', os.path.join(modeldir, 'en-us'))
        config.set_string('-dict', os.path.join(modeldir, 'cmudict-en-us.dict'))
        config.set_string('-kws', 'keyphrase.list')

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        stream.start_stream()

        decoder = Decoder(config)
        decoder.start_utt()
        while True:
            buf = stream.read(1024)
            decoder.process_raw(buf, False, False)
            if decoder.hyp() != None:
                print  "==============Keyword: ", decoder.hyp().hypstr
                page=Page.query.filter(Page.keyword==decoder.hyp().hypstr).one()
                unique = page.id
                #print "Detected keyword", decoder.hyp(), "restarting search"
                decoder.end_utt()
                decoder.start_utt()
                return render_template(url_for('diplay_pages',page=page+1))
    return render_template('pages.html', posts=posts) 

@app.route('/keyword_mapping')
@app.route('/keyword_mapping', methods=['GET','POST'])
def keyword_entry():
    pages=Page.query.all()

    if request.method == 'POST':

        for page in pages:
            page.keyword = request.form[str(page.id)]

    return render_template('keyword_mapping.html', pages=pages)
