#!/usr/bin/env bash
# Install nginx and create folders
# Update apt repositories
apt-get update
# Install nginx
apt-get -y install nginx
# Create folders
mkdir -p /data/web_static/{releases/test/,shared}
# Create simple html file
echo "Holberton School" > /data/web_static/releases/test/index.html
# Create symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current
# Give ownership of the /data/ folder to the ubuntu user AND group
chown -hR ubuntu:ubuntu /data/
# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
sed -i "38i \tlocation /hbnb_static/ {\n \t\talias /data/web_static/current/;\n\t}" /etc/nginx/sites-available/default
# Restart nginx
service nginx restart
