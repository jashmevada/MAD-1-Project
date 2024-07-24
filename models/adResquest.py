from flask import (Blueprint, render_template, session, redirect, url_for, request)

from db.db import db
from models.model import *

bp = Blueprint('ad_request', __name__, url_prefix='/ad_request')


# Utils Functions -----------------------

def get_current_requests() -> list[AdRequest]:


    lst = []
    for i in Campaign.query.filter(Campaign.sponsor_id == Sponsor.query.get(session['username']).user_id).all():
        lst.append(i)

    return [AdRequest.query.filter_by(campaign_id=i.id).all() for i in lst]


def get_ad_for_influencer():
    return AdRequest.query.filter_by(influencer_id=Influencer.query.get({"user_id": session['username']}).user_id).all()


# Routes --------------------------------

@bp.route('/create', methods=['POST'])
def create_ad_request():
    data = AdRequest(
        campaign_id=request.form['camp'],
        influencer_id=session['username'],
        message=request.form['message'],
        payment_amount=request.form['budget'],
    )
    print(data)
    db.session.add(data)
    db.session.commit()
    return render_template("sponsor/find_inf.html", active_tab="find", infs=Influencer.query.all(),
                           cmps=Campaign.query.filter(
                               Campaign.sponsor_id == Sponsor.query.get(session['username']).user_id).all(),
                           ad_req=data)


@bp.route('/')
def index():
    all_reqs = get_current_requests()
    return render_template("sponsor/send_request.html", active_tab="adrequest", reqs=all_reqs)

@bp.route('/influ_req')
def influ_req():
    return render_template("influencer/ad_request.html", active_tab="adrequest", reqs=get_current_requests())