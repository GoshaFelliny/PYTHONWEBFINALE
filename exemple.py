from flask import Flask, redirect, url_for, request, json, jsonify
import random
import string
import os

app = Flask(__name__)
app.config['ROOMS_FILE'] = 'rooms.json'


# Инициализация комнат из JSON файла
def load_rooms():
    if os.path.exists(app.config['ROOMS_FILE']):
        with open(app.config['ROOMS_FILE'], 'r') as f:
            return json.load(f)
    return {}


rooms = load_rooms()


def generate_room_code():
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=4))
        if code not in rooms:
            return code


@app.route('/')
def index():
    return '''
    <!doctype html>
    <html>
    <head><title>Game Rooms</title></head>
    <body>
    <h1>Добро пожаловать!</h1>
    <a href="/create">Создать комнату</a>
    </body>
    </html>
    '''


@app.route('/create', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        room_code = generate_room_code()
        rooms[room_code] = []

        # Сохраняем в JSON файл
        with open(app.config['ROOMS_FILE'], 'w') as f:
            json.dump(rooms, f)

        return redirect(url_for('room', room_code=room_code))

    return '''
    <form method="POST">
    <button type="submit">Создать новую комнату</button>
    </form>
    '''


@app.route('/room/<room_code>', methods=['GET', 'POST'])
def room(room_code):
    if room_code not in rooms:
        return "Комната не найдена", 404

    if request.method == 'POST':
        player_name = request.form['player_name']
        rooms[room_code].append(player_name)

        with open(app.config['ROOMS_FILE'], 'w') as f:
            json.dump(rooms, f)

    return f'''
    <!doctype html>
    <html>
    <head><title>Комната {room_code}</title></head>
    <body>
    <h1>Комната {room_code}</h1>
    <form method="POST">
    <input type="text" name="player_name" placeholder="Ваше имя" required>
    <button type="submit">Присоединиться</button>
    </form>
    <h2>Игроки:</h2>
    <ul>
    {' '.join(f'<li>{player}</li>' for player in rooms[room_code])}
    </ul>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(debug=True)
