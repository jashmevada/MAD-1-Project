from flask import (Blueprint, request, session, flash, redirect, url_for, render_template)
import re

from db.db import db
from models.model import User
from hashlib import sha512

bp = Blueprint('auth', __name__, url_prefix='/auth')


# Utils -----------------------------------------------

def hash_password(password):
    return sha512(password.encode('utf-8')).hexdigest()


# Routes ----------------------------------------------


@bp.route("/login", methods=['GET', 'POST'])
def login():
    print(request.form)
    if request.method == 'POST':
        session.clear()

        # user_ = User.query.filter_by(email=request.form['Email']).first()

        if re.findall(r'@[a-z]*?\.', request.form['Email']):
            user_ = User.query.filter_by(email=request.form['Email']).first()
        else:
            user_ = User.query.filter_by(username=request.form['Email']).first()

        if user_ is not None and hash_password(request.form['password']) == user_.password:
            print("Logged in")
            session["username"] = user_.username
            session["role"] = user_.role
            print(session)
            flash("You were successfully logged in")
            return redirect(url_for("dashboard", username=user_.username))
        elif user_ is None:
            try:
                user = User.query.filter_by(username=request.form['username']).first()
            except Exception as e:
                pass
        else:
                flash("Invalid Credentials")

            # return redirect(url_for("auth.login"))

    return render_template("login.html")


@bp.route("/signup", methods=['GET', 'POST'])
def signup():
    print(request.form)
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            password=hash_password(request.form['password']),
            email=request.form['email'],
            role=request.form['role'],
        )
        user_ = User.query.filter_by(username=user.username).first()

        if user_ is None and User.query.filter_by(email=request.form['email']).first() is None:
            print("OK added user in DB")
            db.session.add(user)
            db.session.commit()
            session["username"] = user.username
        else:
            return "Hello World!-"
        
        print(type(user_), user_)
        
        if user.role == 'Influencer':
            session['role'] = 'Influencer'
            return redirect(url_for("influencer.create_profile", username=user.username))
        
        elif user.role == 'Admin':
            pass
        
        elif user.role == 'Sponsor':
            session['role'] = 'Sponsor'
            return redirect(url_for("sponsor.create_profile", username=user.username))

    return render_template("signup.html")
