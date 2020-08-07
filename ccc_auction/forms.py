from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    biddername = StringField('Bidder Name', validators=[DataRequired()])
    password = PasswordField('Bidder ID', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PlaceBid(FlaskForm):    
    def set_item_id(self, id):
        self.item_id = str(id)
    
    item_id = ''
    submit = SubmitField('Place Bid')