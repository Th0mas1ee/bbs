import time
from models import Model


class Reply(Model):
    def __init__(self, form: dict):
        self.id = None
        self.content = form.get('content', '')
        self.created_time = int(time.time())
        self.updated_time = self.created_time
        self.topic_id = int(form.get('topic_id', -1))

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u
