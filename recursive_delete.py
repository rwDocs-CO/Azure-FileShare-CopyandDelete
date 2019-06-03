######################################
# RECURSIVE FUNCTION TO DELETE FILES IN AZURE
# recursive_delete.py
#
# Tested with Python 3.6.5
# April, 4 2019
#
######################################

####################################################################################
# MIT License
#
# Copyright(c) Rogue Wave Software, Inc. 
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
####################################################################################

######################################
# IMPORT AND SETUP SECTION
######################################
import sys
from azure.storage.file import FileService, File, Directory

######################################
# FUNCTION SECTION
######################################

def delete_directory(file_share, file_service):

    # This is optional.  We are only using this function on a specific directory.
    # If this function is run on the entire file share, it will delete everything,
    # so this statement is to keep everything else safe.

    #if 'current' not in file_share:
    #    print("The delete function is ONLY intended to be used on the 'current' directory! Aborting so something important isn't accidently deleted.")
    #    sys.exit()

    # Create a list of all the files and directories in the file_share parameter.
    generator = file_service.list_directories_and_files(file_share)

    # Loop through each item in the file_share and test to see if it is a directory
    # or file.  If it is a directory, create a new file_share variable and pass that
    # to a new instance of this function. If it is a file and it doesn't match the 
    # file you want to keep, delete it.  If it does match the file you want to keep
    # skip it. We needed to keep a specific file in the original directory, but this
    # part is entirely optional.  
    for share in generator:
        if isinstance(share, Directory):
            print("\nFound a directory. Recursive power engaged.")
            # Update file share variable and pass it to new instance of this function.
            new_file_share_location = file_share + '/' + share.name
            delete_directory(new_file_share_location, file_service)
            file_service.delete_directory(file_share, share.name, fail_not_exist=False, timeout=None)
            print("\t Deleting directory: " + share.name)   
            continue         
        elif isinstance(share, File):
            if 'index.php' in share.name:
                continue
            else:
                print("\t Deleting file: " + share.name)
                file_service.delete_file(file_share, None, share.name)


######################################
# EXAMPLE USE SECTION
######################################

# Create example parameter.  Our main script has this as an input to the script.
file_share = 'dir1/dir2/dir3/dir4/current'

# Create the FileService that is used to access the file share
file_service = FileService(account_name='name_of_account', account_key='account_key')

# Call the function with the initial parameters:
delete_directory(file_share, file_service)