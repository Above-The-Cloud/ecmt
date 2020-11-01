if [ ! -d "/data/log/ecmt" ];then
    mkdir -p /data/log/ecmt
fi
if [ ! -f "/data/log/ecmt/uwsgi.log" ];then
    touch /data/log/ecmt/uwsgi.log
fi

if [ ! -d "/data/app" ];then
    mkdir -p /data/app
fi
if [ ! -d "/data/app/ecmt" ];then
    cd /data/app
    yes|git clone git@github.com:Above-The-Cloud/ecmt.git
fi
chmod -R 777 /data/app/ecmt
cd /data/app/ecmt
rm -f config.json
echo '{
  "appName": "ecmt",
  "database": {
    "name": "ecmt",
    "user": "root",
    "password": "123456",
    "host": "127.0.0.1",
    "port": "3306"
  }
}' > config.json

git checkout .
git checkout master
git pull origin master

rm -f /etc/nginx/sites-enabled/ecmt.yiwangchunyu.wang.conf
ln -s /data/app/ecmt/ecmt.yiwangchunyu.wang.conf /etc/nginx/sites-enabled/ecmt.yiwangchunyu.wang.conf

if [ ! -d "uwsgi" ];then
    mkdir -p uwsgi
fi
if [ ! -f "uwsgi/uwsgi.pid" ];then
    uwsgi --ini uwsgi.ini
else
    uwsgi --reload uwsgi/uwsgi.pid
fi
nginx -s reload