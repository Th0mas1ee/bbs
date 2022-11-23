import time
from models import Model


class Board(Model):
    def __init__(self, form: dict):
        self.id = None
        self.title = form.get('title', '')
        self.created_time = int(time.time())
        self.updated_time = self.created_time
