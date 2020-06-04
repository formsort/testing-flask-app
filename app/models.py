from sqlalchemy.dialects import postgresql

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


class Extraction(db.Model):
    __bind_key__ = "two"
    id = db.Column(db.Integer, primary_key=True, index=True)
    account_id = db.Column(db.Integer, index=True)
    sensor_data = db.Column(postgresql.JSONB(none_as_null=True))
