from flask import render_template, request, url_for, g, redirect, make_response, session
from passlib.hash import sha256_crypt
from decimal import Decimal
from app import webapp
from app.dynamo import Dynamodb

import mysql.connector

import os
import json
import boto3


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)

@webapp.route('/', methods = ['GET'])
@webapp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == "":
            error_msg = "Please enter your username!"
            return render_template("login/login.html",error_msg=error_msg,
                username=username, password=password)
        elif password =="":
            error_msg = "Please enter your password!"
            return render_template("login/login.html",error_msg=error_msg,
                username=username, password=password)

    
        dynamo = Dynamodb()

        key = {'username': username}
        projectionExpression = "username, user_email, user_password, user_role"
        dbresponse = dynamo.dynamodb_get("user_info", key, projectionExpression)
        # print(dbresponse)
        if (not dbresponse):
            error_msg = "User does not exist."
            return render_template("login/login.html", error_msg=error_msg,
                username=username, password=password)
                
        else:
            verified_password = dbresponse["user_password"]

        if (sha256_crypt.verify(password, verified_password) == False):
            error_msg = "The password you provided was incorrect."
            return render_template("login/login.html", error_msg=error_msg,
                username=username, password=password)
        else:
            session['username'] = request.form["username"]
            session['role'] = json.dumps(dbresponse["user_role"], cls = DecimalEncoder)
            # resp = make_response(render_template("main.html"))
            # return resp
            # print(session)
            return redirect(url_for('main'))

    if 'username' in session:
        # return render_template("main.html")
        return redirect(url_for('main'))
    
    return render_template("login/login.html")

@webapp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop("role", None)
    return redirect(url_for("login"))




