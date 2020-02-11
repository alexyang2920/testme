bind = [":8080","unix:var/testme.sock"]
worker_class = 'gevent'
workers = 2
preload_app = False
accesslog = "-"
loglevel = 'info'
timeout = 1800
