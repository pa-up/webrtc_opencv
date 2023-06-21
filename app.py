import cv2
import base64
import numpy as np
from flask import Flask, render_template, Response
from flask_socketio import SocketIO

terminal_command = """
アプリ起動コマンド（ポート番号をOCRアプリ専用で用意）
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=9104
"""

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def process_frame(frame):
    # ここでOpenCVを使ってフレームを処理します
    # 例: グレースケールに変換
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray_frame

@socketio.on('input_video')
def handle_input_video(data):
    input_frame = cv2.imdecode(np.frombuffer(base64.b64decode(data), dtype=np.uint8), cv2.IMREAD_COLOR)
    processed_frame = process_frame(input_frame)
    processed_frame = cv2.flip(processed_frame, 1)
    _, buffer = cv2.imencode('.jpg', processed_frame)
    output_frame = base64.b64encode(buffer).decode('utf-8')
    socketio.emit('output_video', output_frame)

if __name__ == '__main__':
    socketio.run(app)
