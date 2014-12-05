from . import app
from flask import (render_template,
                   session,
                   redirect,
                   url_for,
                   request,
                   Flask,
                   send_from_directory)
from functools import wraps
import os,md5
from werkzeug import secure_filename
from datetime import timedelta, datetime
from models.usermodel import UserModel
from models.user_objects import *
from werkzeug import secure_filename

def login_required(func):
    """
    wrapper for login
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.has_key('user'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('home'))
    return wrapper

@app.route('/')
def home():
    return render_template('master.html')

@app.route('/wall')
@login_required
def wall():
    model_object = UserModel()
    posts = model_object.get_posts(session["user"]["user_id"])
    return render_template('index.html', fname=session['user']['first_name'], posts=posts)


@app.route('/login', methods=["POST"])
def login():
    fields = users()
    model_object = UserModel()
    fields.email_id = request.form["txtusername"]
    fields.password = request.form["txtuserpassword"]
    if model_object.login(fields):
        return "1"
    return "0"

@app.route('/logout')
def logout():
    if session.has_key('user'):
        session.pop("user")
    return redirect("/")

@app.route('/register', methods=["POST"])
def register():
    fields = users()
    model_object = UserModel()
    fields.first_name = request.form["txtfname"]
    fields.last_name = request.form["txtlname"]
    fields.email_id = request.form["txtemail"]
    fields.password = request.form["txtpassword"]
    model_object.register_user(fields)
    return "text"

@app.route('/postcontent', methods=['POST'])
def postcontent():
    objuser = user_post()
    user = session["user"]
    user_post.user_id = user["user_id"]
    user_post.content = request.form["txtcontent"]
    user_post.title = request.form["txttitle"]
    if request.form["selectvisibility"]:
        user_post.visibility_id = request.form["selectvisibility"]
    if request.files['fileupload']:
        try:
            fileupload = request.files['fileupload']
            if fileupload and allowed_file(fileupload.filename):
                # Make the filename safe, remove unsupported chars
                filename = secure_filename(fileupload.filename)
                ext=filename.split('.')
                filename=secure_filename(user['first_name'] + "_" + str(datetime.now()) + "." + ext[len(ext)-1])
                fileupload.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user_post.upload = filename
        except Exception as ex:
            print str(ex)
    model_object = UserModel()
    model_object.postcontent(objuser)
    posts = []
    post = {
            "first_name" : user["first_name"],
            "last_name" : user["last_name"],
            "title" : user_post.title,
            "posted_when" : user_post.posted_when,
            "content" : user_post.content,
            "upload" : str(user_post.upload)
    }
    print post
    posts.append(post)
    return render_template("posts.html", posts = posts)

def get_file_location(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as ex:
        print ex

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
