#!/usr/bin/env python3
""" Back to flask """
from flask import Flask, render_template, request, g
from flask_babel import Babel


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """ Flask configuration class """
    LANGUAGES: list = ["en", "fr"]
    BABEL_DEFAULT_LOCALE: str = "en"
    BABEL_DEFAULT_TIMEZONE: str = "UTC"


app: Flask = Flask(__name__)
app.config.from_object(Config())
babel: Babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """ Get best locale in the request """
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


# for local use and testing
# babel.init_app(app, locale_selector=get_locale)


def get_user() -> dict:
    """ Get user from login_as parameter """
    user_id = request.args.get('login_as')
    if user_id is None:
        return None
    return users.get(int(user_id))


@app.before_request
def before_request():
    """ Set user before each request """
    g.user = get_user()


@app.route("/", strict_slashes=False)
def index() -> str:
    """ Index route """
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run(debug=True)
