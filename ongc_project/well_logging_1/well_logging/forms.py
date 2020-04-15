from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField,FileAllowed

class uploads(FlaskForm):
    las_file_1=FileField('Update Las File',validators=[FileAllowed(['las'])])
    las_file_2=FileField('Update Las File',validators=[FileAllowed(['las'])])
    las_file_3=FileField('Update Las File',validators=[FileAllowed(['las'])])
    submit=SubmitField('Submit')