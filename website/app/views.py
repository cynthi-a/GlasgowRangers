import os
import time
from flask import render_template, request, redirect, url_for, g
from app import app, models, db
from werkzeug.utils import secure_filename
from pdf2jpeg import multiple_pdf2jpeg
from models import Page
#new import statements
import sys
import os
from pocketsphinx import *
import pyaudio


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/upload', methods=['GET', 'POST'])
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
            path = path.replace('.pdf', '{}.pdf')
            jpeg_path = path.replace('.pdf', '.jpeg')
            output_names = multiple_pdf2jpeg(path, jpeg_path)
            models.delete_all()
            models.create_from_names(output_names)
            return redirect(url_for('index'))
    return render_template('upload.html')


@app.route('/pages/<int:page>', methods=['GET', 'POST'])
def display_pages(page=1):
    total_number = len(Page.query.all())
    next_id = page+1 if page < total_number else 0
    prev_id = page-1 if page > 1 else 0
    this_page = Page.query.filter_by(id=page).first()
    print(next_id, prev_id, total_number)

    if page > 1:
        modeldir = get_model_path()

        config = Decoder.default_config()
        config.set_string('-hmm', os.path.join(modeldir, 'en-us'))
        config.set_string(
            '-dict', os.path.join(modeldir, 'cmudict-en-us.dict'))
        config.set_string('-kws', 'keyphrase.list')

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1,
                        rate=16000, input=True, frames_per_buffer=1024)
        stream.start_stream()

        #decoder = Decoder(config)
        #decoder.start_utt()
        while True:
            buf = stream.read(1024)
            #decoder.process_raw(buf, False, False)
            #if decoder.hyp() != None:
            #if decoder.hyp() == None:
            if (1):
                #  this_key = decoder.hyp().hypstr
                this_key = '3'
                print "=========Keyword=======\n", this_key
                next_page = Page.query.filter_by(keyword=this_key).first()
                #decoder.end_utt()
                #decoder.start_utt()
                return render_template('pages.html', 
                                       this_filename=next_page.filename, 
                                       next_id=next_id, 
                                       prev_id=prev_id)
    return render_template('pages.html', 
                           this_filename=this_page.filename,
                           next_id=next_id,
                           prev_id=prev_id)

@app.route('/keyword_mapping')
@app.route('/keyword_mapping', methods=['GET','POST'])
def keyword_entry():
    pages=Page.query.all()

    if request.method == 'POST':
        for page in pages:
            print request.form
            page.keyword = request.form[str(page.id)]
            db.session.commit()

            print "KEYWORD= ", page.keyword

    return render_template('keyword_mapping.html', pages=pages)
