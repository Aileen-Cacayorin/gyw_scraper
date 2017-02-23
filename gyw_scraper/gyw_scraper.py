import os
from flask import Flask, request, redirect, render_template
from lxml import html, etree
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re



app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , gyw_scraper.py

# Load default config and override config from an environment variable
app.config.update(dict(
))

app.config.from_envvar('GYW_SCRAPER_SETTINGS', silent=True)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    # retrieves form input
    brand_name = request.form.get('inputBrand')

    # sends request to Grab Your Wallet Site and parses content
    page = requests.get('https://grabyourwallet.org/Boycott%20These%20Companies.html')
    data = page.text
    soup = BeautifulSoup(data, "lxml")

    #finds table and rows
    table = soup.find_all('table')

    #this returns to many rows, need to find way to only find rows with content
    rows = table[0].find_all('tr')
    brands =[]
    for row in rows:
        #limits which rows are searched
        if len(row)>33:
            info = row.find_all('td')
            #only applies to rows that returned td
            if len(info)>0:
                #gets first td in row, where all the brands on page are listed
                brand = info[0].get_text()
                #eliminates blank td
                if brand != "":
                    #removes extra info in parentheses after brand name
                    brand = re.sub(r"\(.*\)","", brand)
                    brands.append(brand)
        else:
            continue
    return render_template('results.html', brands=brands, brand_name=brand_name)