import requests, psycopg2
from flask import Flask, render_template, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from sweater import app, __name__

if __name__ == "__main__":
    app.run(debug=True)
