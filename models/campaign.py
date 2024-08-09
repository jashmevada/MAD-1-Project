from flask import (Blueprint, render_template, session, redirect, url_for, request, render_template_string)
from datetime import datetime

from db.db import db
from models.model import Campaign, Sponsor
from controllers import common

bp = Blueprint('campaigns', __name__, url_prefix='/campaigns')

search_data = common.Search()


def get_campaigns(username):
    campagings = Campaign.query.filter(Campaign.sponsor_id == Sponsor.query.get(username).user_id).all()

    return campagings


def add_campaign(campaign: Campaign):
    if (campaign.title.isascii() and campaign.description.isascii() and type(campaign.start_date)) == datetime:

        db.session.add(campaign)
        db.session.commit()
    else:
        raise "Not a valid campaign"


@bp.route('/t', methods=['GET', 'POST'])
def render_campaigns():
    return render_template("Dashboard/campaigns.html", active_tab="campaigns", cmps=get_campaigns(session['username']))


@bp.route('/', methods=['GET', 'POST'])  # create
def camp_index():
    print(session)
    date_format = "%Y-%m-%d"
    if request.method == 'POST':
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

        return render_template("Dashboard/campaigns.html", active_tab="campaigns",
                               cmps=get_campaigns(session['username']))

    return render_template("Dashboard/campaigns.html", active_tab="campaigns", cmps=get_campaigns(session['username']))


@bp.route('/viewCampaign/<int:id>/<username>', methods=['GET', 'POST'])
def view_campaign(id, username):
    campaign = Campaign.query.get_or_404(id)
    return render_template("sponsor/viewCampaign.html", camp=campaign)

