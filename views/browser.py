from . import app
from flask import render_template, session, redirect, url_for, request,Flask,send_from_directory
from functools import wraps
import os,md5
from werkzeug import secure_filename
from datetime import timedelta, datetime


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
def wall():
    return render_template('index.html')
