from flask import render_template
from app import application
from app.auth_routes import login_required
from flask_wtf.csrf import generate_csrf


@application.route('/')
@application.route('/intro', methods=['GET', 'POST'])
def intro():
    return render_template('intro.html')

@application.route('/homechart', methods=['GET', 'POST'])
@login_required
def homechart():
    return render_template('homechart.html')

@application.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    return render_template('upload.html', csrf_token=generate_csrf())

@application.route('/share', methods=['GET', 'POST'])
@login_required
def share():
    return render_template('share.html')




