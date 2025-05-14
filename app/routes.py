from flask import render_template, Blueprint
from app.auth_routes import login_required
from app.share_routes import get_shares_for_user
from flask_wtf.csrf import generate_csrf

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/intro', methods=['GET', 'POST'])
def intro():
    return render_template('intro.html')

@main_bp.route('/homechart', methods=['GET', 'POST'])
@login_required
def homechart():
    return render_template('homechart.html')

@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    return render_template('upload.html', csrf_token=generate_csrf())

@main_bp.route('/share', methods=['GET', 'POST'])
@login_required
def share():
    shares = get_shares_for_user() 
    return render_template('share.html', shares = shares, csrf_token=generate_csrf())




