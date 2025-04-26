from flask import render_template
from app import application


@application.route('/')
@application.route('/intro', methods=['GET', 'POST'])
def intro():
    return render_template('intro.html')


# @application.route('/login', methods=['GET', 'POST'])
# def login():
#     return render_template('login.html')


# @application.route('/register', methods=['GET', 'POST'])
# def register():
#     return render_template('register.html')

