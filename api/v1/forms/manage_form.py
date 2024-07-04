from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class ManageForm(FlaskForm):
    platform_name = StringField('Platform Name', validators=[DataRequired(), Length(min=1, max=100)], render_kw={"placeholder": "Platform"})
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=100)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[Length(max=100)], render_kw={"placeholder": "New Password"})
    submit = SubmitField('Submit')
