import time
from models import Model


class Todo(Model):
    @classmethod
    def new(cls, form):
        t = cls(form)
        t.save()
        return t

    @classmethod
    def update(cls, id, form):
        t = cls.find(id)
        valid_names = [
            'title',
            'completed',
        ]
        for key in form:
            if key in valid_names:
                setattr(t, key, form[key])
        t.save()
        return t

    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.completed = False
        self.ct = int(time.time())
        self.ut = self.ct