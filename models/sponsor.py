from flask import (Blueprint, render_template, session, request)

from models.model import *
import controllers.common as common
from models.campaign import get_campaigns

bp = Blueprint('sponsor', __name__, url_prefix='/sponsor')

search_data = common.Search()


@bp.route("/<username>", methods=['GET', 'POST'])
def create_profile(username):

    if request.method == 'POST':
        print("GOT POST REQ")
        print(request.form)

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
        return common.overview()

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
    infs = Influencer.query.all()
    print(infs)
    return render_template("sponsor/find_inf.html", active_tab="find", infs=infs, cmps=Campaign.query.filter(Campaign.sponsor_id == Sponsor.query.get(session['username']).user_id).all())


@bp.route("/overview", methods=['GET'])
def overview():
    return render_template("sponsor/overview.html", active_tab="overview", role='sponsor', user=Sponsor.query.get(session['username']))


@bp.route('/stats')
def stats():
    return render_template("sponsor/stats.html", active_tab="stats", cmps=get_campaigns(session['username']))
