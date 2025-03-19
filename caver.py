import argparse
import os
import subprocess
import uuid
import shutil

import shlex

CONFIG_SAMPLE = """
#*****************************
# CALCULATION SETUP      
#*****************************
load_tunnels no
load_cluster_tree no
stop_after never

#*****************************
# INPUT DATA       
#*****************************
time_sparsity 1
first_frame 1
last_frame 100000

#*****************************
# TUNNEL CALCULATION
#*****************************

#starting_point_atom 
#starting_point_residue
#starting_point_coordinates

probe_radius 0.9
shell_radius 3
shell_depth 4 


#*****************************
# TUNNEL CLUSTERING
#*****************************
clustering average_link
weighting_coefficient 1
clustering_threshold 3.5

exclude_start_zone 2
exclude_end_zone 0
min_middle_zone 5
save_zones yes


#*****************************
# GENERATION OF OUTPUTS
#*****************************
one_tunnel_in_snapshot cheapest
max_output_clusters 999
save_dynamics_visualization no

generate_summary yes
generate_tunnel_characteristics yes
generate_tunnel_profiles yes

generate_histograms no
bottleneck_histogram 0.0 2.0 20
throughput_histogram 0 1.0 10

generate_bottleneck_heat_map no
bottleneck_heat_map_range 1.0 2.0
bottleneck_heat_map_element_size 10 10

generate_profile_heat_map no
profile_heat_map_resolution 0.5
profile_heat_map_range 1.0 2.0
profile_heat_map_element_size 20 10

compute_tunnel_residues no
residue_contact_distance 3.0

compute_bottleneck_residues no
bottleneck_contact_distance 3.0


#*****************************
# ADVANCED SETTINGS
#*****************************

#-----------------------------
# Starting point optimization
#-----------------------------
max_distance 3
desired_radius 5

#-----------------------------
# Advanced tunnel calculation 
#-----------------------------
number_of_approximating_balls 12
add_central_sphere yes

max_number_of_tunnels 10000
max_limiting_radius 100

cost_function_exponent 2

automatic_shell_radius no
automatic_shell_radius_bottleneck_multiplier 2
starting_point_protection_radius 4

#-----------------------------
# Redundant tunnels removal
#-----------------------------
frame_clustering yes
frame_weighting_coefficient 1
frame_clustering_threshold 1

frame_exclude_start_zone 0
frame_exclude_end_zone 0
frame_min_middle_zone 5

#-----------------------------
# Averaging of tunnel ends 
#-----------------------------
average_surface_frame yes
average_surface_global yes

average_surface_smoothness_angle 10
average_surface_point_min_angle 5
average_surface_tunnel_sampling_step 0.5

#-----------------------------
# Approximate clustering
#-----------------------------
do_approximate_clustering no
cluster_by_hierarchical_clustering 20000
max_training_clusters 15
generate_unclassified_cluster no

#-----------------------------
# Outputs
#-----------------------------
profile_tunnel_sampling_step 0.5
visualization_tunnel_sampling_step 1

visualize_tunnels_per_cluster 5000
visualization_subsampling random

compute_errors no
save_error_profiles no

path_to_vmd "C:/Program Files/University of Illinois/VMD/vmd.exe" 
generate_trajectory no

#-----------------------------
# Others
#-----------------------------
swap yes
seed 1    #no deafult, if missing, the seed is random
"""

def caver_input_complete(caver_folder : str) -> bool:
    # check if the caver folder exists
    if not os.path.exists(caver_folder):
        print(f"Error: The specified path does not exist: {args.caver}")
        return False
    # create the path to the caver.jar file
    caver_jar = os.path.join(caver_folder, "caver.jar")
    # check if the caver.jar file exists
    if not os.path.exists(caver_jar):
        print(f"Error: The caver.jar file does not exist in the specified path: {args.caver}")
        return False
    # create the path to the lib-directory
    lib_path = os.path.join(caver_folder, "lib")
    # check if the lib-directory exists
    if not os.path.exists(lib_path):
        print(f"Error: The lib-directory does not exist in the specified path: {args.caver}")
        return False
    return True

def create_configuration() -> str:
    """
    Create a configuration file for CAVER
    """
    res = CONFIG_SAMPLE + "\n"
    res += "starting_point_coordinates 0 0 0\n"
    return res

