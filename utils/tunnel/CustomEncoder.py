import json
from TunnelPoint import TunnelPoint

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, TunnelPoint):
            return obj.to_dict()  # Use the to_dict() method for serialization
        return super().default(obj)  # Use default encoding for other objects