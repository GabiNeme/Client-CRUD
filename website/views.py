from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home/clients.html')


@views.route('/icons.html')
def icons():
    return render_template('home/icons.html')

@views.route('/profile.html')
def profile():
    return render_template('home/client-edit.html')