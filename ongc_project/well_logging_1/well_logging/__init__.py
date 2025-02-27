from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

app=Flask(__name__)
app.config['SECRET_KEY']=secrets.token_hex(12)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

from well_logging import routes 