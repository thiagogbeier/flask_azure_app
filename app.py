import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email
import msal
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# MSAL configuration
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TENANT_ID = os.getenv('TENANT_ID')
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "/getAToken"
SCOPE = ["User.Read"]
SESSION_KEY = "msal_token_cache"
class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    notes = TextAreaField('Notes', validators=[DataRequired()])
    image = FileField('Image')
@app.route('/')
def index():
    if not session.get(SESSION_KEY):
        return redirect(url_for('login'))
    return render_template('form.html', form=MyForm())
@app.route('/login')
def login():
    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
        token_cache=msal.SerializableTokenCache())
    auth_url = msal_app.get_authorization_request_url(SCOPE, redirect_uri=url_for('getAToken', _external=True))
    return redirect(auth_url)
@app.route(REDIRECT_PATH)
def getAToken():
    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
        token_cache=msal.SerializableTokenCache())
    token_response = msal_app.acquire_token_by_authorization_code(
        request.args['code'], scopes=SCOPE, redirect_uri=url_for('getAToken', _external=True))
    session[SESSION_KEY] = token_response
    return redirect(url_for('index'))
@app.route('/submit', methods=['POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        image = form.image.data
        image.save(os.path.join('static/uploads', image.filename))
        return 'Form submitted successfully!'
    return render_template('form.html', form=form)
if __name__ == '__main__':
    app.run(debug=True)
