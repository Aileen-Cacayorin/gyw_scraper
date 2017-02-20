import os
from flask import Flask, request, redirect, render_template
from lxml import html
import requests

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , gyw_scraper.py

# Load default config and override config from an environment variable
app.config.update(dict(
))

app.config.from_envvar('GYW_SCRAPER_SETTINGS', silent=True)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/results')
def results():
    page = requests.get('https://grabyourwallet.org/Boycott%20These%20Companies.html')
    tree = html.fromstring(page.content)
    title = tree.xpath('//span[@class="navbar-brand"]/text()')

    return render_template('results.html', title=title)