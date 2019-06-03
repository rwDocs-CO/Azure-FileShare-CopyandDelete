# Microsoft Azure: File Share copy and delete Python functions
Two python functions that can delete content from a file share and load local files and sub-directories to a Microsoft Azure File Share

We've recently begun automating our documentation publishing process and created these two Python functions to handle removing old content from and copying content to a Microsoft Azure File Share.  These functions, which are part of a larger Python script, are tied to Jenkins and allow our writers to remove and upload content to our Microsoft Azure File Share, which contains the content for our documentation website.

One function removes a file share (all files and sub-directories).  The other function copies all files and sub-directories from a directory on a local drive to the Azure File Share, replicating the directory structure.  I have included some optional elements that we needed in the functions, such as keeping a needed file in the base file share we are uploading to and making sure the delete function only deletes things if a specific directory is in the path.  Both of these can be taken out, though the delete function will happily delete everything, so use with caution.

The delete function does expect all of the files to be deletable, so if one of the files is set to read-only and you don't have permissions to delete it, the script will fail.  We did run into this issue (on a file that should not have been set to read-only) and had to put in a request to delete the file manually.

## Licensing
These functions are licensed under the MIT License.