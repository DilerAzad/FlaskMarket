from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length, Email, DataRequired, EqualTo, ValidationError
from market.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_cheak):
        user = User.query.filter_by(username = username_to_cheak.data).first()
        if user:
            raise ValidationError("Username alredy exists! Please use different one..")

    def validate_email_address(self, email_address_to_cheak):
        mail = User.query.filter_by(email_address = email_address_to_cheak.data).first()
        if mail:
            raise ValidationError("Email Address already exists! Please use another one..")

    
    username = StringField(label = "User Name:", validators=[Length(min=3, max=30), DataRequired()])
    email_address = StringField(label="Email Address:", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password:", validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label="Confirm Password:", validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label="Create Account")

class LoginForm(FlaskForm):

    username = StringField(label='User Name:', validators=[Length(max=30, min=3), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=8), DataRequired()])
    submit = SubmitField(label="Sign in") 

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase Item!") 

class SellItemForm(FlaskForm):
    submit = SubmitField(label="Sell Item!") 


