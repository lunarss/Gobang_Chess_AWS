from flask import render_template, request, url_for, g, redirect, session
from passlib.hash import sha256_crypt
from threading import Thread
from app import webapp
from flask_mail import Message
from app.email import send_email
from app.dynamo import Dynamodb

import datetime
import jwt
import re
import mysql.connector


error_msg = None


@webapp.route('/password/change', methods = ['GET', 'POST'])
def password_change():
    # auth check
    if 'role' in session and 'username' in session:
        if request.method == "POST":
            username = session['username']
            old_password = request.form.get("old_password", "")
            new_password1 = request.form.get("new_password1", "")
            new_password2 = request.form.get("new_password2", "")
            # form format checking
            if old_password == "":
                error_msg = "Please enter your oringinal password!"
                return render_template("password/passwordchange.html", error_msg = error_msg,
                    old_password = old_password, new_password1 = new_password1, new_password2 = new_password2)
            elif new_password1 == "":
                error_msg = "Password can't be empty!"
                return render_template("password/passwordchange.html", error_msg = error_msg,
                    old_password = old_password, new_password1 = new_password1, new_password2 = new_password2)
            elif new_password2 == "":
                error_msg = "Please confirm your new password!"
                return render_template("password/passwordchange.html", error_msg = error_msg,
                    old_password = old_password, new_password1 = new_password1, new_password2 = new_password2)
            elif new_password1 != new_password2:
                error_msg = "The passwords you provide must be identical!"
                return render_template("password/passwordchange.html", error_msg = error_msg,
                    old_password = old_password, new_password1 = new_password1, new_password2 = new_password2)

            dynamo = Dynamodb()
            # check if the old password match the record
            key = {'username': username}
            projectionExpression = "username, user_password"
            dbresponse = dynamo.dynamodb_get("user_info", key, projectionExpression)
            

            if (sha256_crypt.verify(old_password, dbresponse["user_password"]) == False):
                error_msg = "The password you provide does not match our record!"
                return render_template("password/passwordchange.html", error_msg = error_msg,
                    old_password = old_password, new_password1 = new_password1, new_password2 = new_password2)
            else:
                # encrpt and update password
                password = sha256_crypt.hash(new_password1)
                updateExpression = "set user_password = :p"
                expressionAttributeValues = {':p': password}
                dbresponse = dynamo.dynamodb_update("user_info", key, updateExpression, expressionAttributeValues)
                # give success message
                error_msg = "Your password has been updated."
                return render_template("/main.html", error_msg = error_msg)

        return render_template("/password/passwordchange.html")

    else:
        return render_template("/login/login.html", error_msg = "Please sign in first")

@webapp.route('/password/recovery', methods = ['GET', 'POST'])
def password_recovery():
    if request.method == "POST":
        username = request.form.get("username", "")
        # form format checking
        if username == "":
            error_msg = "Please enter your username!"
            return render_template("password/passwordrecovery.html", error_msg = error_msg,
                username = username)

        dynamo = Dynamodb()
        # check if the username is recorded
        key = {'username': username}
        projectionExpression = "username, user_email"
        dbresponse = dynamo.dynamodb_get("user_info", key, projectionExpression)

        if not dbresponse:
            error_msg = "Sorry, the username you provided does not match our record."
            return render_template("password/passwordrecovery.html", error_msg = error_msg,
                username = username)
        else:
            # send email with password change link to the user
            email_address = dbresponse["user_email"]
            msg = Message(subject = 'Password Reset', sender = 'leo1779project@gmail.com', 
                          recipients = [email_address])
            # msg.body = "Thank you for registering, your default password has been set to 123456. Please use the link below to change your password: \n"
            # get a token for the reset link, valid for 10 minute
            token = jwt.encode({"reset_password": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=600)}, webapp.config.get("JWT_SECRET_KEY"), algorithm='HS256')
            # email display message
            display_msg = "We have received your password recovery request. Please use the link below to reset your password:"
            msg.html = render_template('/password/passwordreset.html', token = token, username = username, display_msg = display_msg)
            Thread(target = send_email, args = (webapp, msg)).start()

            error_msg = "An email that contains the link for your password recovery has been sent!"

            return render_template("password/passwordrecovery.html", error_msg = error_msg,
                username = username)
    return render_template("/password/passwordrecovery.html")

@webapp.route('/password/reset/<token>', methods = ['GET', 'POST'])
def password_reset(token):
    try:
        username = jwt.decode(token, webapp.config.get("JWT_SECRET_KEY"), algorithm='HS256')["reset_password"]
    except Exception as e:
        print(e)
        error_msg = "Unauthorized access."
        return render_template("/login/login.html", error_msg = error_msg)
    
    if not username:
        error_msg = "User info lost, please retry."
        return render_template("login/login.html", error_msg = error_msg)

    return render_template("/password/passwordresetverified.html", token = token)

@webapp.route('/password/reset/verified/<token>', methods = ['POST'])
def password_reset_verified(token):
    password1 = request.form.get("password1", "")
    password2 = request.form.get("password2", "")

    if password1 == "":
        error_msg = "Password can't be empty!"
        return render_template("/password/passwordresetverified.html", token = token,
                password1 = password1, password2 = password2, error_msg = error_msg)
    elif password2 =="":
        error_msg = "Please confirm your new password!"
        return render_template("/password/passwordresetverified.html", token = token,
                password1 = password1, password2 = password2, error_msg = error_msg)
    elif password1 != password2:
        error_msg = "The passwords you provide must be identical!"
        return render_template("/password/passwordresetverified.html", token = token,
                password1 = password1, password2 = password2, error_msg = error_msg)

    try:
        username = jwt.decode(token, webapp.config.get("JWT_SECRET_KEY"), algorithm='HS256')["reset_password"]
    except Exception as e:
        print(e)
        error_msg = "Unauthorized access."
        return render_template("/login/login.html", error_msg = error_msg)

    dynamo = Dynamodb()
    # encrpt and update password
    password = sha256_crypt.hash(password1)

    key = {'username': username}
    updateExpression = "set user_password = :p"
    expressionAttributeValues = {':p': password}
    dbresponse = dynamo.dynamodb_update("user_info", key, updateExpression, expressionAttributeValues)

    # give success message
    error_msg = "Your password has been updated."
    return render_template("/login/login.html", error_msg = error_msg)