from flask import Flask
import config
from routes.todo import main as todo_routes
from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes


app = Flask(__name__)
app.secret_key = config.secret_key
app.register_blueprint(index_routes)
app.register_blueprint(topic_routes, url_prefix='/topic')
app.register_blueprint(reply_routes, url_prefix='/reply')
app.register_blueprint(board_routes, url_prefix='/board')
# app.register_blueprint(todo_routes, url_prefix='/todo')


if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2001,
    )
    app.run(**config)