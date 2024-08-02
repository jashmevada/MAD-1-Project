from flask import (Blueprint, render_template, redirect, url_for, request, session)

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/overview')
def overview():
    return render_template('admin/overview.html', active_tab="overview")