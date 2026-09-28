from flask import Blueprint

from app.controllers.webhook_controller import WebhookController

webhooks_bp = Blueprint("webhooks", __name__)


# GET /v1/webhooks - Получить все записи вебхуков
@webhooks_bp.route("/v1/webhooks", methods=["GET"])
def get_webhooks():
    return WebhookController.get_webhooks()


# DELETE /v1/webhooks - Удалить все записи вебхуков
@webhooks_bp.route("/v1/webhooks", methods=["DELETE"])
def delete_webhooks():
    return WebhookController.delete_webhooks()


# POST /v1/webhooks - Сохранить входящий вебхук
@webhooks_bp.route("/v1/webhooks", methods=["POST"])
def save_history():
    return WebhookController.save_history()
