import requests, psycopg2
from flask import Flask, render_template, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash


from sweater import conn, cur, app


class User(object):
    def __init__(self, loggined, user_login, email, h_password):
        self.loggined = loggined
        self.user_login = user_login
        self.email = email
        self.h_password = h_password
    def UserLoggedIn(self):
        self.loggined = True
    def UserLoggedOut(self):
        self.loggined = False
    def SetUsername(self, username):
        self.user_login = username
    def GetName(self):
        return(self.user_login)
    def SetEmail(self, email):
        self.email = email
    def GetEmail(self):
        return(self.email)
    def SetPass(self, password):
        self.h_password = generate_password_hash(password)
    def VerifyPass(self, h_pass, password):
        return check_password_hash(h_pass, password)