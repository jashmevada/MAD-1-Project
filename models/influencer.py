from flask import (Blueprint, render_template, session, request, flash, redirect, render_template_string)
from werkzeug.utils import secure_filename
import os

import utils

from controllers import common
from models import adResquest
from models.model import *

bp = Blueprint('influencer', __name__, url_prefix='/influencer')

search_data = common.Search()


@bp.route("/<username>", methods=['GET', 'POST'])
def create_profile(username):
    ok = False
    # Campaign.query.filter(Campaign.sponsor_id == Sponsor.query.get(username).user_id).all()
    if request.method == 'POST':
        print(request.form)

        image_name = ''

        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and utils.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_name = filename
            file.save(os.path.join(utils.UPLOAD_FOLDER, filename))

        infl = Influencer(
            user_id=username,
            name=request.form['fullname'],
            email=request.form['email'],  # request.form['email']
            gender=request.form['gender'],
            channel=request.form['link'],
            niche=request.form['niche'],
            image=image_name
        )

        if create_influencers(infl):
            return common.overview()
        else:
            User.query.filter(User.id == session['username']).delete()
            db.session.commit()
            return redirect('/auth/login')

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
                           user=Influencer.query.filter(Influencer.user_id == session['username']).first())


@bp.route('/find', methods=['GET'])
def find():
    get_public_camps = Campaign.query.filter(Campaign.visibility == 'public').all()
    return render_template("influencer/find_campaigns.html", active_tab="find", public_camps=get_public_camps)


@bp.route('/ad_request')
def ad_request():
    req = adResquest.get_ad_for_influencer(session['username'])
    print(req)
    # print(req[0].sponsor_id)
    send_data = {
        'sponsor_names': [Sponsor.query.get_or_404(req[i].sponsor_id).full_name for i in range(len(req))],
        'campaign_title': [req[i].campaign.title for i in range(len(req))],
        'message': [i.message for i in req],
        'description': [req[i].campaign.description for i in range(len(req))],
        'budget_of_campaign': [req[i].campaign.budget for i in range(len(req))],
        'budget_from_sponsor': [i.payment_amount for i in req],
        'status': [i.status for i in req],
        'campaign_id': [req[i].campaign.id for i in range(len(req))],
    }
    print(send_data)
    return render_template('influencer/ad_request.html', active_tab="adrequest", data=send_data)


@bp.route('/stats')
def stats():
    return render_template('influencer/stats.html', active_tab="stats")


@bp.route('/profile')
def profile():
    return render_template('influencer/profile.html', active_tab="profile",
                           influencer=Influencer.query.get(session['username']))


@bp.route('/profile/edit', methods=['GET', 'PUT'])
def edit_profile():
    if request.method == 'PUT':
        print(request.form)

    return render_template('influencer/profile_edit.html', active_tab='profile',
                           influencer=Influencer.query.get(session['username']))


@bp.route('/send_req/<int:campaign_id>', methods=['POST'])
def send_request(campaign_id):
    return """        <div class="blue-tick">
            &#10004;  <!-- Unicode character for checkmark -->
        </div>"""


@bp.route("/active_req/<int:campaign_id>", methods=['POST'])
def active_req(campaign_id):
    req = adResquest.get_ad_for_influencer(session['username'])
    get_status = request.args['status']
    set_status = ''

    if get_status == 'accept':
        set_status = 'active'
    elif get_status == 'reject':
        set_status = 'reject'

    for i in range(len(req)):
        if req[i].campaign_id == campaign_id:
            print(req[i])
            req[i].status = set_status
            db.session.commit()
    if set_status == 'active':
        return """<div class="blue-tick">&#10004;</div>"""
    else:
        return """<div class="red-tick" >&#10004;</div>"""


@bp.route("/view")
def view():
    _id = request.args.get('id')
    _sponsor_id = request.args.get('sp_id')
    sp = Sponsor.query.get_or_404(_sponsor_id)
    c = Campaign.query.get_or_404(_id)
    return render_template('influencer/viewCamps.html', camp=c, spnr=sp)


@bp.route("/in_request")
def in_request():
    return render_template('influencer/send_adrequest.html', active_tab='in_req')


@bp.route("/act_req")
def all_active_requests():
    get_all_act_req = AdRequest.query.filter_by(influencer_id=session.get('username'), status='active').all()
    return render_template('influencer/active_req.html', reqs=get_all_act_req, active_tab="active_req")


@bp.route("/send_req")
def send_ad_request():
    pass


@bp.route("/q_camp", methods=['POST'])
def search_campaign():
    q = request.form.get('search')
    query = search_data.campaigns(q)
    data = \
        """
            {% for cmp in public_camps %}
                <tr>
                    <td>{{ cmp.title }}</td>
                    <td>{{ cmp.budget }}</td>
                    <td>{{ cmp.start_date }}</td>
                    <td>{{ cmp.end_date }}</td>
                    <td>
                        <button class="btn btn-primary" hx-get="/influencer/view?id={{ cmp.id }}&sp_id={{ cmp.sponsor_id }}"
                                hx-trigger="click" hx-target="#content">View
                        </button>
                    </td>
                    <td>
                        <button id="req-btn" class="btn btn-sm" style="background-color: var(--accent)"
                        data-bs-target="#exampleModalToggle" data-bs-toggle="modal" onclick="data_arr = ['{{cmp.id}}','{{cmp.sponsor_id}}']">
                            Send Request
                        </button>
                    </td>
                </tr>
            {% endfor %}
        """

    return render_template_string(data, public_camps=query)
