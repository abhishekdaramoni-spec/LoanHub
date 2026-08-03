from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, DateField, DecimalField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError
import re

class LoanApplicationForm(FlaskForm):
    full_name = StringField('Full Name (as in PAN)', validators=[DataRequired(), Length(min=2, max=100)])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    address = TextAreaField('Current Address', validators=[DataRequired(), Length(max=500)])
    
    # Financial details
    occupation = SelectField('Occupation Type', choices=[
        ('', 'Select Occupation'), 
        ('Salaried', 'Salaried'), 
        ('Self Employed Business', 'Self Employed (Business)'), 
        ('Self Employed Professional', 'Self Employed (Professional)'), 
        ('Agriculture', 'Agriculture'), 
        ('Retired', 'Retired'), 
        ('Student', 'Student')
    ], validators=[DataRequired()])
    employer = StringField('Employer Name / Business Name', validators=[DataRequired(), Length(max=150)])
    monthly_income = DecimalField('Net Monthly Income (INR)', validators=[DataRequired(), NumberRange(min=1000, message="Income must be at least 1000.")])
    
    # Loan request details
    loan_type = SelectField('Loan Type', coerce=int, validators=[DataRequired()])
    loan_amount = DecimalField('Required Loan Amount (INR)', validators=[DataRequired(), NumberRange(min=1000, message="Loan amount must be at least 1000.")])
    tenure_months = IntegerField('Tenure (in Months)', validators=[DataRequired(), NumberRange(min=1, message="Tenure must be at least 1 month.")])
    
    # KYCs
    pan_number = StringField('PAN Card Number', validators=[DataRequired(), Length(min=10, max=10)])
    aadhar_number = StringField('Aadhar Card Number (12 Digits)', validators=[DataRequired(), Length(min=12, max=12)])
    
    # Documents
    pan_doc = FileField('Upload PAN Card (PDF/Image)', validators=[FileRequired(), FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDF or Images only (max 10MB)')])
    aadhar_doc = FileField('Upload Aadhar Card (PDF/Image)', validators=[FileRequired(), FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDF or Images only (max 10MB)')])
    salary_slip_doc = FileField('Upload Last 3 Months Salary Slip (PDF/Image)', validators=[FileRequired(), FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDF or Images only (max 10MB)')])
    bank_statement_doc = FileField('Upload Last 6 Months Bank Statement (PDF/Image)', validators=[FileRequired(), FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDF or Images only (max 10MB)')])
    
    submit = SubmitField('Submit Loan Application')

    def validate_pan_number(self, pan_number):
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', pan_number.data):
            raise ValidationError('Invalid PAN Format. Must be 5 uppercase letters, 4 digits, 1 uppercase letter.')

    def validate_aadhar_number(self, aadhar_number):
        if not re.match(r'^[0-9]{12}$', aadhar_number.data):
            raise ValidationError('Invalid Aadhar Card Number. Must be exactly 12 digits.')
