from flask import render_template, request, url_for, g, redirect, session, jsonify
from passlib.hash import sha256_crypt
from threading import Thread
from flask_mail import Message
from app.email import send_email
from app.dynamo import Dynamodb
from app import webapp


import datetime
import jwt
import re



error_msg = None


@webapp.route('/user/list', methods = ['GET'])
def user_list():
    # auth check
    if 'role' in session and 'username' in session:
        if int(session['role']) != 1:
            error_msg = "You have to be a privileged user to be able to use this feature."
            return render_template("main.html", error_msg = error_msg)

        dynamo = Dynamodb()
        projectionExpression = "username, user_email"
        dbresponse = dynamo.list_all("user_info", projectionExpression)
        # print(dbresponse)

        return render_template("user/userlist.html", title = "User Management", dbresponse = dbresponse)
    
    else:
        return render_template("/login/login.html", error_msg = "Please sign in first")

@webapp.route('/user/signup', methods = ['GET', 'POST'])
def user_signup():
    # code to execute if it is a post request
    if request.method == "POST":
        username = request.form.get("username", "")
        email_address = request.form.get("email_address", "")

        # form format checking
        if username == "":
            error_msg = "You must put in a username!"
            return render_template("user/usercreate.html",title="User Signup",
                error_msg=error_msg, username=username, email_address=email_address)
        elif email_address =="":
            error_msg = "You must put in an email address!"
            return render_template("user/usercreate.html",title="User Signup",
                error_msg=error_msg, username=username, email_address=email_address)
        elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email_address):
            error_msg = "Please enter a valid email address!"
            return render_template("user/usercreate.html",title="User Signup",
                error_msg=error_msg, username=username, email_address=email_address)

        default_password = sha256_crypt.hash("123456")
        dynamo = Dynamodb()

        # check if the username is used, here we allow same email address to be used multiple times
        key = {'username': username}
        projectionExpression = "username, user_email, user_password, user_role"
        dbresponse = dynamo.dynamodb_get("user_info", key, projectionExpression)
        # if username is available
        if (not dbresponse):
            item = {"username": username,
                    "user_email": email_address,
                    "user_password": default_password,
                    "user_role": 0}
            # put item to dynamodb
            dbresponse = dynamo.dynamodb_put("user_info", item)
            print(dbresponse)
            # send email with password change link to the user
            msg = Message(subject = 'Registeration Confirmed', sender = 'leo1779project@gmail.com', 
                          recipients = [email_address])
            # msg.body = "Thank you for registering, your default password has been set to 123456. Please use the link below to change your password: \n"
            # get a token for the reset link, valid for 10 minutes
            token = jwt.encode({"reset_password": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=600)}, webapp.config.get("JWT_SECRET_KEY"), algorithm='HS256')
            # email display message
            display_msg = "Thank you for registering, your default password has been set to 123456. Please use the link below to change your password:"
            msg.html = render_template('/password/passwordreset.html', token = token, username = username, display_msg = display_msg)
            Thread(target = send_email, args = (webapp, msg)).start()
            # give success message
            error_msg = "User signup success, an email notification has been sent!"
            return render_template("user/usercreate.html",title="User Signup",
                    error_msg=error_msg, username=username, email_address=email_address)
        # if username is used
        else:
            error_msg = "User name already in use!"
            return render_template("user/usercreate.html",title="User Signup",
                error_msg=error_msg, username=username, email_address=email_address)

    # Code to execute if it is a get request
    return render_template("/user/usercreate.html", title = "User Signup")

@webapp.route('/user/delete/<string:username>', methods = ['POST'])
def user_delete(username):
    # auth check
    if 'role' in session and 'username' in session:
        if int(session['role']) != 1:
            error_msg = "You have to be a privileged user to be able to use this feature."
            return render_template("main.html", error_msg = error_msg)

        # form format checking
        if not username:
            error_msg = "User information error, Please retry."
            return render_template("main.html", error_msg = error_msg)

        else:
            dynamo = Dynamodb()
            key = {'username': username}
            dbresponse = dynamo.dynamodb_delete("user_info", key)

            error_msg = "User delete success!"
            # give success message and reload with new list
            projectionExpression = "username, user_email"
            dbresponse = dynamo.list_all("user_info", projectionExpression)

            return render_template("user/userlist.html", title = "User Management", dbresponse = dbresponse, error_msg = error_msg)
    
    else:
        return render_template("/login/login.html", error_msg = "Please sign in first")


