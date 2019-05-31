######################################
# RECURSIVE FUNCTION TO COPY FILES TO AZURE
# recursive_file_copy.py
#
# Function to copy files and sub-directories to Azure File Share.
# This function is acts like a recursive function when it 
# finds a sub-directory when it is trying to upload files
# from a local directory to the Azure File Share. Each time it 
# encounters a sub-directory in the local directory it creates 
# a directory on Azure with that name, and calls itself with 
# the new sub-directories parameters.  It enters the new sub-directory
# and starts uploading files from the local location to the new
# location in Azure.
#
# Tested with Python 3.6.5
# April, 4 2019
#
######################################

######################################
# MIT License
#
# Copyright(c) Rogue Wave Software, Inc. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# ----------------------------------------------------------------------------------
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
######################################


######################################
# IMPORT AND SETUP SECTION
######################################
import os, sys
from azure.storage.file import FileService

######################################
# FUNCTION SECTION
######################################

def upload_directory(az_root_dir, az_dir_to_copy_to, local_dir, file_service):
    # Create the current location in Azure from the root directory and the directory
    # are currently in.
    current_file_share_location = az_root_dir + '/' + az_dir_to_copy_to

    for item in os.listdir(local_dir):
        local_path_and_item = local_dir + "\\" + item

        if os.path.isdir(local_path_and_item):  
            print("\nFound a directory. Recursive power engaged.")
            # Create a directory in Azure.
            file_service.create_directory(current_file_share_location, item)
            upload_directory(current_file_share_location, item, local_path_and_item, file_service)
            continue  
        elif os.path.isfile(local_path_and_item):  
            print("\nCopying a file to Azure.")
            try:
                file_service.create_file_from_path(
                az_root_dir, 
                az_dir_to_copy_to,
                item, 
                local_path_and_item, 
                content_settings=None, 
                metadata=None, 
                validate_content=False, 
                progress_callback=None, 
                max_connections=2, 
                timeout=None
                )
            except Exception as e:
                print("Error during blob uploading. Details: {0}".format(e))  
        else:  
            print("Found an unexpected file." )


######################################
# EXAMPLE USE SECTION
######################################

# Create parameters.  Our main script has these as inputs to the script.
file_share = 'dir1/dir2/dir3'
az_dir_name = 'dir_to_put_files_into'  # this puts the files in dir1/dir2/dir3/dir_to_put_files_into
local_path = r"C:\test_files\test"

# Create the FileService that is used to access the file share
file_service = FileService(account_name='name_of_account', account_key='account_key')

# Call the function with the initial parameters:
upload_directory(file_share, az_dir_name, local_path, file_service)