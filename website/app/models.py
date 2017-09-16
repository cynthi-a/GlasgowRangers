from app import db

def create_from_names(output_names):
    for i, name in enumerate(output_names):
        page = Page(filename=name, keyword=str(i+1))
        db.session.add(page)
        db.session.commit()

def delete_all():
    for page in Page.query.all():
        db.session.delete(page)
        db.session.commit()

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), index=True, unique=True)
    keyword = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Page {} with keyword {}>'.format(self.filename, self.keyword)
