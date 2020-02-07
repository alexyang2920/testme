bind = [":8080","unix:var/testme.sock"]
worker_class = 'gevent'
workers = 2
preload = True
accesslog = "-"
loglevel = 'info'
timeout = 1800
