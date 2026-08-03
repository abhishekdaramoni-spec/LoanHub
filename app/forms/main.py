from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Length(max=15)])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=150)])
    message = TextAreaField('Your Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

class InterestRateForm(FlaskForm):
    loan_type_id = SelectField('Loan Type', coerce=int, validators=[DataRequired()])
    tenure_months = IntegerField('Tenure (Months)', validators=[DataRequired(), NumberRange(min=1)])
    rate_pct = DecimalField('Interest Rate (% p.a.)', validators=[DataRequired(), NumberRange(min=1, max=30)])
    status = SelectField('Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')
    submit = SubmitField('Save Interest Rate')
