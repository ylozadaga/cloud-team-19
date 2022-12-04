#!/bin/sh
ln -s /etc/nginx/sites-available/convertion-tool /etc/nginx/sites-enabled
systemctl start convertion-tool
systemctl enable convertion-tool
systemctl daemon-reload
systemctl restart convertion-tool
systemctl restart nginx