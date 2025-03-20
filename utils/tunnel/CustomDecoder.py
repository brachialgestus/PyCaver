from TunnelPoint import TunnelPoint

class CustomDecoder:
    # Custom decoder to convert JSON dicts back to TunnelPoint objects
    def tunnelpoint_decoder(d):
        if "x" in d and "y" in d and "z" in d and "radius" in d:  # Detect TunnelPoint structure
            return TunnelPoint(d["x"], d["y"], d["z"], d["radius"])
        return d  # Return unchanged if it's not a TunnelPoint