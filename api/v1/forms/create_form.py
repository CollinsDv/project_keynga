from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class CreatePlatformForm(FlaskForm):
    """create a form for taking user data for his platforms"""
    platform_name = StringField('Platform Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class GeneratePasswordForm(FlaskForm):
    """generates a form for assisting in password generation"""
    platform_name = StringField('Platform Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Generate Password')
