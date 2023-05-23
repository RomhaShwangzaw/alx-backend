#!/usr/bin/env python3
"""A Basic Flask app"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Optional, Dict


class Config:
    """Babel Configuration Class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Optional[Dict]:
    """
    Returns a user dictionary corresponding to the
    user passed in as a url argument `login_as`.
    If the ID cannot be found or if `login_as` was
    not passed, returns None.
    """
    login_as = request.args.get('login_as')
    if not login_as:
        return None
    return users.get(int(login_as))


@app.before_request
def before_request() -> None:
    """
    Uses `get_user` to find a user if any, and set
    it as a global on `flask.g.user`.
    """
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """Determines the best match with our supported languages"""
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')
    header_locale = request.headers.get('locale')
    if header_locale in app.config['LANGUAGES']:
        return header_locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """Determines the best match with our supported timezones"""
    tz = request.args.get('timezone')
    if not tz and g.user:
        tz = g.user.get('timezone')
    try:
        return timezone(tz).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index() -> str:
    """The home/index page"""
    return render_template('7-index.html')


if __name__ == "__main__":
    app.run()
