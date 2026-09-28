from datetime import datetime, timezone

from app.extensions import db


class PingLog(db.Model):
    __tablename__ = "ping_logs"

    id = db.Column(db.Integer, primary_key=True)
    monitor_id = db.Column(db.Integer, db.ForeignKey("monitors.id"), nullable=False)
    status_code = db.Column(db.Integer, nullable=True)
    response_time_ms = db.Column(db.Float, nullable=True)
    is_up = db.Column(db.Boolean, nullable=False)
    error_message = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "monitor_id": self.monitor_id,
            "status_code": self.status_code,
            "response_time_ms": self.response_time_ms,
            "is_up": self.is_up,
            "error_message": self.error_message,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }
