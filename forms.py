from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import SelectField, MultipleFileField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):
    client = SelectField('Which client?', render_kw={
                         'class': "form-select form-control"}, description="Select a client")
    convertFile = MultipleFileField('One or More Excel Files (.xls, .xlsx)',
                                    validators=[DataRequired(), FileAllowed(['xls', 'xlsx'])], render_kw={'accept': '.xls, .xlsx', 'class': 'form-control'})
