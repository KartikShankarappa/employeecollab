from . import app
from flask import render_template, session, redirect, url_for, request,Flask,send_from_directory
from functools import wraps
import os,md5
from werkzeug import secure_filename
from datetime import timedelta, datetime

signupStatus={'activate':'Please check your email and activate your account!','success':'Your account is activated!','invalid':'Invalid key','inactive':'Your account is not activated! Please activate using the link sent to your email!','incorrect':'Invalid credentials!','exist':'You are already registered. Please check your email now to activate!','false':'Email already been registered!','0':'Invalid Key/Email. Please use the correct url sent to your email.','1':'Password Updated!'}

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
    return render_template('home.html')
