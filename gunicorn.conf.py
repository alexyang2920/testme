bind = [":8080","unix:var/testme.sock"]
worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
workers = 2
preload_app = False
accesslog = "-"
loglevel = 'info'
timeout = 1800
