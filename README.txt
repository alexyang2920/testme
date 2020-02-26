testme
======

Getting Started
---------------

- Change directory into your newly created project.

    cd testme

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Run your project's tests.

    env/bin/pytest

- Run your project.

    env/bin/pserve development.ini

- Send Email
	qp --config qp.ini
	https://docs.pylonsproject.org/projects/pyramid-mailer/en/latest/#queue

- Start supervisor
    supervisord -n

- github
	ssh-add -K ~/.ssh/id_rsa_zpyang2920

- nginx
	brew install nginx
	nginx -h

	# stop
	nginx -s stop -c /Users/alexyang/Documents/exp/zope_hacking/project/testme/etc/nginx/nginx.conf

	# start
	nginx -c /Users/alexyang/Documents/exp/zope_hacking/project/testme/etc/nginx/nginx.conf

	# config ref:
	https://www.cnblogs.com/xiaogangqq123/archive/2011/03/02/1969006.html
	https://blog.csdn.net/physicsdandan/article/details/45667357

	https://www.digitalocean.com/community/questions/configure-nginx-for-nodejs-backend-and-react-frontend-app


- redis
	https://redis.io/topics/quickstart
	steps:
		wget http://download.redis.io/redis-stable.tar.gz
		tar xvzf redis-stable.tar.gz
		cd redis-stable
		make

		cp redis-server ~/VirtualEnvs/testme/bin
		cp redis-cli ~/VirtualEnvs/testme/bin
