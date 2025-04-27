from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import BooleanField, HiddenField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class UploadArticleForm(FlaskForm):
    #files = FileField('Upload Files', validators=[FileRequired()], render_kw={'multiple': True})
    primary_category = StringField("Enter Article Category: ", validators=[DataRequired()])
    primary_sub_category = StringField("Enter Sub-Category: ")
    files = FileField('Upload Files', render_kw={'multiple': True})
    #status = HiddenField('Status', validators=[DataRequired()])
    status = HiddenField('Status')
    submit_draft = SubmitField(label="Upload Draft")
    publish = SubmitField(label="Publish")
