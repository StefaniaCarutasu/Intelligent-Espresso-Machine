from re import sub
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, AnyOf

from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

import email_validator

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    birth_date = DateField('Birth date')
    submit = SubmitField('Edit profile')

class CoffeeOptionsForm(FlaskForm):
    beverage_type = SelectField('Beverage type', validators=[DataRequired()])
    roast_type = SelectField('Roast type', choices=[('Decaffeinated', 'Decaffeinated'), ('Low', 'Low'), ('Medium', "Medium"), ('High', "High")], validators=[DataRequired()])
    syrup = BooleanField('Add syrup', default=False, validators=[AnyOf([True, False])])
    submit = SubmitField('Start')

class PreferenceForm(CoffeeOptionsForm):
    submit = SubmitField('Set preference')

class ProgrammedCoffeeForm(CoffeeOptionsForm):
    time = TimeField('Time', validators=[DataRequired()])
    submit = SubmitField('Add')

class BloodPressureForm(FlaskForm):
    systolic = IntegerField('Systolic', validators=[DataRequired()])
    diastolic = IntegerField('Diastolic', validators=[DataRequired()])
    submit = SubmitField('Search')

