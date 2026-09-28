from datetime import datetime, timedelta, timezone

from flask import jsonify, request
from sqlalchemy import func

from app.extensions import db
from app.models.monitor import Monitor
from app.models.PingLog import PingLog
from app.utils.checker import check_url
from app.utils.validators import as_bool, as_int, as_text, json_body


class MonitorController:

    @staticmethod
    def get_monitors():

        monitors = Monitor.query.order_by(Monitor.id).all()

        return jsonify([monitor.to_dict() for monitor in monitors]), 200

    @staticmethod
    def create_monitor():

        data = json_body()

        if data is None:
            return jsonify({"error": "Request body must be a JSON object"}), 400

        try:
            name = as_text(data.get("name"), "name", 160)
            url = as_text(data.get("url"), "url", 500)
            interval_seconds = as_int(data.get("interval_seconds", 30), "interval_seconds", 1, 86400)
            expected_status = as_int(data.get("expected_status", 200), "expected_status", 100, 599)
            is_active = as_bool(data["is_active"]) if "is_active" in data else True
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

        monitor = Monitor(
            name=name,
            url=url,
            interval_seconds=interval_seconds,
            expected_status=expected_status,
            is_active=is_active,
        )

        db.session.add(monitor)
        db.session.commit()

        return jsonify({
            "message": "Monitor created",
            "monitor": monitor.to_dict(),
        }), 201

    @staticmethod
    def get_monitor_by_id(monitor_id):

        monitor = db.session.get(Monitor, monitor_id)

        if not monitor:
            return jsonify({"error": "Monitor not found"}), 404

        return jsonify({"monitor": monitor.to_dict()}), 200

    @staticmethod
    def update_monitor(monitor_id):

        monitor = db.session.get(Monitor, monitor_id)

        if not monitor:
            return jsonify({"error": "Monitor not found"}), 404

        data = json_body()

        if data is None:
            return jsonify({"error": "Request body must be a JSON object"}), 400

        try:
            if "name" in data:
                monitor.name = as_text(data["name"], "name", 160)

            if "url" in data:
                monitor.url = as_text(data["url"], "url", 500)

            if "interval_seconds" in data:
                monitor.interval_seconds = as_int(data["interval_seconds"], "interval_seconds", 1, 86400)

            if "expected_status" in data:
                monitor.expected_status = as_int(data["expected_status"], "expected_status", 100, 599)

            if "is_active" in data:
                monitor.is_active = as_bool(data["is_active"])
        except ValueError as exc:
            db.session.rollback()
            return jsonify({"error": str(exc)}), 400

        db.session.commit()

        return jsonify(monitor.to_dict()), 200

    @staticmethod
    def delete_monitor(monitor_id):

        monitor = db.session.get(Monitor, monitor_id)

        if not monitor:
            return jsonify({"error": "Monitor not found"}), 404

        PingLog.query.filter_by(monitor_id=monitor_id).delete()
        db.session.delete(monitor)
        db.session.commit()

        return jsonify({"message": "Monitor deleted"}), 200

    @staticmethod
    def get_monitor_logs(monitor_id):

        monitor = db.session.get(Monitor, monitor_id)

        if not monitor:
            return jsonify({"error": "Monitor not found"}), 404

        limit = min(max(request.args.get("limit", 100, type=int) or 100, 1), 1000)

        logs = (
            PingLog.query.filter_by(monitor_id=monitor_id)
            .order_by(PingLog.timestamp.desc(), PingLog.id.desc())
            .limit(limit)
            .all()
        )

        return jsonify([log.to_dict() for log in logs]), 200

    @staticmethod
    def trigger_manual_check(monitor_id):

        monitor = db.session.get(Monitor, monitor_id)

        if not monitor:
            return jsonify({"error": "Monitor not found"}), 404

        result = check_url(monitor.url, monitor.expected_status)

        log = PingLog(
            monitor_id=monitor.id,
            status_code=result["status_code"],
            response_time_ms=result["response_time_ms"],
            is_up=result["is_up"],
            error_message=result["error_message"],
        )

        monitor.pings = (monitor.pings or 0) + 1

        db.session.add(log)
        db.session.commit()

        return jsonify({
            "monitor_id": monitor.id,
            "is_up": log.is_up,
            "status_code": log.status_code,
            "response_time_ms": log.response_time_ms,
            "error_message": log.error_message,
            "pings": monitor.pings,
            "ping": log.to_dict(),
        }), 200

    @staticmethod
    def get_monitor_stats(monitor_id):

        monitor = db.session.get(Monitor, monitor_id)

        if not monitor:
            return jsonify({"error": "Monitor not found"}), 404

        time_24h_ago = datetime.now(timezone.utc) - timedelta(hours=24)

        total_pings = PingLog.query.filter(
            PingLog.monitor_id == monitor_id,
            PingLog.timestamp >= time_24h_ago,
        ).count()

        successful_pings = PingLog.query.filter(
            PingLog.monitor_id == monitor_id,
            PingLog.timestamp >= time_24h_ago,
            PingLog.is_up.is_(True),
        ).count()

        uptime_percentage = round((successful_pings / total_pings) * 100, 2) if total_pings > 0 else 100.0

        avg_latency = db.session.query(func.avg(PingLog.response_time_ms)).filter(
            PingLog.monitor_id == monitor_id,
            PingLog.timestamp >= time_24h_ago,
            PingLog.is_up.is_(True),
        ).scalar()

        return jsonify({
            "monitor_id": monitor.id,
            "name": monitor.name,
            "period": "24h",
            "total_checks": total_pings,
            "successful_checks": successful_pings,
            "uptime_percentage": uptime_percentage,
            "avg_response_time_ms": round(avg_latency, 2) if avg_latency is not None else 0.0,
        }), 200
