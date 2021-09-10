from flask import Flask
from flask.templating import render_template
from flask_debugtoolbar import DebugToolbarExtension
from forms import FileForm

app = Flask(__name__)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def show_home_page():
    form = FileForm()
    return render_template("home.html", form=form)