#!/usr/bin/env python3
""" Application """

from os import abort
from flask import Response
from django.shortcuts import redirect
from flask import Flask, jsonify, make_response
import flask
from requests import request, session
from auth import Auth
AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """ Home page """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """ register a new user """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"})


@app.route('/sessions', methods=['POST'])
def sessions():
    """ Login """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)
    response = make_response(
        jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """ Delete the session """
    cookie = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(cookie)
    if user is None:
        abort(403)
    else:
        AUTH.destroy_session(user.id)
        return redirect('/')

    @app.route('/profile', methods=['GET'])
    def profile(self):
        """ Profile """
        cookie = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(cookie)
        if user is None:
            abort(403)
        else:
            return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
