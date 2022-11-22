from flask import (
    request,
    render_template,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.topic import Topic


main = Blueprint('topic', __name__)


@main.route('/')
def index():
    ms = Topic.all()
    return render_template('topic/index.html', ms=ms)


@main.route('/new')
def new():
    return render_template('topic/new.html')


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    return render_template('topic/detail.html', topic=m)