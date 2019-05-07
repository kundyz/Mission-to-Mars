import sys
import pymongo
import scrape_mars
from flask import Flask, render_template, jsonify, redirect

app = Flask(__name__)

client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_facts

@app.route('/')
def home():
    mars_data = list(db.collection.find())[0]
    return render_template('index.html', mars_data=mars_data)

@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape()
    db.collection.insert_one(mars_data)
    return render_template('mars_scrape.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=80) 