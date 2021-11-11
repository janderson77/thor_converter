from io import BytesIO
import time
from flask import Flask, request, flash, abort, send_file
from flask.templating import render_template
from forms import FileForm
import json
from masterfile_api import convert_masterfile
from novatime_api import convertNT
from pathlib import Path, PurePath
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED


app = Flask(__name__)

# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = 'aognaognag'

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

cwd = Path.cwd()
path = PurePath(cwd, 'uploads')
uploads = Path(path)

app.config['UPLOADS_FOLDER'] = uploads


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
        files = []
        print(form.client.data)
        if form.client.data == 'Papa Pita Bakery':
            for i in f:
                if 'masterfile' in i.filename.lower() or 'master' in i.filename.lower():
                    export = convert_masterfile(i)
                    for j in export:
                        files.append(j)
                if 'twkpr' in i.filename.lower():
                    export = convertNT(i, "Papa Pita")
                    files.append(export)
        elif form.client.data == 'Novatime':
            for k in f:
                export = convertNT(k)
                files.append(export)
        else:
            flash("Not Yet Supported", 'danger')
            return render_template("home.html", form=form)

        # ///////////Start Return Functions///////////
        if len(files) == 0:
            flash("No file uploaded", 'danger')
            return render_template("home.html", form=form)

        elif len(files) == 1:
            try:
                return send_file(
                    files[0][0],
                    as_attachment=True,
                    download_name=f'{files[0][1]}.xlsx',
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            except:
                abort(404)

        else:
            memory_file = BytesIO()
            with ZipFile(memory_file, 'w') as zf:
                for individualFile in files:
                    data = ZipInfo(f'{individualFile[1]}.xlsx')
                    data.date_time = time.localtime(time.time())[:6]
                    data.compress_type = ZIP_DEFLATED
                    zf.writestr(data, individualFile[0].getvalue())
            memory_file.seek(0)

            try:

                return send_file(memory_file, as_attachment=True, download_name="Imports.zip")

            except:
                abort(404)

    return render_template("home.html", form=form)
