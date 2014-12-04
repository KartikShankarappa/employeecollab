from . import app
from flask import render_template, session, redirect, url_for, request,Flask,send_from_directory
from functools import wraps
import os,md5
from werkzeug import secure_filename
from datetime import timedelta, datetime
from models.usermodel import UserModel
from models.user_objects import *

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
    return render_template('index.html', fname = session['user']['first_name'])


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