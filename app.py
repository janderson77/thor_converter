from io import BytesIO
import time
from flask import Flask, request, flash, abort, send_file, jsonify, make_response
from flask.templating import render_template
from flask_cors import CORS
from forms import FileForm
import json
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from masterfile_api import convert_masterfile
from helpers import getRandomPhrase
from novatime_api import convertNT
from nutraceutical import convert_nutra
from pbm import convertPBM
from maximus import convert_maximus

app = Flask(__name__)
CORS(app, expose_headers='Content-Disposition')

# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = 'aognaognag'

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=["POST"])
def process_data():
    print(request.files)
    client = request.form.get('client')
    f = request.files.getlist("file")
    files = []

    if client == 'Papa Pita Bakery':
        for i in f:
            if 'masterfile' in i.filename.lower() or 'master' in i.filename.lower():
                export = convert_masterfile(i)
                for j in export:
                    files.append(j)
            if 'twkpr' in i.filename.lower():
                export = convertNT(i, "Papa Pita")
                files.append(export)
    elif client == 'Novatime':
        for k in f:
            export = convertNT(k)
            files.append(export)
    elif client == "Nutraceutical":
        for k in f:
            export = convert_nutra(k)
            files.append(export)
    elif client == "PBM":
        for k in f:
            export = convertPBM(k)
            files.append(export)
    elif client == "Maximus":
        for k in f:
            if "assignment" in k.filename.lower():
                assignment_register = k
            else:
                payroll_data = k
        export = convert_maximus(payroll_data, assignment_register)
        for e in export:
            files.append(e)

    if len(files) == 0:
        flash("No file uploaded", 'danger')
        return render_template("home.html", form=form)

    elif len(files) == 1:
        if client == "PBM":
            try:
                return send_file(
                    files[0][0],
                    as_attachment=True,
                    download_name=f'{files[0][1]}.xls',
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            except:
                flash("File not processed. Please see Administrator")
                return render_template("home.html", phrase=phrase, form=form)
        else:
            try:
                return send_file(
                    files[0][0],
                    as_attachment=True,
                    download_name=f'{files[0][1]}.xlsx',
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            except:
                flash("File not processed. Please see Administrator")
                return render_template("home.html", phrase=phrase, form=form)

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
            response = make_response(send_file(
                memory_file, 
                as_attachment=True, 
                download_name="Imports.zip",
                attachment_filename='Imports.zip'
                ))
            response.headers['mimetype'] ='application/zip'
            response.content_type = "application/download"
            return response

        except:
            abort(404)
    
    
@app.route('/', methods=["GET"])
def show_home_page():
    c = open('clients.json')
    data = json.load(c)
    d = []
    for i in data['Clients']:
        d.append(i['name'])
    form = FileForm()
    form.client.choices = d
    phrase = getRandomPhrase()

    if form.validate_on_submit():
        f = request.files.getlist(form.convertFile.name)
        files = []
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
        elif form.client.data == "Nutraceutical":
            for k in f:
                export = convert_nutra(k)
                files.append(export)
        elif form.client.data == "PBM":
            for k in f:
                export = convertPBM(k)
                files.append(export)
        elif form.client.data == "Maximus":
            for k in f:
                if "assignment" in k.filename.lower():
                    assignment_register = k
                else:
                    payroll_data = k
            export = convert_maximus(payroll_data, assignment_register)
            for e in export:
                files.append(e)

                
        else:
            flash("Not Yet Supported", 'danger')
            return render_template("home.html", phrase=phrase, form=form)

        # ///////////Start Return Functions///////////
        if len(files) == 0:
            flash("No file uploaded", 'danger')
            return render_template("home.html", form=form)

        elif len(files) == 1:
            if form.client.data == "PBM":
                try:
                    return send_file(
                        files[0][0],
                        as_attachment=True,
                        download_name=f'{files[0][1]}.xls',
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                except:
                    flash("File not processed. Please see Administrator")
                    return render_template("home.html", phrase=phrase, form=form)
            else:
                try:
                    return send_file(
                        files[0][0],
                        as_attachment=True,
                        download_name=f'{files[0][1]}.xlsx',
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                except:
                    flash("File not processed. Please see Administrator")
                    return render_template("home.html", phrase=phrase, form=form)

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
        
    response = jsonify(["this", "returned"])
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.status_code = 200

    return response
