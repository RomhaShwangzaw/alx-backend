#!/usr/bin/env python3
"""A Basic Flask app"""

from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """Babel Configuration Class"""
    LANGUAGES = ["en", "fr"]


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route('/')
def index() -> str:
    """The home/index page"""
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run()
