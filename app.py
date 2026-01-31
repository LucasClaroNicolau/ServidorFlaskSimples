import threading
import time
import cv2
from flask import Flask, Response, render_template_string
from telegram import enviarMensagem

app = Flask(__name__)

# Webcam (0 = webcam padrão)
camera = cv2.VideoCapture(0)

def loop_telegram():
    while True:
        enviarMensagem()
        time.sleep(3600)

def gerar_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Codifica frame para JPG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def home():
    return "Servidor Flask rodando!"

@app.route("/camera")
def camera_page():
    return render_template_string("""
    <html>
        <head>
            <title>Webcam ao vivo</title>
            <style>
                body {
                    margin: 0;
                    background: #000;
                    text-align: center;
                }
                img {
                    width: 100%;
                    height: auto;
                }
            </style>
        </head>
        <body>
            <img src="/video_feed">
        </body>
    </html>
    """)

@app.route("/video_feed")
def video_feed():
    return Response(
        gerar_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == "__main__":
    t = threading.Thread(target=loop_telegram, daemon=True)
    t.start()

    app.run(host="0.0.0.0", port=5000, debug=False)
