from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_cors import CORS
from model import User
from peewee import create_model_tables
import requests
import json

app = Flask(__name__)

CORS(app)

app.config['SECRET_KEY'] = 'top secret!'

create_model_tables([User], fail_silently=True)



def exists(userId):
    return User.select().where(User.userId == userId).exists()

@app.route('/')
def index():
    users = User.select()
    return render_template('index.html', users=[user.to_dict() for user in users])

@app.route('/send/<userId>')
def send(userId):
    header = {"Content-Type": "application/json; charset=utf-8",
          "Authorization": "Basic NzNlYWRlYmYtNTI2ZS00NGI1LWI5MjktOTY4NTFkNzFlZjVk"}

    payload = {"app_id": "8ad4022a-609b-4ab5-840a-1e4b40cb72ef",
           "include_player_ids": [userId],
           "contents": {"en": "Hey notifications"}}

    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

    return redirect(url_for('index'))




@app.route('/push',  methods=['POST'])
def push():
    if request.method == 'POST':
        if request.data:
            user = json.loads(request.data)
            print(user)
            if exists(user['userId']):
                return jsonify({'User': 'Exists'}), 400
            user = User(**user)
            user.save()
            return jsonify({'success': True}), 200
        return jsonify({'success': False}), 400
    return jsonify({'method': 'Post Allowed'}), 400


if __name__ == '__main__':
    app.run()
