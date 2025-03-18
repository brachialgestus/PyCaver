import argparse
import os
import subprocess


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


def execute_caver():
    """
    java -Xmx4000m -cp $lib_path -jar $caver_jar -home $caver_folder -pdb $pdb_folder -conf "$output_folder/config.txt" -out $output_folder
    """
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyCaver: A Python-wrapper for CAVER, a software tool for the analysis and visualization of tunnels and channels in protein structures.')
    parser.add_argument('-i', '--input', help='Input file', required=True)
    parser.add_argument('-o', '--output', help='Output file')#, required=True)
    parser.add_argument('-c', '--caver', help='Path to the CAVER folder containing the caver.jar file and the lib-directory', default="caver_3.0/caver")

    parser.add_argument('--pdb_wise', help='PDB-wise mode', action='store_true')

    args = parser.parse_args()
    print(args)

    # perform caver input checks
    if not caver_input_complete(args.caver):
        exit()

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
        pass



    else:
        print("Error: The specified input is neither a file nor a directory")
        exit()
    

    execute_caver()