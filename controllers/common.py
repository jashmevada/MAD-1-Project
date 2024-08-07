from flask import (Blueprint, render_template, session, redirect, url_for, request)

from db.db import db
from models.model import *

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


class Search:
    def __init__(self):
        pass

    @staticmethod
    def influencers(q:str):
        _query = Influencer.query.filter(
            (Influencer.name.ilike(f'%{q}%')) |
            (Influencer.gender.ilike(f'%{q}%')) |
            (Influencer.niche.ilike(f'%{q}%')) |
            (Influencer.email.ilike(f'%{q}%'))
        ).all()
        return _query

    @staticmethod
    def sponsors(q: str):
        _query = Sponsor.query.filter(
            (Sponsor.full_name.ilike(f'%{q}%')) |
            (Sponsor.email.ilike(f'%{q}%')) |
            (Sponsor.company_name.ilike(f'%{q}%'))
        ).all()
        return _query

    @staticmethod
    def campaigns(q: str):
        _query = Campaign.query.filter(
            (Campaign.title.ilike(f'%{q}%')) |
            (Campaign.description.ilike(f'%{q}%')) |
            (Campaign.budget.ilike(f'%{q}%'))
        ).all()

        return _query
