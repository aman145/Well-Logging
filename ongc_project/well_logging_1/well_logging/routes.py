from flask import render_template,flash,url_for,redirect,request
from well_logging.models import upload
from well_logging.forms import uploads
import os
from well_logging.data import data_process
from well_logging import app,db
def save_picture(form_picture):
    f_name,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=f_name + f_ext
    picture_path=os.path.join(app.root_path,'static',picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/",methods=['POST', 'GET'])
@app.route("/home",methods=['POST', 'GET'])
def home():
    form=uploads()
    if form.validate_on_submit():
        if form.las_file_1.data:
            data_file_1=save_picture(form.las_file_1.data)
        if form.las_file_2.data:
            data_file_2=save_picture(form.las_file_2.data)
        if form.las_file_3.data:
            data_file_3=save_picture(form.las_file_3.data)
        recipe=upload(data_file=data_file_1)
        db.session.add(recipe)
        recipe=upload(data_file=data_file_2)
        db.session.add(recipe)
        recipe=upload(data_file=data_file_3)
        db.session.add(recipe)
        db.session.commit()        
        flash('files is added','success')
        return redirect(url_for('about'))

    return render_template("home.html",form=form)

@app.route("/about",methods=['GET', 'POST'])
def about():
    data_process()
    return render_template("about.html")