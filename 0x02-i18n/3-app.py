#!/usr/bin/env python3
""" Back to flask """
from flask import Flask, render_template, request
from flask_babel import Babel, gettext


class Config:
    """ Flask configuration class """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config())
babel = Babel(app)


# @babel.localeselector
def get_locale():
    """ Get best locale in the request """
    return request.accept_languages.best_match(app.config["LANGUAGES"])


babel.init_app(app, locale_selector=get_locale)


@app.route("/", strict_slashes=False)
def index():
    """ Index route """
    return render_template("3-index.html",
                           home_title=gettext("home_title"),
                           home_header=gettext("home_header"))


if __name__ == "__main__":
    app.run(debug=True)
