import requests, psycopg2
from flask import Flask, render_template, url_for, request, redirect
from sweater import conn, cur, app

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


userOne = User(False, 'username', 'email', '')


@app.route("/founder")
def founder():
    if userOne.loggined:
        return render_template("nft.html")
    else:
        return redirect(url_for('auth'))


@app.route("/res", methods=['POST', "GET"])
def result():
    output = request.form.to_dict()
    address = output["address"]
    url = 'https://solana-gateway.moralis.io/nft/mainnet/' + address + '/metadata'
    headers = {
        "accept": "application/json",
        "X-API-Key": "SWnpmagdLrYt67aFhsaBRRzoubD59cdQkydkZLeljvVREBpWGmpLktfRLZXcvudp"
    }
    response = requests.get(url, headers=headers)
    cur.execute("""SELECT * from nft WHERE nft_address = %s""", (address,))
    answer = cur.fetchall()
    if answer!=[]:
        for row in answer:
            print('nft_address - ', row[0])
            print('nft_info - ', row[1])
            print('fromDB')
        return render_template('res2.html', address=response.text)
    else:
        cur.execute("""INSERT INTO nft (nft_address, nft_info) VALUES (%s, %s);""", (address, response.text))
        conn.commit()
        print('added to db')
        return render_template('res.html', address=response.text)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/logout')
def logout():
    if userOne.loggined:
        userOne.UserLoggedOut()
        return redirect("/")
    else:
        return redirect("/")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/sign')
def sign():
    return render_template("sign_in.html")


@app.route('/signres', methods=['POST', "GET"])
def sign_res():
    output = request.form.to_dict()
    name = output["namereg"]
    email = output["emailreg"]
    password = output["passreg"]
    #hash_password = generate_password_hash(password, method='sha256')   hash_password
    userOne.SetPass(password)
    h_password1 = userOne.h_password
    cur.execute("""SELECT * from users WHERE user_name = %s""", (name,))
    answer1 = cur.fetchall()
    if answer1!=[]:
        return render_template("sign_res.html", answer381="User with this name is already registered")
    else:
        cur.execute("""INSERT INTO users (user_name, user_email, user_password) VALUES (%s, %s, %s);""", (name, email, h_password1))
        conn.commit()
        return render_template('sign_res.html', answer381="registration completed successfully")


@app.route('/log', methods=['POST', "GET"])
def log():
    if request.method == 'POST':
        output = request.form.to_dict()
        name = output["namelog"]
        password = output["passlog"]
        #hash_password = generate_password_hash(password, method='sha256')
        cur.execute("""SELECT user_email FROM users WHERE user_name = %s""", (name,))
        answer17 = cur.fetchall()
        if answer17 != []:
            cur.execute("""SELECT user_password FROM users WHERE user_name = %s""", (name,))
            answer16 = cur.fetchall()
            if userOne.VerifyPass(answer16[0][0], password):
                userOne.SetUsername(name)
                userOne.SetEmail(email=answer17[0][0])
                # return render_template("log_in.html", answer391="login succesfull")
                userOne.UserLoggedIn()
                return redirect(url_for('profile'), 301)
            else:
                return render_template('log_in.html', answer391="Incorrect username or password entered")
        else:
            return render_template('log_in.html', answer391="Incorrect username or password entered")
    return render_template("log_in.html")


@app.route('/profile')
def profile():
    if userOne.loggined:
        return render_template('profile.html', namepi=userOne.GetName(), emailpi=userOne.GetEmail())
    else:
        return redirect('auth')


@app.route('/auth')
def auth():
    return render_template('auth.html')


@app.route('/user/<string:name>/<string:password>')
def user(name, password):
    return "User page: " + name + " - " + password


"""
testosterone
testo99
"""