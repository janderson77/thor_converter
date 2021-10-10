import os
from os.path import basename
from flask import Flask, request, flash, redirect, abort, send_from_directory
from flask.templating import render_template
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import secure_filename
from forms import FileForm
import json
from masterfile_api import convert_masterfile
from novatime_api import convertNT
from pathlib import Path, PurePath
from zipfile import ZipFile


app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

cwd = Path.cwd()
uploads = PurePath(cwd, 'uploads')
app.config['UPLOADS_FOLDER'] = uploads


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def zipFilesInDir(dirName, zipFileName, filter):
    with ZipFile('uploads/Converted.zip', 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(dirName):
            for filename in filenames:
                if filter(filename):
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath, basename(filePath))
                    os.remove(filePath)


@app.route('/', methods=["GET", "POST"])
def show_home_page():
    c = open('clients.json')
    data = json.load(c)
    d = []
    for i in data['Clients']:
        d.append(i['name'])
    form = FileForm()
    form.client.choices = d

    if form.validate_on_submit():
        if 'Converted.zip' in os.listdir(uploads):
            os.remove(f'{uploads}/Converted.zip')
        f = request.files.getlist(form.convertFile.name)
        if form.client.data == 'Papa Pita Bakery':
            for i in f:
                if 'masterfile' in i.filename.lower():
                    convert_masterfile(i)
                if 'twkpr' in i.filename.lower():
                    if 'TWKPR.XLS' in os.listdir(uploads):
                        os.remove(f'{uploads}/TWKPR.XLS')
                    if 'TWKPR.XLSX' in os.listdir(uploads):
                        os.remove(f'{uploads}/TWKPR.XLSX')
                    filename = secure_filename(i.filename)
                    i.save(os.path.join(uploads, filename))
                    convertNT(form.client.data)
        else:
            flash("Not Yet Supported", 'danger')
            return render_template("home.html", form=form)

        zipFilesInDir('uploads', 'downloads', lambda name: 'xlsx' in name)
        try:
            return send_from_directory(app.config['UPLOADS_FOLDER'], 'Converted.zip')
        except:
            abort(404)

    return render_template("home.html", form=form)
