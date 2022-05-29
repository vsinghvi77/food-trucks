class ProtocolPayload:
    def __init__(self, status, payload):
        self.status = status
        self.payload = payload
    def to_json(self):
        return f"""
        {{
            "status":"{self.status}",
            "payload":{self.payload}
        }}
        """

class ProtocolSearchPayload:
    def __init__(self, total_count, data):
        self.total_count = total_count
        self.data = data
    def to_json(self):
        return f"""
        {{
            "tc":"{self.total_count}",
            "data":{self.data}
        }}
        """