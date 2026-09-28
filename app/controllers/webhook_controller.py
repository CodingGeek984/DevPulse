from flask import jsonify, request

from app.extensions import db
from app.models.webhook import Webhook
from app.utils.validators import as_text, json_body


class WebhookController:

    @staticmethod
    def get_webhooks():

        webhooks = Webhook.query.order_by(Webhook.id).all()

        return jsonify([webhook.to_dict() for webhook in webhooks]), 200

    @staticmethod
    def delete_webhooks():

        deleted = Webhook.query.delete()
        db.session.commit()

        if not deleted:
            return jsonify({"message": "Webhooks not found"}), 404

        return jsonify({
            "message": "webhooks deleted successfully",
            "deleted": deleted,
        }), 200

    @staticmethod
    def save_history():

        data = json_body()

        if data is None:
            return jsonify({"error": "Request body must be a JSON object"}), 400

        try:
            source = as_text(data.get("source"), "source", 80)
            message = as_text(data.get("message"), "message", 10000)
            level = as_text(data.get("level") or "info", "level", 20).lower()
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

        webhook = Webhook(
            source=source,
            message=message,
            level=level,
            payload=data.get("payload"),
        )

        db.session.add(webhook)
        db.session.commit()

        return jsonify({
            "message": "Webhook saved",
            "webhook": webhook.to_dict(),
        }), 201
