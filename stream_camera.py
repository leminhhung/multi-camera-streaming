# -*- coding: utf-8 -*-
import cv2
import redis
import numpy as np
from base_camera import BaseCamera
from utils import OBJECT_DETECTED_KEY
import pickle

redis_server = redis.Redis()

class StreamCamera(BaseCamera):

    def __init__(self, cam_id):
        super(StreamCamera, self).__init__(cam_id)

    @staticmethod
    def frames(unique_id):
        while True:
            try:
                str_frame = redis_server.get(unique_id)
                if not str_frame:
                    continue
                frame = cv2.imdecode(np.fromstring(str_frame, np.uint8), cv2.COLOR_BGR2RGB)
                detected_objects = pickle.loads(redis_server.get(OBJECT_DETECTED_KEY))
                if detected_objects and int(unique_id) in detected_objects:
                    for person in detected_objects[int(unique_id)]:
                        try:
                            object_name = person['object']
                            confidence = person['confidence']
                            startX = person['start-x']
                            startY = person['start-y']
                            endX = person['end-x']
                            endY = person['end-y']
                            cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)
                            text = "{}: {:.4f}".format(object_name, confidence)
                            cv2.putText(frame, text, (startX, startY - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, (0, 255, 0), 2)
                        except Exception as e:
                            print(e)
                frame = cv2.imencode('.jpg', frame)[1].tostring()
                yield frame
            except Exception as e:
                    print(e)