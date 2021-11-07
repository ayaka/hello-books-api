from app import db

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    books = db.relationship("Book", secondary="books_genres", back_populates="genres")

    @classmethod
    def from_dict(cls, genre_dict):
        return Genre(name = genre_dict["name"])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }