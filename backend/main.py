from flask import request, jsonify
from config import app, db
from flask_sqlalchemy import SQLAlchemy
from models import Log
import json
from config import r

@app.route('/build/agent/<string:os>', methods=["GET"])
def build_agent():
    return "Not Implemented Yet"

@app.route('/metrics', methods=["GET"])
def get_last_logs():
    stmt = db.select(Log).order_by(Log.id.desc()).limit(10)
    last_three_logs = db.session.scalars(stmt).all()
    #print(stmt)
    json_logs = list(map(lambda x: x.to_json(), last_three_logs))
    #print(json_logs)
    return jsonify({"logs": json_logs})

@app.route('/api/events', methods=["GET"])
def get_logs_from_redis():
    logs = r.xrevrange("logs", "+", "-", count=10)
    result = []
    for log_id, data in logs:
        result.append({
            "id": log_id,
            "level": data.get("level"),
            "host_id": data.get("host_id"),
            "event_type": data.get("event_type"),
            "metric": data.get("metric"),
            "value": data.get("value"),
            "message": data.get("message")
        })
    #print(result)
    return jsonify({"events": result})

@app.route('/send_metrics', methods=["POST"])
def receive_metrics():
    print(request.json)
    host_id = request.json.get("hostID")
    timestamp = request.json.get("timestamp")
    hostname = request.json.get("hostname")
    operating_sys = request.json.get("operatingSys")
    total_memory = request.json.get("totalMemory")
    free_memory = request.json.get("freeMemory")
    memory_usage = round(((total_memory - free_memory) / total_memory) * 100, 2)
    disk_size = request.json.get("diskSize")
    free_disk_space = request.json.get("freeDiskSpace")
    disk_usage = round(((disk_size - free_disk_space) / disk_size) * 100, 2)
    cpu_usage = round(request.json.get("cpuUsage"), 2)
    new_log = Log(host_id=host_id, timestamp=timestamp, cpu_usage=cpu_usage, hostname=hostname, operating_sys=operating_sys, memory_usage=memory_usage, disk_usage=disk_usage)
    critical_events = detect_critical_events(new_log.to_json())
    #print(new_log.to_json())
    try:
        db.session.add(new_log)
        db.session.commit()
        if (critical_events):
                # send to Postgres and redis
                for event in critical_events:
                    send_log(r, "WARNING", host_id=host_id, message=f"{event['metric']}", event_type=event["event_type"], metric=event['metric'], value=event["value"])
    except Exception as e:
        db.session.rollback()
        print("ERROR: ", repr(e))
        return (jsonify({"message": str(e)}), 400)
    return (jsonify({"message": "Log successfully added!"}), 200)

def detect_critical_events(metric: dict):
    critical_events = []
    print(metric)
    for key, value in metric.items():
        # Check if metric is above 85% and add high_metric to list
        if value is not None and 'usage' in key.lower() and value > 85:
            critical_events.append({
                "event_type": "high_" + key,
                "metric": key,
                "value": value
            })
    #print(critical_events)
    return critical_events

def send_log(redis_connection, level, host_id, message, event_type, metric, value):
    redis_connection.xadd("logs", {
        "level": level,
        "host_id": host_id,
        "event_type": event_type,
        "metric": metric,
        "value": str(value),
        "message": message
    })


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)