from flask import Flask, Response

import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)

def gen():
    """Video streaming generator function."""
    while True:
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        _, frame = camera.read()
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8182, debug=True, threaded=True)
# RUN: gunicorn --threads 5 --workers 1 --bind 0.0.0.0:8182 laptop_webcam_stream:app