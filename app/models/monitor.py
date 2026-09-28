from datetime import datetime, timezone

from app.extensions import db


class Monitor(db.Model):
    __tablename__ = "monitors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    interval_seconds = db.Column(db.Integer, default=30)
    expected_status = db.Column(db.Integer, default=200)
    is_active = db.Column(db.Boolean, default=True)
    pings = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __init__(
        self,
        name,
        url,
        interval_seconds=30,
        expected_status=200,
        is_active=True,
        pings=0,
    ):
        self.name = name
        self.url = url
        self.interval_seconds = interval_seconds
        self.expected_status = expected_status
        self.is_active = is_active
        self.pings = pings

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "interval_seconds": self.interval_seconds,
            "expected_status": self.expected_status,
            "is_active": self.is_active,
            "pings": self.pings,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
