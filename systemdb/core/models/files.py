from systemdb.core.extentions import db


class ImportedFile(db.Model):
    __tablename__ = "ImportedFile"
    id = db.Column(db.Integer, primary_key=True)
    Hash = db.Column(db.String, unique=True, nullable=False)
