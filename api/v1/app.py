import sys
import os
# Ensure the project root directory is in 'sys.path'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from flask import Flask, render_template, url_for, flash, redirect, session, g, request
from models.user import User
from models import user_store
from api.v1.forms.register_form import RegistrationForm
from api.v1.forms.login_form import LoginForm
from wtforms import ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'createatokenusingsecretpackage'

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # Simplified condition check
        try:
            if form.validate_username(form.username):
                user = User(name=form.username.data, master_pass=form.master_password.data)
                user_store.load()
                user.add()
                user_store.save()
                flash('Registered Successfully', 'success')
                return redirect(url_for('login'))
        except ValidationError as e:  # Included try-except block for ValidationError
            flash(str(e), 'danger')
    else:
        for fieldName, errorMessages in form.errors.items():  # Flashing field-specific errors
            for err in errorMessages:
                flash(err, 'danger')
    return render_template('register.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            if form.validate_user(form):
                session.pop('user', None)
                session['user'] = form.username.data
                flash('Login Successful', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'danger')  # Generic error message
        except Exception as e:  # Catch a more generic exception if unsure
            flash(str(e), 'danger')
    return render_template('login.html', form=form)

@app.route('/home')
def home():
    if g.user:
        return render_template('home.html', user=session['user'])
    return render_template(url_for('login'))

@app.route('/dropsession')
def dropsession():
    """drops a user session and logs out"""
    session.pop('user', None)  # Log out the user
    session.pop('_flashes', None)  # Clear all flashed messages
    return redirect(url_for('login'))

@app.before_request
def before_request():
    """operates before any request is made"""
    g.user = None

    if 'user' in session:
        g.user = session['user']

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
