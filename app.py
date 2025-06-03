from dotenv import load_dotenv
load_dotenv()

import os
import json
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import msal

# Load secrets from .env
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TENANT_ID = os.getenv('TENANT_ID')
REDIRECT_PATH = "/getAToken"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["User.Read"]
SESSION_KEY = "msal_token_cache"

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "super-secret-key")
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Force HTTPS when behind Azure reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.before_request
def enforce_https_in_url_for():
    if request.headers.get('X-Forwarded-Proto') == 'https':
        request.environ['wsgi.url_scheme'] = 'https'

# Upload directory
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Form definition
class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    notes = TextAreaField('Notes', validators=[DataRequired()])
    image = FileField('Image')

# Home page (form)
@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if not session.get(SESSION_KEY):
        return redirect(url_for('login'))

    if request.method == 'POST':
        if form.validate_on_submit():
            image = form.image.data
            if image and image.filename:
                filename = secure_filename(image.filename)
                image.save(os.path.join(UPLOAD_FOLDER, filename))
            return render_template('success.html', message="Form submitted successfully!")
        else:
            return render_template('form.html', form=form)

    return render_template('form.html', form=form)

# Microsoft login
@app.route('/login')
def login():
    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
        token_cache=msal.SerializableTokenCache()
    )
    auth_url = msal_app.get_authorization_request_url(
        SCOPE,
        redirect_uri=url_for('getAToken', _external=True)
    )
    return redirect(auth_url)

# Microsoft callback
@app.route(REDIRECT_PATH)
def getAToken():
    cache = msal.SerializableTokenCache()
    msal_app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
        token_cache=cache
    )
    code = request.args.get("code")
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=SCOPE,
        redirect_uri=url_for('getAToken', _external=True)
    )

    if "access_token" in result:
        session[SESSION_KEY] = cache.serialize()
        session["user"] = result.get("id_token_claims")
        return redirect(url_for("index"))
    else:
        return f"Login failed: {json.dumps(result, indent=2)}"

# Logout
@app.route('/logout')
def logout():
    session.clear()
    logout_url = (
        f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri={url_for('index', _external=True)}"
    )
    return redirect(logout_url)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
