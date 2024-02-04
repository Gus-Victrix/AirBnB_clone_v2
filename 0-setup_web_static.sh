#!/usr/bin/env bash
#Preconfigure the server to put our static web

apt-get -y update
apt-get -y install nginx
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared
echo "Hello world" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -hR ubuntu:ubuntu /data/
sed -i "38i\\\tlocation /hbnb_static/ {\n\t\t alias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default
service nginx restart
