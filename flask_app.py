#importing the packages
from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen as uReq
import pymongo
from flask import Flask, render_template, request,jsonify

#initialising the flask_app

app = Flask(__name__)

@app.route('/',methods=['POST','GET']) # route with allowed methods as POST and GET
def index():
        if request.method == 'POST':
            reviews = []
            searchString = request.form['content'].replace(" ","") # obtaining the search string entered in the form
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString # preparing the URL to search the product on flipkart
            uClient = uReq(flipkart_url) # requesting the webpage from the internet
            flipkartPage = uClient.read() # reading the webpage
            uClient.close() # closing the connection to the web server
            flipkart_html = bs(flipkartPage, "html.parser") # parsing the webpage as HTML
            bigboxes = flipkart_html.findAll("div", {"class": "bhgxx2 col-12-12"}) # seacrhing for appropriate tag to redirect to the product link
            del bigboxes[0:3] # the first 3 members of the list do not contain relevant information, hence deleting them.
            box = bigboxes[0] #  taking the first iteration (for demo)
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href'] # extracting the actual product link
            prodRes = requests.get(productLink) # getting the product page from server
            prod_html = bs(prodRes.text, "html.parser") # parsing the product page as HTML
            commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"}) # finding the HTML section containing the customer comments
