from app.model.user import User

from app import response, app, db
from flask import request
from flask_jwt_extended import *
from datetime import datetime, timedelta


def register():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        users = User(username=username)
        users.setPassword(password)
        db.session.add(users)
        db.session.commit()
        data = singleObject(users)

        return response.success(data, 'successfully added user')

    except Exception as e:
        print(e)


def singleObject(data):
    data = {
        'id': data.id,
        'username': data.username
    }

    return data


def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user:
            return response.badRequest([], 'Username tidak terdaftar')

        if not user.checkPassword(password):
            return response.badRequest([], 'Kombinasi password salah')

        data = singleObject(user)

        expires = timedelta(days=7)
        expires_refresh = timedelta(days=7)

        acces_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return response.success({
            "data": data,
            "access_token": acces_token,
            "refresh_token": refresh_token,
        }, "Sukses Login!")

    except Exception as e:
        print(e)


def loginGuest():
    try:
        username = "Guest"

        expires = timedelta(days=7)
        expires_refresh = timedelta(days=7)

        acces_token = create_access_token(identity=username, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(identity=username, expires_delta=expires_refresh)

        return response.success({
            "access_token": acces_token,
            "refresh_token": refresh_token,
        }, "Successfully login as a guest")

    except Exception as e:
        print(e)