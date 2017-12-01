from datetime import datetime
from flask import render_template
from OkiPoki import app as main

@main.after_request
def add_header(response):
    response.headers['Cache-Control'] = "no-cache, no-store"
    return response

@main.route('/')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )
