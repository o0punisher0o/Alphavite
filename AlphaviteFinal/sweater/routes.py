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
        cur.execute(f"""SELECT * from words ORDER BY words ASC""")
        answer = cur.fetchall()
        if answer != []:
            x = ''
            y = ''
            for row in answer:
                x += row[1]
                x += '\n\n\n'
                y += row[2]
                y += '\n\n\n'
                print('word - ', row[1])
                print('definition - ', row[2])

            return render_template('nft.html', word=x, definition=y)
        else:
            return render_template("nft.html")
    else:
        return redirect(url_for('auth'))


@app.route("/res", methods=['POST', "GET"])
def result():
    output = request.form.to_dict()
    word = output["word"]
    cur.execute(f"""SELECT * from words WHERE word LIKE '{word}%' ORDER BY words ASC""")
    answer = cur.fetchall()
    if answer != []:
        x = ''
        y = ''
        for row in answer:
            x += row[1]
            x += '\n\n\n'
            y += row[2]
            y += '\n\n\n'
            print('word - ', row[1])
            print('definition - ', row[2])

        return render_template('res2.html', word=x, definition=y)
    else:
        return render_template('res.html')


@app.route("/add", methods=['POST', "GET"])
def add():
    output = request.form.to_dict()
    word = output["word"]
    definition = output["definition"]
    cur.execute(f"""SELECT * from words WHERE word = '{word}'""")
    answer = cur.fetchall()
    if answer!=[]:
        for row in answer:
            print('this word is already in database')
        return render_template('res2.html')
    else:
        cur.execute("""INSERT INTO words (word, definition) VALUES (%s, %s);""", (word, definition))
        conn.commit()
        print('added to db')
        return render_template('addres.html')



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
    userOne.SetPass(password)
    h_password1 = userOne.h_password
    cur.execute("""SELECT * from users WHERE username = %s""", (name,))
    answer1 = cur.fetchall()
    if answer1!=[]:
        return render_template("sign_res.html", answer381="User with this name is already registered")
    else:
        cur.execute("""INSERT INTO users (username, email, password) VALUES (%s, %s, %s);""", (name, email, h_password1))
        conn.commit()
        return render_template('sign_res.html', answer381="registration completed successfully")


@app.route('/log', methods=['POST', "GET"])
def log():
    if request.method == 'POST':
        output = request.form.to_dict()
        name = output["namelog"]
        password = output["passlog"]
        #hash_password = generate_password_hash(password, method='sha256')
        cur.execute("""SELECT email FROM users WHERE username = %s""", (name,))
        answer17 = cur.fetchall()
        if answer17 != []:
            cur.execute("""SELECT password FROM users WHERE username = %s""", (name,))
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