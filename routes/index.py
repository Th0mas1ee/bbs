from flask import (
    render_template,
    url_for,
    request,
    redirect,
    session,
    Blueprint,
    send_from_directory,
)
from werkzeug.utils import secure_filename
from models.user import User
from routes import current_user
from config import user_file_directory
import os
from utils import log

main = Blueprint('index', __name__)


@main.route('/')
def index():
    u = current_user()
    return render_template('index.html', user=u)


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('topic.index'))
    else:
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


def allow_file(filename: str):
    suffix = filename.split('.')[-1]
    from config import accpet_user_file_type
    return suffix in accpet_user_file_type


@main.route('/add_img', methods=['POST'])
def add_img():
    u = current_user()
    if u is None:
        return redirect(url_for('.profile'))
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if allow_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_file_directory, filename))
        u.user_image = filename
        u.save()
    return redirect(url_for('.profile'))


@main.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(user_file_directory, filename)
