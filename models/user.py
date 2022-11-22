from models import Model


class User(Model):
    def __init__(self, form: dict):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def salted_password(self, password, salt='!@#$%^^&&*'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    @classmethod
    def register(cls, form: dict):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_by(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        return None

    @classmethod
    def validate_login(cls, form: dict):
        u = User(form)
        user = u.find_by(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        return None
