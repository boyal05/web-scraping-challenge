from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    scraped_info = mongo.db.scraped_info.find_one()
    return render_template("index.html", scraped_info=scraped_info)

@app.route("/scrape")
def scrape():
    # Run scrape function
    scraped = scrape_mars.mars_scrape()

    mongo.db.scraped_info.update({}, scraped, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

