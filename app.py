import sys
from flask_pymongo import PyMongo
import scrape_mars
from flask import Flask, render_template, jsonify, redirect

app = Flask(__name__)

client = PyMongo(app=app, uri="mongodb://localhost:27017/mars_db")
collection = client.db.mars_facts

@app.route('/')
def home():
    # mars_data = list(db.collection.find())[0]
    mars_data = collection.find_one()
    return render_template('index.html', mars_data=mars_data)

@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape()
    collection.insert_one(mars_data)
    return render_template('mars_scrape.html')

if __name__ == "__main__":
    app.run(debug=True)
