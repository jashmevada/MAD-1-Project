from flask import (Blueprint, render_template, session, request, url_for, redirect)

from models.model import Influence, Role
from models.common import render_test
bp = Blueprint('influencer', __name__, url_prefix='/influencer')


@bp.route("/<username>", methods=['GET', 'POST'])
def create_profile(username):
    if request.method == 'POST':
        return render_test(Role.INFLUENCER)
    return render_template("create_profile.html")


def get_influencers(username: str):
    if username is not None and username != "":
        return Influence.query.filter(Influence.username == username).all()
    else:
        return None


# session['get_influencers'] = get_influencers
