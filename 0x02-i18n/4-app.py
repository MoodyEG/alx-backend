#!/usr/bin/env python3
""" Back to flask """
from flask import Flask, render_template, request
from flask_babel import Babel


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


@app.route("/", strict_slashes=False)
def index() -> str:
    """ Index route """
    return render_template("3-index.html")


if __name__ == "__main__":
    app.run(debug=True)
