from flask import (Blueprint, request, session, flash, redirect, url_for, render_template)

from db.db import db
from models.model import User, State

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/login", methods=['GET', 'POST'])
def login():
    print(request.form)
    if request.method == 'POST':
        user_ = User.query.filter_by(email=request.form['Email']).first()
        # print(user_.role)
        if user_ is not None and user_.password == request.form['password']:
            print("Logged in")
            session["username"] = user_.username
            session["role"] = user_.role
            session['active_state'] = State(
                user_id=user_.username,
                role=user_.role
            ).model_dump_json()

            print(session)
            flash("You were successfully logged in")
            return redirect(url_for("dashboard", username=user_.username))
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
            password=request.form['password'],
            email=request.form['email'],
            role=request.form['role'],
        )
        user_ = User.query.filter_by(username=user.username).first()

        if user_ is None:
            db.session.add(user)
            db.session.commit()
            session["username"] = user.username
            session['active_state'] = State(
                user_id=user.username,
                role=user.role
            ).model_dump_json()

        print(type(user_), user_)
        if user.role == 'Influencer':
            session['role'] = 'Influencer'
            return redirect(url_for("influencer.create_profile", username=user.username))
        elif user.role == 'Admin':
            pass
        elif user.role == 'Sponsor':
            session['role'] = 'Sponsor'
            return redirect(url_for("sponsor.create_profile", username=user.username))
        # user = User.query.filter_by(username=username).first()
        # if user and user.check_password(password):

    return render_template("signup.html")
