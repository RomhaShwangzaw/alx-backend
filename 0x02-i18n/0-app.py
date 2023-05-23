#!/usr/bin/env python3
"""A Basic Flask app"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index() -> str:
    """The home/index page"""
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
