from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    biddername = StringField('Bidder Name', validators=[DataRequired()])
    password = PasswordField('Bidder ID', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')