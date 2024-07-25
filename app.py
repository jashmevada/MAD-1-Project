from flask import Flask, render_template, request, redirect, session
from flask_migrate import Migrate
from flask_restful import Api

from db.db import db
from models import (campaign, influencer, sponsor, adResquest)
from controllers import auth
from controllers import common
import utils

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test5.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = utils.UPLOAD_FOLDER

db.init_app(app)
api = Api(app)

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
        return common.overview()
    else:
        # g.username = username
        return redirect("/auth/login")


@app.route("/login_post", methods=['POST'])
def req_form_data(form):
    pass


@app.route('/logout')
def logout():
    print(session)
    session.clear()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


app.register_blueprint(auth.bp)
app.register_blueprint(influencer.bp)
app.register_blueprint(sponsor.bp)
app.register_blueprint(campaign.bp)
app.register_blueprint(common.bp)
app.register_blueprint(adResquest.bp)

if __name__ == '__main__':
    app.run()  # debug=True
