from app import db

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), index=True, unique=True)
    keyword = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Page {} with keyword {}>'.format(self.filename, self.keyword)
