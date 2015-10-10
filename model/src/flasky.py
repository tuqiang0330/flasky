from .database import db

user_label = db.Table('user_label',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('label_id', db.Integer, db.ForeignKey('label.id')),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    password = db.Column(db.String(64))

    article_list = db.relationship('Article', lazy='dynamic')
    label_list = db.relationship('Label', secondary=user_label, lazy='dynamic')

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User: %d, %s>' % (self.id, self.name)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', lazy='select')

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return '<Address: %d, %s>' % (self.id, self.title)


class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    user_list = db.relationship('User', secondary=user_label, lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Label: %d, %s>' % (self.id, self.name)
