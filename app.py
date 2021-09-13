import os
from flask import Flask, request, flash, redirect
from flask.templating import render_template
from flask_debugtoolbar import DebugToolbarExtension
from forms import FileForm
import json
from masterfile_api import convert_masterfile


app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        f = request.files.getlist(form.convertFile.name)
        for i in f:
            if 'masterfile' in i.filename:
                convert_masterfile(i)
        print(f)
        return redirect('/')
    return render_template("home.html", form=form)
