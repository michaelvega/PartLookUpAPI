"""
    app.py
    API looks up part number of certain manufacture parts.
"""
import os

from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, request
from flask_cors import CORS
import logging

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': '*'}})  # what site resources (r) followed by accessors
tags = {}
blocks = {}


def getPage(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


@app.route('/')
@app.route('/API')
@app.route('/API/')
def home():
    return render_template('index.html')


@app.route('/API/partLookUp', methods=['POST'])
def partLookUpPOST():
    global tags
    global blocks
    blocks = {}
    tags = {}
    empty_dict = {"results": "Unable to Scan Part"}
    Query = str(request.data.decode())

    partnum = Query

    url = "https://www.partstown.com/parts?q=" + partnum
    soup = getPage(url)
    logging.debug(soup)
    try:
        price = soup.find('div', class_='js-product-listPrice').text
        name = soup.find('h1', class_='name').text
        results_json = {name: price}
    except AttributeError:  # If name and price are NoneType
        results_json = empty_dict

    return results_json


if __name__ == '__main__':
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    app.run(debug=True, host='localhost', port=int(os.environ.get('PORT', 8080)))  # Should be 0.0.0.0, 8080

# STAM2-Z11877