def execute_caver(heapSize : int, caver_lib : str, caver_jar : str, caver_folder : str, pdb_folder : str, config : str, output_folder : str):
    """
    use subprocess to 
    java -Xmx4000m -cp $lib_path -jar $caver_jar -home $caver_folder -pdb $pdb_folder -conf "$output_folder/config.txt" -out $output_folder
    """
    #subprocess.run(["ls", "-l"], shell=True)
    cmd = ["java", f"-Xmx{heapSize}m", "-cp", caver_lib, "-jar", caver_jar, "-home", caver_folder, "-pdb", pdb_folder, "-conf", config, "-out", output_folder]
    #cmd = shlex.join(cmd)
    print(cmd)
    
    

    result = subprocess.run(cmd, capture_output=True, text=True)

    print("Output:", result.stdout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyCaver: A Python-wrapper for CAVER, a software tool for the analysis and visualization of tunnels and channels in protein structures.')
    parser.add_argument('-i', '--input', help='Input file', required=True)
    parser.add_argument('-o', '--output', help='Output file', required=True)
    parser.add_argument('-c', '--caver', help='Path to the CAVER folder containing the caver.jar file and the lib-directory', default="caver_3.0/caver")

    parser.add_argument('-t', '--tmp', help='Temporary folder for storing temporary files"', default="tmp")
    parser.add_argument('-hs', '--heapSize', help='Heap size for Java', default=4000)
    parser.add_argument('-n', '--name', help='Name of the output file', default=None)

    parser.add_argument('--pdb_wise', help='PDB-wise mode', action='store_true')

    #################################### caver options ####################################

    #################################### caver options ####################################

    args = parser.parse_args()
    print(args)

    # perform caver input checks
    if not caver_input_complete(args.caver):
        exit()
    else:
        caver_jar = os.path.join(args.caver, "caver.jar")
        caver_lib = os.path.join(args.caver, "lib")

    # check if tmp folder exists
    if not os.path.exists(args.tmp):
        os.makedirs(args.tmp)
        print(f"Created temporary folder: {args.tmp}")

    # check if output folder exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)
        print(f"Created output folder: {args.output}")

    # check if name is defined if not create custom id
    if args.name is None:
        name = str(uuid.uuid4())
    else:
        name = args.name

    # check if input is file or directory
    if os.path.isdir(args.input):       # Input is directory
        if args.pdb_wise:            # PDB-wise mode is enabled
            """
            Running caver in PDB-wise mode meaning caver will be run for each PDB file in the input directory
            - therefore separat folders have to be created in the tmp folder for each PDB file
            - the pdb files will get copied there
            - caver is run on each folder and the results are stored in the output folder in one subfolder for each pdb file
            """
            pass
            

        else:
            """
            Running caver in normal mode meaning caver will be run on the input directory
            - therefore no folder has to be created in the tmp folder OR save the config file in the tmp folder??
            - output is stored in the output folder
            """
            pass


    elif os.path.isfile(args.input):    # Input is single file
        """
        Running caver in single file mode meaning caver will be run on the input file
        - therefore a folder has to be created in the tmp folder
        - the pdb file will get copied there
        - caver is run on the folder and the results are stored in the output folder
        """
        # prepare folder
        name_folder = os.path.join(args.tmp, name)
        if not os.path.exists(name_folder):
            os.makedirs(name_folder)

        in_folder = os.path.join(name_folder, "input")
        os.makedirs(in_folder)

        # copy pdb file to folder
        pdb_file_source = os.path.join(args.input)
        pdb_file_name = os.path.basename(pdb_file_source)
        pdb_file_destination = os.path.join(in_folder, pdb_file_name)

        try:
            shutil.copy(pdb_file_source, pdb_file_destination)
            #verbose print("File copied successfully.")
        except shutil.SameFileError:
            print("Error: Source and destination represents the same file.")
            exit()
        except PermissionError:
            print("Error: Permission denied.")
            exit()
        except:
            print("Error occurred while copying file.")
            exit()

        # create config file
        config_file = os.path.join(name_folder, "config.txt")
        with open(config_file, "w") as file:
            config = create_configuration()
            file.write(config)

        # run caver
        print(f"Running CAVER on {pdb_file_name}")
        execute_caver(heapSize=args.heapSize, caver_lib=caver_lib, caver_jar=caver_jar, caver_folder=args.caver, pdb_folder=in_folder, config=config_file, output_folder=args.output)
        pass



    else:
        print("Error: The specified input is neither a file nor a directory")
        exit()
    

    #execute_caver(heapSize=args.heapSize, caver_jar="args.caver", caver_folder="args.caver", pdb_folder="args.input", output_folder="args.output")