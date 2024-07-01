from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
from models import user_store
import json

class RegistrationForm(FlaskForm):
    username = StringField('Username', [Length(min=4, max=25)])
    master_password = PasswordField('New Password', [
        DataRequired(), EqualTo('confirm', message="Passwords must match")
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')
    # accept_tos = BooleanField('I accept the TOS', [DataRequired()])

    def validate_username(self, username):
        """Check if the username already exists"""
        print(user_store.get_users())
        for user in user_store.get_users().values():
            if user.name == username.data:
                raise ValidationError('Username already exists')
        return True
