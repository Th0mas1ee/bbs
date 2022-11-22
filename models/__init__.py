import json
from utils import log


def save(data, path):
    """
    :param data: dict or list
    :param path: directory for saving
    :return:
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        log('Before read')
        s = f.read()
        log(f's:({s})')
        return json.loads(s)


class Model(object):
    @classmethod
    def db_path(cls):
        class_name = cls.__name__
        path = f'data/{class_name}.txt'
        return path

    @classmethod
    def _new_from_dict(cls, d):
        m = cls({})
        for k, v in d.items():
            setattr(m, k, v)
        return m

    @classmethod
    def new(cls, form: dict, **kwargs):
        m = cls(form)
        for k, v in kwargs.items():
            setattr(m, k, v)
        m.save()
        return m

    @classmethod
    def all(cls):
        path = cls.db_path()
        # log(f'path:({path})')
        models = load(path)
        # log(f'models:({models})')
        ms = [cls._new_from_dict(m) for m in models]
        return ms

    @classmethod
    def find_all(cls, **kwargs):
        ms = []
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                ms.append(m)
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def delete(cls, id):
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        if index != -1:
            obj = models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)
            return obj

    def __repr__(self):
            class_name = self.__class__.__name__
            properties = [f'{k}, ({v})' for k, v in self.__dict__.items()]
            s = '\n'.join(properties)
            return f'< {class_name}\n{s} \n>\n'

    def json(self):
        d = self.__dict__.copy()
        return d

    def save(self):
        models = self.all()
        if self.id is None:
            if len(models) == 0:
                self.id = 1
            else:
                m = models[-1]
                self.id = m.id + 1
            models.append(self)
        else:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            models[index] = self
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)