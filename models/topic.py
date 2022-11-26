import time
from models import Model
from models.user import User


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
        self.user_id = int(form.get('user_id', -1))
        self.board_id = int(form.get('board_id', -1))

    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id=self.id)
        return ms

    def board(self):
        from .board import Board
        m = Board.find(self.board_id)
        return m

    def user(self):
        u = User.find(id=self.user_id)
        return u
