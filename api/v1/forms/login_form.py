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
                    print(f"User found: {user['name']}")
                    if verify_password(form.master_password.data, user['hash_pw']):
                        print("Password is correct")
                        user_key = f"{user['name']}:{user['user_id']}"
                        print(f"User key: {user_key}")
                        if user_key in user_store.get_users():
                            return user_store.get_users()[user_key]
                        else:
                            print(f"User key {user_key} not found in user store.")
                            return None
                    else:
                        print("Password is incorrect")
        print("User not found or password incorrect")
        return None
