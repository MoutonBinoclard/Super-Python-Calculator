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