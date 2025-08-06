import os

def list_files(extension, prefix):
    """
    Lists all files in the current directory that have a specific extension
    and do not start with a specific prefix.
    """
    
    # Get the current directory
    current_directory = os.getcwd()
    
    # List all files in the current directory
    files = os.listdir(current_directory)
    
    # Filter files to exclude those that start with the prefix
    filtered_files = [
        file for file in files
        if file.endswith(extension) and not file.startswith(prefix)
    ]
    
    return filtered_files

def show_entries_from_base_dict(dict_base):
    """
    Print the dictionary but good
    """
    for keys in dict_base :
        print(keys)
        print(dict_base[keys]['name'])
        for round in dict_base[keys]['rounds']:
            print(round)
        # print stats
        print('Number of rounds:', dict_base[keys]['nb_rounds'])
        print('Total kills:', dict_base[keys]['total_kills'])
        print('Total wins:', dict_base[keys]['total_wins'])
        print('Kill average:', dict_base[keys]['kill_avg'])
        print('Placement average:', dict_base[keys]['plac_avg'])
        print('Max kills:', dict_base[keys]['max_kill'])
        print("\n")

def show_entries_from_fusion_dict(dict_fusion):
    """
    Print the fusion dictionary but good
    """
    for keys in dict_fusion:
        print(keys)
        print(dict_fusion[keys]['names'])
        print('Score:', dict_fusion[keys]['score'])
        for round in dict_fusion[keys]['rounds']:
            print(round)
        # print stats
        print("\n")
