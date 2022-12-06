FROM ubuntu:22.04
WORKDIR /convertion_tool
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV VIRTUAL_ENV=/convertion_tool/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY . .
COPY convertion-tool.service /etc/systemd/system/convertion-tool.service
COPY convertion-tool /etc/nginx/sites-available/convertion-tool
RUN mkdir -p /convertion_tool/file_storage
RUN chown -R root:www-data /convertion_tool
RUN chmod -R 777 /convertion_tool
RUN apt -y update && apt -y upgrade && apt -y install python3 python3-pip python3-venv python3-dev build-essential libssl-dev libffi-dev python3-setuptools python-is-python3 systemctl nginx
RUN python -m venv $VIRTUAL_ENV
RUN . $VIRTUAL_ENV/bin/activate
RUN pip install -r requirements.txt
RUN ln -s /etc/nginx/sites-available/convertion-tool /etc/nginx/sites-enabled/
RUN nginx -t
RUN systemctl start convertion-tool
RUN systemctl enable convertion-tool
RUN systemctl start nginx
RUN systemctl enable nginx
RUN systemctl daemon-reload
RUN systemctl restart convertion-tool
RUN systemctl restart nginx
EXPOSE 8080