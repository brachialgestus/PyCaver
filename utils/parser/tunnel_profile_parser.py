import os

def parse_tunnel_profiles(path : str) -> dict:
    """
    Parse the tunnel profiles from the tunnel_profiles.json file.
    :input: path to the tunnel_profiles.csv
    :return: The tunnel profiles.
    """
    res = {}

    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} not found.")
    with open(path, 'r') as f:
        lines = f.readlines()
        # Skipt first line -> header
        for i in range(1, len(lines), 7):
            x_row = lines[i].split(',')
            y_row = lines[i+1].split(',')
            z_row = lines[i+2].split(',')
            distance_row = lines[i+3].split(',')
            length_row = lines[i+4].split(',')
            r_row = lines[i+5].split(',')
            r_error_bound_row = lines[i+6].split(',')
                        
            # get tunnel id and tunnel cluster
            tunnel_cluster = int(x_row[1].strip())

            # check if all rows have the same length
            if len(x_row) != len(y_row) or len(y_row) != len(z_row) or len(z_row) != len(distance_row) or len(distance_row) != len(length_row) or len(length_row) != len(r_row) or len(r_row) != len(r_error_bound_row):
                raise ValueError(f"Rows have different lengths: {len(x_row)}, {len(y_row)}, {len(z_row)}, {len(distance_row)}, {len(length_row)}, {len(r_row)}, {len(r_error_bound_row)}")
            
            x_values = []
            y_values = []
            z_values = []
            distance_values = []
            length_values = []
            r_values = []

            for j in range(13,len(x_row)):
                x_values.append(float(x_row[j]))
                y_values.append(float(y_row[j]))
                z_values.append(float(z_row[j]))
                distance_values.append(float(distance_row[j]))
                length_values.append(float(length_row[j]))
                r_values.append(float(r_row[j]))

            tunnel_profile = {
                'x': x_values,
                'y': y_values,
                'z': z_values,
                'distance': distance_values,
                'length': length_values,
                'r': r_values
            }
            
            # append tunnel profile to tunnel with cluster_id or tunnel_id
            res[tunnel_cluster] = tunnel_profile

    return res