import imutils
import imagezmq
import time
import cv2
import redis
import pickle
from threading import Thread
from ffmpeg_reader import ffmpegVideoOnvif
from utils import DEMO_CAMERAS, OBJECT_DETECTED_KEY
from sdd_detection.object_detection import MobileNetSSDDetection

# redis_server = redis.Redis(host='redis', port=6379)
redis_server = redis.Redis()

def start_rtsp_camera(cam_id, uri):
    sender = imagezmq.ImageSender()
    ff = ffmpegVideoOnvif(uri)
    t = Thread(target=ff.runGetStream)
    t.start()

    while True:
        image = ff.lastFrame
        if image is not None:
            sender.send_image(cam_id, image)

        time.sleep(0.041)
    ff.flg_run = False

def start_client_http_camera(cam_id, uri):
    sender = imagezmq.ImageSender()
    cam = cv2.VideoCapture(uri)
    time.sleep(2.0)
    while True:
        rc, frame = cam.read()
        if not rc:
            continue
        frame = imutils.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), width=400)
        sender.send_image(cam_id, frame)

def start_zmq_hub():
    image_hub = imagezmq.ImageHub()
    while True:
        cam_id, image = image_hub.recv_image()
        image_hub.send_reply(b'OK')
        frame = cv2.imencode('.jpg', image)[1].tostring()
        redis_server.set(cam_id, frame)

def start_detection():
    while True:
        items = {}
        for cam in DEMO_CAMERAS:
            if not cam['active']:
                continue
            cam_id = cam["cam_id"]
            obj_detected = MobileNetSSDDetection.perform(cam["cam_id"])
            items[cam_id] = obj_detected
            if obj_detected:
                print(f"=cam: {cam_id}==obj_detected:{obj_detected}")

        pickled_object_detected = pickle.dumps(items)
        redis_server.set(OBJECT_DETECTED_KEY, pickled_object_detected)
        time.sleep(0.5)

def main():
    try:
        # start image zmq hub
        task_zmq = Thread(target=start_zmq_hub)
        task_zmq.start()

        # start detection
        detection = Thread(target=start_detection)
        detection.start()

        # start client receiving frames
        for cam in DEMO_CAMERAS:
            if not cam['active']:
                continue
            if cam['uri_type'] == 'http':
                http_client = Thread(target=start_client_http_camera, args=(cam['cam_id'], cam['uri_stream']))
                http_client.start()
            if cam['uri_type'] == 'rtsp':
                rtsp_client = Thread(target=start_rtsp_camera, args=(cam['cam_id'], cam['uri_stream']))
                rtsp_client.start()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()