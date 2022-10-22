FROM ubuntu:22.04
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
COPY /convertion_tool /app
RUN apt update && apt -y upgrade && apt -y install python3 && apt install -y python3-pip && apt install python-is-python3
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]
