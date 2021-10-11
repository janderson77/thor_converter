from app import app
from livereload import Server

app.debug = False

if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve()
