import os
from flask import Flask, request, redirect, render_template
from lxml import html, etree
import requests
from bs4 import BeautifulSoup
import pandas as pd



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
    data = page.text
    import lxml
    soup = BeautifulSoup(data, "lxml")
    table = soup.find_all('table')
    rows = table[0].find_all('tr')
    print(len(rows))
    for row in rows:
        if len(row)>33:
            info = row.find_all('td')
            if len(info)>0:
                brand = info[0].get_text()
                if brand != "":
                    print(brand)
        else:
            continue
    # stuff = rows[4].find_all('td')
    # print(len(stuff))
    # print(stuff[0].get_text())
    # for row in rows:
    #     cols = row.find_all('td')
    #     print(cols)


    # tree = html.fromstring(page.content)
    # print(tree)
    # table = etree.HTML(tree)
    # print(table)
    # table_data = tree.xpath('//tr/td/text()')
    # table_data = tree.xpath('//tr')[0]
    # print(table_data.xpath('//td/text()'))
    # for row in table_data:
    #      print (row.xpath('//td/text()'))
    # for element in table_data:
    #     row = html.fromstring(element)
    #     print(row)
    # for row in tree.xpath('//tbody/tr'):
        # print (row.xpath('//td/text()'))
        # row_data = (row.xpath('//td/text()'))
        # print(row_data[3])


    return render_template('results.html')