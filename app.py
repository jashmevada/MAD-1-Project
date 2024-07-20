from flask import Flask, render_template, g, request, redirect, url_for, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from db.db import db
from models import auth, influencer, sponsor, campaign, common
from models.model import User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return render_template("test.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/dashboard/<username>", methods=['GET', 'POST'])
def dashboard(username):
    if request.method == "POST":
        print("Not Right")

    if session.get("username") == username:
        g.username = session['username']
        return render_template("layouts/dashboard_layout.html")  # dashboard.html
    else:
        # g.username = username
        return redirect("/auth/login")


@app.route("/profile/<username>")
def profile(username):
    return render_template("profile.html")


@auth.bp.route("/signup", methods=['GET', 'POST'])
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
            # db.session.commit()
            session["username"] = user.username

        print(type(user_), user_)
        # db.session.add(user)
        # db.session.commit()
        if user.role == 'Influencer':
            session['role'] = 'influencer'
            return redirect(url_for("influencer.create_profile", username=user.username))
        elif user.role == 'Admin':
            pass
        elif user.role == 'Sponsor':
            session['role'] = 'sponsor'
            return redirect(url_for("sponsor.create_profile", username=user.username))
        # user = User.query.filter_by(username=username).first()
        # if user and user.check_password(password):

    return render_template("signup.html")


@auth.bp.route("/login", methods=['GET', 'POST'])
def login():
    print(request.form)
    if request.method == 'POST':
        user_ = User.query.filter_by(email=request.form['Email']).first()
        print(user_)
        if user_ is not None and user_.password == request.form['password']:
            print("Logged in")
            session["username"] = user_.username
            return redirect(url_for("dashboard", username=user_.username))

    return render_template("login.html")


@app.route("/campaigns/create", methods=['GET', 'POST'])
def campaigns():
    if request.method == "POST":
        pass


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


app.register_blueprint(auth.bp)
app.register_blueprint(influencer.bp)
app.register_blueprint(sponsor.bp)
app.register_blueprint(campaign.bp)
app.register_blueprint(common.bp)

if __name__ == '__main__':
    app.run(debug=True)
