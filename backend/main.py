from flask import request, jsonify
from config import app, db
from flask_sqlalchemy import SQLAlchemy
from models import Log
import json

@app.route('/build/agent/<string:os>', methods=["GET"])
def build_agent():
    return "Not Implemented Yet"

@app.route('/metrics', methods=["GET"])
def get_last_logs():
    # show only last 3 queries
    stmt = db.select(Log).order_by(Log.id.desc()).limit(3)
    last_three_logs = db.session.scalars(stmt).all()
    print(stmt)
    json_logs = list(map(lambda x: x.to_json(), last_three_logs))
    return jsonify({"logs": json_logs})

@app.route('/send_metrics', methods=["POST"])
def receive_metrics():
    print(request.json)
    hostname = request.json.get("hostname")
    operating_sys = request.json.get("operatingSys")
    total_memory = request.json.get("totalMemory")
    free_memory = request.json.get("freeMemory")
    memory_usage = round(((total_memory - free_memory) / total_memory) * 100, 3)
    disk_size = request.json.get("diskSize")
    free_disk_space = request.json.get("freeDiskSpace")
    disk_usage = round(((disk_size - free_disk_space) / disk_size) * 100, 3)
    cpu_usage = request.json.get("cpuUsage")
    new_log = Log(cpu_usage=cpu_usage, hostname=hostname, operating_sys=operating_sys, memory_usage=memory_usage, disk_usage=disk_usage)
    critical_events = detect_critical_events(new_log.to_json())
    if (critical_events):
        # send to Postgres
        print(critical_events)
        pass
    else:
        #send to redis
        pass
    #print(new_log.to_json())
    try:
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        return (jsonify({"message": str(e)}), 400)
    return (jsonify({"message": "Log successfully added!"}), 200)


def detect_critical_events(metric: dict):
    critical_events = []
    print(metric)
    for key in metric.keys():
        # Check if metric is above 85% and add high_metric to list
        if key != "id" and key != "hostname" and key != "operatingSys" and type(metric[key]) is not None and metric[key] > 85:
            critical_events.append("high_" + key)
    return critical_events

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)