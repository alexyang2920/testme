
bind = [":8080","unix:var/testme.sock"]
worker_class = 'gevent'
workers = 1
preload = True
accesslog = "-"
loglevel = 'info'
