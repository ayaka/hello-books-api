from app import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    books = db.relationship("Books", back_populates="author")

    @classmethod
    def from_dict(cls, author_dict):
        return Author(**author_dict)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }