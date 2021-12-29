from flask import render_template, session
from base64 import b64encode

from app import webapp

import boto3
# webapp.secret_key = ajsdadbwa'xfadad\fea]'

@webapp.route('/index',methods=['GET'])
@webapp.route('/main',methods=['GET'])
def main():
    if 'username' in session:

        return render_template("main.html")

    return render_template("/login/login.html", error_msg = "Please sign in first.")