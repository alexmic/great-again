#!/usr/bin/env python

from gevent.monkey import patch_all

patch_all()

from gevent.wsgi import WSGIServer
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication

from ga.app import create_app


app = create_app()


if __name__ == '__main__':
    @run_with_reloader
    def run(interface='0.0.0.0', port=8000):
        print u" * Server is running at %s:%s" % (interface, port)

        wsgi = DebuggedApplication(app)

        http_server = WSGIServer((interface, port), wsgi)
        http_server.serve_forever()
