import cv2
import imutils
import redis
import numpy as np
from . import CLASSES, CONSIDER, CONFIDENCE

# redis_server = redis.Redis(host='redis', port=6379)
redis_server = redis.Redis()

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("model/MobileNetSSD_deploy.prototxt", "model/MobileNetSSD_deploy.caffemodel")

class MobileNetSSDDetection:
    @staticmethod
    def perform(cam_id):
        result = []
        str_frame = redis_server.get(cam_id)
        if str_frame:
            frame = cv2.imdecode(np.fromstring(str_frame, np.uint8), cv2.IMREAD_COLOR)
            redis_server.set(cam_id, '')
        else:
            return result

        # do sdd_detection
        frame = imutils.resize(frame, width=400)
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > CONFIDENCE:
                idx = int(detections[0, 0, i, 1])
                if CLASSES[idx] in CONSIDER:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    result.append({
                        "object": CLASSES[idx],
                        "confidence": confidence,
                        "start-x": startX,
                        "start-y": startY,
                        "end-x": endX,
                        "end-y": endY
                    })
        return result
