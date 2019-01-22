import json
from datetime import datetime


class VideoStatsDto:
    """
    describes, stores and serializes video motion stats
    """
    name = ""
    values = []
    total = 0
    duration_total = 0
    start_time = ""
    date_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self):
        self.name = ""
        self.values = []
        self.start_time = ""
        self.total = 0
        self.frames_total = 0
        self.duration_total = 0
        self.date_format = '%Y-%m-%d %H:%M:%S'

    def set(self, k, v):
        setattr(self, k, v)

    def get_all(self):
        return self.__class__.__dict__

    def unserialize(self, json_str):
        if json_str:
            d = json.loads(json_str)

            self.values = d["values"]
            self.duration_total = d["total_duration"]
            self.frames_total = d["clip_frames_total"]
            self.total = d["total"]
            self.start_time = d["start_time"]
            self.start_time = datetime.strptime(d["start_time"], self.date_format)

    def serialize(self):
        final = {
            "values": self.values,
            "total_duration": self.duration_total,
            "total": self.total,
            "name": self.name,
            "clip_frames_total": self.frames_total,
            "start_time": self.start_time
        }

        return json.dumps(final)
