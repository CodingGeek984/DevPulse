from datetime import datetime, timezone

from app.extensions import db


class Webhook(db.Model):
    __tablename__ = "webhooks"

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(80), nullable=False)
    level = db.Column(db.String(20), default="info")
    message = db.Column(db.Text, nullable=False)
    payload = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __init__(self, source, message, level="info", payload=None):
        self.source = source
        self.message = message
        self.level = level
        self.payload = payload

    def to_dict(self):
        return {
            "id": self.id,
            "source": self.source,
            "level": self.level,
            "message": self.message,
            "payload": self.payload,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
