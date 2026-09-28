from flask import Blueprint

from app.controllers.monitor_controller import MonitorController

monitors_bp = Blueprint("monitors", __name__)


# GET /v1/monitors - Получить все мониторы
@monitors_bp.route("/v1/monitors", methods=["GET"])
def get_monitors():
    return MonitorController.get_monitors()


# POST /v1/monitors - Создать новый монитор
@monitors_bp.route("/v1/monitors", methods=["POST"])
def create_monitor():
    return MonitorController.create_monitor()


# GET /v1/monitors/<id> - Получить монитор по ID
@monitors_bp.route("/v1/monitors/<monitor_id:monitor_id>", methods=["GET"])
def get_monitor(monitor_id):
    return MonitorController.get_monitor_by_id(monitor_id)


# PUT /v1/monitors/<id> - Обновить параметры монитора
@monitors_bp.route("/v1/monitors/<monitor_id:monitor_id>", methods=["PUT"])
def update_monitor(monitor_id):
    return MonitorController.update_monitor(monitor_id)


# DELETE /v1/monitors/<id> - Удалить монитор
@monitors_bp.route("/v1/monitors/<monitor_id:monitor_id>", methods=["DELETE"])
def delete_monitor(monitor_id):
    return MonitorController.delete_monitor(monitor_id)


# GET /v1/monitors/<id>/logs - История пингов
@monitors_bp.route("/v1/monitors/<monitor_id:monitor_id>/logs", methods=["GET"])
def get_logs(monitor_id):
    return MonitorController.get_monitor_logs(monitor_id)


# POST /v1/monitors/<id>/check - Ручной пинг прямо сейчас
@monitors_bp.route("/v1/monitors/<monitor_id:monitor_id>/check", methods=["POST"])
def manual_check(monitor_id):
    return MonitorController.trigger_manual_check(monitor_id)


# GET /v1/monitors/<id>/stats - Статистика (аптайм % и пинг)
@monitors_bp.route("/v1/monitors/<monitor_id:monitor_id>/stats", methods=["GET"])
def get_stats(monitor_id):
    return MonitorController.get_monitor_stats(monitor_id)
