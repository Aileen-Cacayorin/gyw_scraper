import os
from flask import Flask, request, redirect, render_template
from flask import json, jsonify
from lxml import html, etree
import requests
from bs4 import BeautifulSoup
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


@app.route('/_results')
def results():
    brand_name = request.args.get('brand_name').lower()
    page = requests.get(
        'https://grabyourwallet.org/Boycott%20These%20Companies.html')  # sends request to Grab Your Wallet Site and parses content
    page_info = page.text
    soup = BeautifulSoup(page_info, "lxml")
    table = soup.find_all('table')  # finds table and rows
    rows = table[0].find_all('tr')  # this returns too many rows, need to find way to only find rows with content
    brands = []
    for row in rows:
        if len(row) > 33:  # limits which rows are searched
            info = row.find_all('td')  # gets td for row
            if len(info) > 0:  # limits to rows that only returned td
                brand = info[0].get_text().lower()  # gets first td in row, where all the brands on page are listed
                if brand != "":  # eliminates blank td
                    brand = re.sub(r"\(.*\)", "", brand)  # removes extra info in parentheses after brand name
                    brand = re.sub(r'[^\w\s]', '', brand)  # removes punctuation from brand
                    brands.append(brand)
        else:
            continue
    message=""
    for brand in brands:
        if re.sub(r'[^\w\s]', '', brand_name) == brand:
            message = brand_name.title() + " is on the boycott list. Shop elsewhere."
            color= "red"
            break
        else:
            message = brand_name.title() + " is not the boycott list. Happy shopping!"
            color= "green"
    # return render_template('results.html', brands=brands, brand_name=brand_name, message=message)
    return jsonify(message=message, color=color)


  #creates regex based on brand_name:
  # brand_regex = r"\b(?=\w)" + re.escape(brand_name) + r"\b(?!\w)"