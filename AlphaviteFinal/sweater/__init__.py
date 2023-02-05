import requests, psycopg2
from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap


app = Flask(__name__)
conn = psycopg2.connect("dbname=dictionary user=postgres password=6679")
cur = conn.cursor()



from sweater import models, routes