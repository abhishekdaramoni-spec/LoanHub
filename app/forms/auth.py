from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import re

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters.")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    address = TextAreaField('Residential Address', validators=[Length(max=500)])
    submit = SubmitField('Register')

    def validate_phone(self, phone):
        if not re.match(r'^\+?[0-9]{10,15}$', phone.data):
            raise ValidationError('Invalid phone number. Please enter 10 to 15 digits.')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Password Reset Link')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Reset Password')

class ProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    address = TextAreaField('Residential Address', validators=[Length(max=500)])
    photo = FileField('Update Profile Photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Save Profile')
