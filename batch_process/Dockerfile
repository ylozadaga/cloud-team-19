FROM ubuntu:22.04
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
COPY /convertion_tool .
RUN mkdir -p /app/file_storage/input /app/file_storage/output
RUN chown -R root:www-data /app
RUN chmod -R 775 /app
RUN apt -y update && apt -y upgrade && apt -y install python3 python3-pip python3.10-venv python3-dev build-essential libssl-dev libffi-dev python3-setuptools python-is-python3 systemctl nginx ffmpeg redis-server
RUN python -m venv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt
COPY flask.conf /etc/nginx/conf.d/flask.conf
RUN chmod 777 run.sh
EXPOSE 8080
CMD ./run.sh
