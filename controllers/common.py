from flask import (Blueprint, render_template, session, redirect, url_for, request)

from db.db import db
from models.model import Role

bp = Blueprint('common', __name__, url_prefix='/')


@bp.route('/dashboard/overview')
def overview():
    role = session.get('role')
    if role is not None:
        if role == 'Sponsor':
            return redirect(url_for('sponsor.overview'))
        elif role == 'Admin':
            return redirect(url_for('admin.overview'))
        elif role == 'Influencer':
            return redirect(url_for('influencer.overview'))


@bp.route('/profile')
def profile():
    role = session.get('role')
    if role is not None:
        if role == 'Sponsor':
            return redirect(url_for('sponsor.profile'))
        elif role == 'Admin':
            return redirect(url_for('admin.profile'))
        elif role == 'Influencer':
            return redirect(url_for('influencer.profile'))
