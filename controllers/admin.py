from flask import (Blueprint, render_template, redirect, url_for, request, render_template_string)

from models.model import *
from controllers import common

bp = Blueprint('admin', __name__, url_prefix='/admin')

search_data = common.Search()


@bp.route('/overview')
def overview():
    return render_template('admin/overview.html', active_tab="overview")


@bp.route('/profile')
def profile():
    return render_template('admin/profile.html', active_tab="profile")


@bp.route('/campaigns')
def campaigns():
    all_campaigns = Campaign.query.all()
    return render_template('admin/campaigns.html', public_camps=all_campaigns, active_tab="campaigns")


@bp.route('/sponsors')
def all_sponsor_details():
    all_sponsor = Sponsor.query.all()
    return render_template('admin/sponsors.html', spns=all_sponsor, active_tab="sponsors")


@bp.route('/influencers')
def all_influencers_details():
    all_influencers = Influencer.query.all()
    return render_template('admin/influencers.html', influencers=all_influencers, active_tab="influ")


def stats():
    pass


@bp.route('/q_influ', methods=['POST'])
def search_influencers():
    q = request.form['search']
    _query = search_data.influencers(q)

    data = \
        """
        {% for influ in influencers %}
            <tr>
                <td style="text-align: left">
                    <div class="d-flex align-items-center">
                        <img
                                {% if influ.image != '' %}
                                    src="{{ url_for('static', filename='/uploads/' + influ.image) }}"
                                {% else %}
                                    src="https://mdbootstrap.com/img/new/avatars/8.jpg"
                                {% endif %}
                                    alt=""
                                    style="width: 45px; height: 45px"
                                    class="rounded-circle"
                        />
                        <div class="ms-3">
                            <p class="fw-bold mb-1">{{ influ.name }}  </p>
                            <p class="text-muted mb-0">{{ influ.email }} @{{ influ.user_id }}</p>
                        </div>
                    </div>
                </td>
                <td>{{ influ.niche }}</td>
                <td>{{ influ.channel }}</td>
                <td>
                    <button class="btn btn-primary"
                            hx-get="/influencer/view?id={{ influ.id }}&sp_id={{ influ.sponsor_id }}"
                            hx-trigger="click" hx-target="#content">View
                    </button>
                </td>
            </tr>
        {% endfor %}
    """
    return render_template_string(data, influencers=_query)


@bp.route('/q_camp', methods=['POST'])
def search_campaigns():
    q = request.form['search']
    _query = search_data.campaigns(q)

    data = """
            {% for cmp in public_camps %}
                <tr>
                    <td>{{ cmp.title }}</td>
                    <td>{{ cmp.budget }}</td>
                    <td>{{ cmp.start_date }}</td>
                    <td>{{ cmp.end_date }}</td>
                    <td>
                        <button class="btn btn-primary"
                                hx-get="/influencer/view?id={{ cmp.id }}&sp_id={{ cmp.sponsor_id }}"
                                hx-trigger="click" hx-target="#content">View
                        </button>
                    </td>
                </tr>
            {% endfor %}"""

    return render_template_string(data, public_camps=_query)


@bp.route('/q_sponr', methods=['POST'])
def searches():
    q = request.form['search']
    _query = search_data.sponsors(q)
    return render_template('sponsor/searches.html', spns=_query)


@bp.route('/stats')
def stats():
    # data: active ad request, campiangs ,
    # no. of infl, spono.

    data = {
        'Count of Influencer': Influencer.query.count(),
        'Count of Sponsors': Sponsor.query.count(),
        'Count of Campaigns': Campaign.query.count(),
        'Total Ad Request Running': AdRequest.query.count()
    }

    return render_template('admin/stats.html', active_tab="stats", data=data)
