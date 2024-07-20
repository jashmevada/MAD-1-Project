from flask import (Blueprint, render_template, session, redirect, url_for, request)

from db.db import db
from models.model import Role

bp = Blueprint('common', __name__, url_prefix='/')


@bp.route('/overview/', methods=['GET', 'POST'])
def render_test(role: Role):
    if request.method == 'POST':
        print("GOT POST request")
    print(role)
    if role == Role.ADMIN:
        return render_template("Dashboard/overview.html", active_tab="overview", role=role.ADMIN.name)
    elif role == Role.INFLUENCER:
        return render_template("Dashboard/overview.html", active_tab="overview", role=role.INFLUENCER.name)
    elif role == Role.SPONSOR:
        return render_template("Dashboard/overview.html", active_tab="overview", role=role.SPONSOR)
    # else:
    #     return redirect("/auth/login")
