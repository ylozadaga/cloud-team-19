FROM ubuntu:22.04
WORKDIR /app
RUN mkdir -p /app/file_storage/input /app/file_storage/output
RUN chown -R nobody:nogroup /app
RUN chmod -R 777 /app
RUN apt -y update && apt -y upgrade && apt -y install python3 python3-pip python3.10-venv python3-dev build-essential libssl-dev libffi-dev python3-setuptools python-is-python3 systemctl nfs-kernel-server
