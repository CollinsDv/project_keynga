from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from models import user_store
from models.generators.hash_generator import verify_password
import json
from models.store.vault import Vault


class LoginForm(FlaskForm):
    """generates a login form"""
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=25)],
                           render_kw={"placeholder": "Username"})
    master_password = PasswordField('Master_Password',
                                    validators=[DataRequired()],
                                    render_kw={
                                        "placeholder": "Master Password"
                                        })
    submit = SubmitField('Login')

    def validate_user(self, form):
        """checks if a user password matches the hash
        Args:
            form (FlaskForm): contains entries from client userform
        Return:
            User object if password matches, else None
        """
        try:
            with open(user_store.file_store, 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            print("User store file not found")
            return None
        else:
            for user in users.values():
                if user['name'] == form.username.data:
                    if verify_password(form.master_password.data,
                                       user['hash_pw']):
                        user['hash_pw'] = user['hash_pw'].encode()
                        user['authenticated'] = True  # for flask login
                        user['vault'] = Vault(user['user_id'],
                                              form.master_password.data,
                                              user['salt'])
                        return user
                    else:
                        return None  # incorrect password
        return None  # Unavailable user
