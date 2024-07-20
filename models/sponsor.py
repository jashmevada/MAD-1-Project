from flask import (Blueprint, render_template, session, request, redirect, url_for)
from db.db import db

from models.model import Sponsor, Influence

bp = Blueprint('sponsor', __name__, url_prefix='/sponsor')


@bp.route("/<username>", methods=['GET', 'POST'])
def create_profile(username):
    print(session)
    if request.method == 'POST':
        print("GOT POST REQ")
        print (request.form)

        spn = Sponsor(
            user_id=username,
            full_name=request.form['fullname'],
            email=request.form['email'],
            phone_number=request.form['phone_number'],
            company_name=request.form['company_name'],
            industry=request.form['industry'],
            company_website=request.form['website'],
        )

        create_sponsor(spn)

        return redirect(url_for("common.render_test", active='overview'))

    return render_template("create_profile.html")


@bp.route("/add", methods=['POST'])
def add_sponsor():
    if request.method == "POST":
        pass


def create_sponsor(sponsor: Sponsor):
    try:
        db.session.add(sponsor)
        db.session.commit()
    except Exception as e:
        print(e)


@bp.route('/find', methods=['GET', 'POST'])
def find_influencer():
    infs = Influence.query.all()
    print(infs)

    return render_template("Dashboard/find_inf.html", active_tab="find", infs=infs)
