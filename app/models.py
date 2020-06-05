from .extensions import db


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    password_hash = db.Column(db.Unicode)
    email = db.Column(db.Unicode, nullable=False, unique=True)
    first_name = db.Column(db.Unicode, nullable=False)
    last_name = db.Column(db.Unicode, nullable=False)
    registered_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.text("statement_timestamp()"),
    )
