from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
from APP.data_process.scrape_reviews import scrape
from APP.routes import app

