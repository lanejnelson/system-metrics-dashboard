from config import db

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(80), unique=False, nullable=False)
    operating_sys = db.Column(db.String(80), unique=False, nullable=False)
    cpu_usage = db.Column(db.Integer, unique=False, nullable=False)
    memory_usage = db.Column(db.Float, unique=False, nullable=False)
    disk_usage = db.Column(db.Float, unique=False, nullable=False)
    #network_usage = db.Column(db.Float, unique=False, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "hostname": self.hostname,
            "operatingSys": self.operating_sys,
            "cpuUsage": self.cpu_usage,
            "memoryUsage": self.memory_usage,
            "diskUsage": self.disk_usage,
            #"currentDiskUsage": self.current_disk_usage,
            #"storagePercentage": self.storage_percentage,
            #"networkUsage": self.network_usage
        }