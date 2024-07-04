import sys
import os
# Ensure the project root directory is in 'sys.path'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from flask import Flask, render_template, url_for, flash, redirect, g, request
from flask import get_flashed_messages
from models.user import User
from models import user_store
from api.v1.forms.register_form import RegistrationForm
from api.v1.forms.login_form import LoginForm
from api.v1.forms.manage_form import ManageForm
from api.v1.forms.create_form import CreatePlatformForm, GeneratePasswordForm
from wtforms import ValidationError
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'createatokenusingsecretpackage'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    for user_key, user_obj in user_store.get_users().items():
        if user_obj.user_id == user_id:
            return user_obj
    return None

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            if form.validate_username(form.username):
                user = User(name=form.username.data, master_pass=form.master_password.data)
                user_store.load()
                user.add()
                user_store.save()
                flash('Registered Successfully', 'success')
                return redirect(url_for('login'))
        except ValidationError as e:
            flash(str(e), 'danger')
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(err, 'danger')
    return render_template('register.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            if form.validate_user(form):
                user = next(user for user in user_store.get_users().values() if user.name == form.username.data)
                login_user(user)
                flash('Login Successful', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'danger')
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('login.html', form=form)

@app.route('/profile')
@login_required
def profile():
    user = current_user
    decrypted_vault = user.vault.decrypt()
    unique_platforms = list(set(platform.split('-')[0] for platform in decrypted_vault.keys()))
    return render_template('profile.html', user=user, vault=decrypted_vault, unique_platforms=unique_platforms)


@app.route('/home')
@login_required
def home():
    user = current_user
    return render_template('home.html', user=user)

@app.route('/dropsession')
def dropsession():
    clear_flashes()
    flash("You have been logged out.", "info")
    logout_user()
    return redirect(url_for('login'))

def clear_flashes():
    # Retrieve and discard all flash messages
    get_flashed_messages()

@app.before_request
def before_request():
    g.user = current_user

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreatePlatformForm()
    gen_form = GeneratePasswordForm()
    if form.validate_on_submit():
        user = current_user
        user.vault.add_platform(form.platform_name.data, form.username.data, form.password.data)
        user.vault.save_platforms()
        flash('Platform added successfully', 'success')
        return redirect(url_for('create'))
    return render_template('create.html', form=form, gen_form=gen_form)

@app.route('/generate_password', methods=['POST'])
@login_required
def generate_password():
    gen_form = GeneratePasswordForm()
    if gen_form.validate_on_submit():
        user = current_user
        user.vault.generate_password(gen_form.platform_name.data, gen_form.username.data)
        user.vault.save_platforms()
        flash('Password generated successfully', 'success')
    return redirect(url_for('create'))

@app.route('/platforms')
@login_required
def platforms():
    user = current_user
    decrypted_vault = user.vault.decrypt()
    return render_template('platforms.html', vault=decrypted_vault)

@app.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    form = ManageForm()
    user = current_user
    decrypted_vault = user.vault.decrypt()
    if form.validate_on_submit():
        user.vault.add_platform(form.platform_name.data, form.username.data, form.password.data)
        user.vault.save_platforms()
        flash('Platform updated successfully', 'success')
        return redirect(url_for('manage'))
    return render_template('manage.html', form=form, vault=decrypted_vault)

@app.route('/delete_platform', methods=['POST'])
@login_required
def delete_platform():
    platform_name = request.form.get('platform_name')
    username = request.form.get('username')
    user = current_user
    user.vault.delete_platform(platform_name, username)
    user.vault.save_platforms()
    flash('Platform deleted successfully', 'success')
    return redirect(url_for('manage'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
