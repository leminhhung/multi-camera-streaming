FROM python:3.9.5
RUN apt-get update
RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx libsm6 libxext6 libxrender-dev

ADD . /webcam-docker
WORKDIR /webcam-docker

RUN pip install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000
COPY . .
CMD exec gunicorn --bind 0.0.0.0:5000 --workers 5 --threads 3 app:app