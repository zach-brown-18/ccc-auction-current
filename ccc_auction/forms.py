from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    biddername = StringField('Bidder Name', validators=[DataRequired()])
    password = PasswordField('Bidder ID', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PlaceBid(FlaskForm):    
    # change to int to match new 'models' schema
    # choose id as int or string
    def set_item_id(self, id):
        self.item_id = id
    
    item_id = None
    submit = SubmitField('Place Bid')