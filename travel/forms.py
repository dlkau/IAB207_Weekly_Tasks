from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg'}

class DestinationForm(FlaskForm):
  name = StringField('Country', validators=[InputRequired()])
  # adding two validators, one to ensure input is entered and other to check if the 
  # description meets the length requirements
  description = TextAreaField('Description', validators = [InputRequired()])
  image = FileField('Destination Image', validators=[FileRequired(message="Destination Image must be provided"),
                                                    FileAllowed(ALLOWED_FILE, message="Only PNG and JPG files are accepted")])
  currency = StringField('Currency', validators=[InputRequired()])
  submit = SubmitField("Create")
    
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')

class LoginForm(FlaskForm):
  user_name = StringField("User Name", validators=[InputRequired("Enter user name")])
  password = PasswordField("Password", validators=[InputRequired("Enter user password")])
  submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")

