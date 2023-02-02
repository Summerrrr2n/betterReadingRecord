# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from betterReadingRecord.extensions import db
from betterReadingRecord.models import User, Item, ReadRecord, Book

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('read_record.app'))

    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if user is not None and user.validate_password(password):
            login_user(user)
            return jsonify(message='Login success.')
    return jsonify(message='Invalid username or password.'), 400


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(message='Logout success.')

@auth_bp.route('/register',methods=['POST'])
def register():
    # get register info
    data = request.get_json()
    username = data['username']
    password = data['password']

    is_registered = User.query.filter_by(username=username).first()
    if is_registered:
        return jsonify(message='用户已存在.')

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify(username=username, password=password, message='Generate success.')