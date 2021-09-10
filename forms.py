from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class FileForm(FlaskForm):
    convertFile = FileField('Excel file (.xls, .xlsx)',
        validators=[FileRequired(),FileAllowed(['xls', 'xlsx'])],render_kw={'accept': '.xls, .xlsx'})