import time
from models import Model


class Topic(Model):
    @classmethod
    def get(cls, id):
        t = cls.find_by(id=id)
        t.views += 1
        t.save()
        return t

    def __init__(self, form: dict):
        self.id = None
        self.views = 0
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.created_time = int(time.time())
        self.updated_time = self.created_time
        self.user_id = form.get('user_id', -1)

    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id=self.id)
        return ms
