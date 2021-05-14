import redis

# REDIS_SERVER = redis.Redis(host='redis', port=6379)
# redis_server = redis.Redis(host='localhost', port=6379)


OBJECT_DETECTED_KEY = "object_detected_key"

DEMO_CAMERAS = [
    {
        "cam_id": 1,
        "camera_name": "cam-ip-home",
        "uri_stream": "rtsp://admin:abc123456@192.168.100.7:554/onvif1",
        "uri_type": "rtsp",
        "active": True
    },
    {
        "cam_id": 2,
        "camera_name": "cam-ip-home-gate",
        "uri_stream": "rtsp://admin:abc123456@192.168.100.12:554/onvif1",
        "uri_type": "rtsp",
        "active": True
    },
    {
        "cam_id": 3,
        "camera_name": "cam-ip-raspi",
        "uri_stream": "http://192.168.100.5:8181/video_feed",
        "uri_type": "http",
        "active": True
    },
    {
        "cam_id": 4,
        "camera_name": "cam-android-font",
        "uri_stream": "rtsp://192.168.100.2:5554/front",
        "uri_type": "rtsp",
        "active": False
    },
    {
        "cam_id": 5,
        "camera_name": "cam-android-back",
        "uri_stream": "rtsp://192.168.100.2:5554/back",
        "uri_type": "rtsp",
        "active": False
    },
    {
        "cam_id": 6,
        "camera_name": "laptop-webcam",
        # "uri_stream": "http://172.16.3.36:8182/video_feed",
        "uri_stream": "http://192.168.100.3:8182/video_feed",
        "uri_type": "http",
        "active": True
    }
]