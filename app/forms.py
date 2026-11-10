from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Optional, EqualTo, Regexp

CATEGORY_CHOICES = [
    ("", "Select a category"),
    ("electricity", "Electricity / Power"),
    ("plumbing", "Plumbing / Water"),
    ("internet", "Internet / Wi-Fi"),
    ("cleanliness", "Cleanliness / Hygiene"),
    ("furniture", "Furniture / Fixtures"),
    ("security", "Security"),
    ("hostel", "Hostel Facilities"),
    ("canteen", "Canteen / Mess"),
    ("other", "Other"),
]

STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("In Progress", "In Progress"),
    ("Resolved", "Resolved"),
    ("Rejected", "Rejected"),
]

PRIORITY_CHOICES = [
    ("Low", "Low"),
    ("Medium", "Medium"),
    ("High", "High"),
    ("Urgent", "Urgent"),
]


class ComplaintForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email Address", validators=[DataRequired(), Regexp(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", message="Invalid email address."), Length(max=120)])
    phone = StringField("Phone Number", validators=[Optional(), Length(max=20)])
    category = SelectField("Category", choices=CATEGORY_CHOICES, validators=[DataRequired()])
    location = StringField("Location (Hostel / Block / Room)", validators=[DataRequired(), Length(max=120)])
    description = TextAreaField("Describe the Issue", validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField("Submit Complaint")


class TrackForm(FlaskForm):
    complaint_id = StringField("Complaint ID", validators=[DataRequired()], render_kw={"placeholder": "e.g. FMC-2026-A1B2C3"})
    submit = SubmitField("Track Complaint")


class AdminLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class ComplaintUpdateForm(FlaskForm):
    status = SelectField("Status", choices=STATUS_CHOICES, validators=[DataRequired()])
    priority = SelectField("Priority", choices=PRIORITY_CHOICES, validators=[DataRequired()])
    admin_notes = TextAreaField("Admin Notes", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Update Complaint")
