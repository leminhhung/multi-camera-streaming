from flask import Flask, render_template, Response
from stream_camera import StreamCamera
from utils import DEMO_CAMERAS

app = Flask(__name__)
# cache = redis.Redis(host='redis', port=6379)

def gen(camera):
    while True:
        frame = camera.get_frame()
        if not frame:
            continue
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/welcome')
def welcome():
    return "welcome to security camera !"

@app.route('/')
def index():
    cameras = []
    for i in DEMO_CAMERAS:
        if i['active']:
            cameras.append(i)
    return render_template('index.html', cameras=cameras)

@app.route('/stream/<cam_id>')
def video_feed(cam_id):
    return Response(gen(StreamCamera(cam_id)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# gunicorn --threads 5 --workers 1 --bind 0.0.0.0:5000 app:app