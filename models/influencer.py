from flask import (Blueprint, render_template, session, request, flash, redirect)
from werkzeug.utils import secure_filename
import os

import utils
from db.db import db
from controllers import common
from models import adResquest
from models.model import Influencer, Campaign

bp = Blueprint('influencer', __name__, url_prefix='/influencer')


@bp.route("/<username>", methods=['GET', 'POST'])
def create_profile(username):
    ok = False
    # Campaign.query.filter(Campaign.sponsor_id == Sponsor.query.get(username).user_id).all()
    if request.method == 'POST':
        print(request.form)

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(utils.UPLOAD_FOLDER, filename))

        infl = Influencer(
            user_id=username,
            name=request.form['fullname'],
            email=request.form['email'],  # request.form['email']
            gender=request.form['gender'],
            channel=request.form['link'],
            niche=request.form['niche'],
            image=file.filename
        )
        if create_influencers(infl):
            return common.overview()
        ok = True
        session['image_path'] = file.filename

    return render_template("create_profile.html", ok=ok)


def get_influencers(username: str):
    if username is not None and username != "":
        return Influencer.query.filter(Influencer.username == username).all()
    else:
        return None


def create_influencers(infl: Influencer):
    try:
        db.session.add(infl)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


@bp.route('/overview')
def overview():
    return render_template('influencer/overview.html', active_tab="overview",
                           img=Influencer.query.filter(Influencer.user_id == session['username']).first())


@bp.route('/find')
def find():
    get_public_camps = Campaign.query.filter(Campaign.visibility == 'public').all()
    return render_template("influencer/find_campaigns.html", active_tab="find", public_camps=get_public_camps)


@bp.route('/ad_request')
def ad_request():
    return render_template('influencer/ad_request.html', active_tab="ad_req", reqs=adResquest.get_ad_for_influencer())


@bp.route('/stats')
def stats():
    return render_template('influencer/stats.html', active_tab="stats")


@bp.route('/profile')
def profile():
    return render_template('influencer/profile.html', active_tab="profile")


@bp.route('/send_req', methods=['POST'])
def send_request():
    return """        <div class="blue-tick">
            &#10004;  <!-- Unicode character for checkmark -->
        </div>"""
