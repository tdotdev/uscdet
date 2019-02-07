from app import app

from bokeh.embed import server_document
from bokeh.server.server import Server
import threading
from tornado.ioloop import IOLoop

FLASK_PORT = '5000'
BOKEH_PORT = '5006'

def get_url(port):
    return f"localhost:{port}" 

def status():
    return 'online'

def bokeh_server_worker():
    bk_server = Server(
        {},
        io_loop=IOLoop(),
        allow_websocket_origin=[
            get_url(FLASK_PORT),
            get_url(BOKEH_PORT)
        ]
    )
    bk_server.start()
    bk_server.io_loop.start()

if __name__ == '__main__':
    threading.Thread(target=bokeh_server_worker).start()
    app.run()