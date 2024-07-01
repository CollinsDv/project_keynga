from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from models import user_store
from models.generators.hash_generator import verify_password
import json

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)], render_kw={"placeholder": "Username"})
    master_password = PasswordField('Master_Password', validators=[DataRequired()], render_kw={"placeholder": "Master Password"})
    submit = SubmitField('Login')

    def validate_user(self, form):
        """checks if a user password matches the hash
        Args:
            Form (flaskform) - contains entries from client userform
        Return:
            bool - True if password matches, else false
        """
        try:
            with open(user_store.file_store, 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            return False
        else:
            for user in users.values():
                if user['name'] == form.username.data:
                    return verify_password(form.master_password.data, user['hash_pw'])
