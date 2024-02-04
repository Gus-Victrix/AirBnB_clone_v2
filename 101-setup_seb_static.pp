#Make the tsk 0 under puppet
exec {'/usr/bin/env apt-get -y update' : }
-> exec {'/usr/bin/env apt-get -y install nginx' : }
-> exec {'/usr/bin/env mkdir -p /data/web_static/releases/test' : }
-> exec {'/usr/bin/env mkdir -p /data/web_static/shared' : }
-> exec {'/usr/bin/env echo "Hello world" > /data/web_static/releases/test/index.html' : }
-> exec {'/usr/bin/env ln -sf /data/web_static/releases/test/ /data/web_static/current' : }
-> exec {'/usr/bin/env chown -hR ubuntu:ubuntu /data/' : }
-> exec {'/usr/bin/env sed -i "38i\\\tlocation /hbnb_static/ {\n\t\t alias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default' : }
-> exec {'/usr/bin/env service nginx restart' : }
