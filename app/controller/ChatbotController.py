from app.model.message import Message

from app import response, app, db

from flask import request
from flask_jwt_extended import *

from datetime import datetime,timedelta
import string
import numpy as np
import json
import pandas as pd
import re
from nltk.corpus import stopwords
import random

from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras.models import load_model

from sklearn.preprocessing import LabelEncoder

with open('C:/Users/wiart/Documents/Backend Teman Ngorte - TUBES DEEP LEARNING/Backend/app/controller/mentalhealth_intent_update2_new.json') as content:
    data1 = json.load(content)
#getting all the data to lists
tags = []
inputs = []
responses={}
for intent in data1['intents']:
  responses[intent['tag']]=intent['responses']
  for lines in intent['patterns']:
    inputs.append(lines)
    tags.append(intent['tag'])
#converting to dataframe
data = pd.DataFrame({"inputs":inputs,
                     "tags":tags})

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('indonesian'))

data['inputs'] = data['inputs'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
data['inputs'] = data['inputs'].apply(lambda wrd: ''.join(wrd))
data['inputs'] = data['inputs'].apply(lambda wrd: REPLACE_BY_SPACE_RE.sub(' ', wrd))
data['inputs'] = data['inputs'].apply(lambda wrd: BAD_SYMBOLS_RE.sub(' ', wrd))
data['inputs'] = data['inputs'].apply(lambda wrd: ' '.join(word for word in wrd.split() if word not in STOPWORDS))

tokenizer = Tokenizer(num_words=2000)
tokenizer.fit_on_texts(data['inputs'])
train = tokenizer.texts_to_sequences(data['inputs'])
x_train = pad_sequences(train)

le = LabelEncoder()
y_train = le.fit_transform(data['tags'])

input_shape = x_train.shape[1]

model = load_model('C:/Users/wiart/Documents/Backend Teman Ngorte - TUBES DEEP LEARNING/Backend/app/controller/model.h5')

def get_response(message):
    texts_p = []
    prediction_input = [letters.lower() for letters in message if letters not in string.punctuation]
    prediction_input = ''.join(prediction_input)
    texts_p.append(prediction_input)
    # tokenizing and padding
    prediction_input = tokenizer.texts_to_sequences(texts_p)
    prediction_input = np.array(prediction_input).reshape(-1)
    prediction_input = pad_sequences([prediction_input], input_shape)
    # getting output from model
    output = model.predict(prediction_input)
    output = output.argmax()
    # finding the right tag and predicting
    response_tag = le.inverse_transform([output])[0]
    chatbot_response = random.choice(responses[response_tag])
    return chatbot_response

def bot_response_guest(current_user):
    user_text = request.args.get('msg')
    user_timestamp = datetime.now()

    bot_response = get_response(user_text)
    bot_timestamp = datetime.now()

    return response.success({
        "user_message": user_text,
        "response": bot_response,
        "user_timestamp": user_timestamp,
        "bot_timestamp": bot_timestamp,
        "user": current_user
    }, "Success")

def post_bot_response_user(current_user):
    user_text = request.form.get('msg')
    user_timestamp = datetime.now()

    bot_response = get_response(user_text)
    bot_timestamp = datetime.now()

    message = Message(user_msg=user_text, bot_response=bot_response, user_timestamp=user_timestamp, bot_timestamp=bot_timestamp, user_id=current_user['id'])
    db.session.add(message)
    db.session.commit()

    return response.success({
        "user_message": user_text,
        "response": bot_response,
        "user_timestamp": user_timestamp,
        "bot_timestamp": bot_timestamp,
        "user": current_user
    }, "Success")

def singleMessage(message):
    data = {
        'id': message.id,
        'user_message': message.user_msg,
        'bot_response': message.bot_response,
        'user_timestamp': message.user_timestamp,
        'bot_timestamp': message.bot_timestamp
    }
    return data

def formatMessage(data):
    array = []

    for i in data:
        array.append(singleMessage(i))
    return array

def get_bot_response_user(current_user):
    message = Message.query.filter_by(user_id=current_user['id'])

    data_message = formatMessage(message)

    return response.success({
        "chatbot_message": data_message,
        "user": current_user
    }, "Success")