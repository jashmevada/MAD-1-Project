from flask import (Blueprint, render_template, session, redirect, url_for, request)
from datetime import datetime

from db.db import db
from models.model import Campaign, Sponsor

bp = Blueprint('campaigns', __name__, url_prefix='/campaigns')


@bp.route("/get")
def get_campaigns():
    campaigns = Campaign.query.all()
    print(campaigns)
    return campaigns


@bp.route('/add', methods=['GET', 'POST'])
def add_campaign(campaign: Campaign):
    if (campaign.title.isascii() and campaign.description.isascii()
        and type(campaign.start_date)) == datetime:

        db.session.add(campaign)
        db.session.commit()
    else:
        raise "Not a valid campaign"


@bp.route('/', methods=['GET', 'POST'])
def render_campaigns():
    session['tab'] = "campaigns"
    if request.method == 'POST':
        print("GOT POST request")

    return redirect(url_for("dashboard", username=session['username']))


@bp.route('/test', methods=['GET', 'POST'])
def render_test():
    print(session)
    date_format = "%Y-%m-%d"
    if request.method == 'POST':
        # sponsor = Sponsor.query.filter(Sponsor.user_id == session['username']).all()
        sponsor = Sponsor.query.get_or_404(session['username'])
        print(request.form, sponsor)
        print("GOT POST request")
        camp = Campaign(
            title=request.form['title'],
            description=request.form['description'],
            budget=int(request.form['budget']),
            start_date=datetime.strptime(request.form['start_date'], date_format),
            end_date=datetime.strptime(request.form['end_date'], date_format),
            sponsor_id=session['username'],
        )
        sponsor.active_campaigns += 1
        add_campaign(camp)

        return render_template("Dashboard/campaigns.html", active_tab="campaigns", cmps=get_campaigns())

    return render_template("Dashboard/campaigns.html", active_tab="campaigns", cmps=get_campaigns())


# session["get_campaigns"] = get_campaigns

