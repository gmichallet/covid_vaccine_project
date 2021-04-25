def create_classes(db):
    class vaccine(db.Model):
        __tablename__ = 'vaccine'

        id = db.Column(db.Integer)
        age = db.Column(db.Integer)
        gender = db.Column(db.String)
        brand = db.Column(db.String)
        symptom = db.Column(db.String)
        lat = db.Column(db.Float)
        lon = db.Column(db.Float)

        def __repr__(self):
            return '<vaccine %r>' % (self.age)
    return vaccine
