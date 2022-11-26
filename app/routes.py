from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import app
from app.controller import UserController


@app.route('/')
def index():
    return 'Hello'


@app.route('/register', methods=['POST'])
def users():
    return UserController.register()


@app.route('/login', methods=['POST'])
def logins():
    return UserController.login()


@app.route('/login-guest', methods=['POST'])
def loginGuests():
    return UserController.loginGuest()


# @app.route('/chatbot-guest', methods=['GET'])
# @jwt_required()
# def botResponse():
#     current_user = get_jwt_identity()
#     return ChatbotController.bot_response_guest(current_user)

# @app.route('/chatbot-user', methods=['POST', 'GET'])
# @jwt_required()
# def botUserResponse():
#     current_user = get_jwt_identity()
#     if request.method == 'POST':
#         return ChatbotController.post_bot_response_user(current_user)
#     else:
#         return ChatbotController.get_bot_response_user(current_user)