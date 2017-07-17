import os
from . import zipfile
import tempfile
import shutil
from django.core.files.base import ContentFile
from django.core.files import File
from django.http import HttpRequest
from chatbot.models import aiml_file
####################################################################
## Process Archive File - Used in admin.py 
## For uploading setup configurations
## Takes a list of files and returns a list of only chatbot files

DJANGO_LOGGING = True # I'm only implementing this lazily here, but we'd stick this constant in the settings.py of the parent app and all it into necessary pages.

def PrintException():
    import linecache
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)



def g_log_exception(err, filename="general_log.txt", exception=False):
    if DJANGO_LOGGING:
        import time
        import datetime
        errorFile = open(os.path.join(os.path.dirname(__file__), 'errors', filename), "a")
        startTime = time.time()
        startTime = datetime.datetime.fromtimestamp(startTime) # check 
        errorFile.write("Time: " + str(startTime) + "  ")
        errorFile.write(str(err))
        if exception:
            errorFile.write("\n" + PrintException())
        errorFile.write("\n")
        errorFile.close()

# Ensure all files extracted from zip file are of the appropriate chatbot type
def Validate(files):
    valid_files = []
    acceptable_filetypes = ('.aiml', '.set', '.map', '.substitution', '.pdefaults', '.properties')
    for file in files:
        filename, file_extension = os.path.splitext(file.name)
        if file_extension in acceptable_filetypes:
            valid_files.append(file)
    return valid_files


# Process any zip files and return a list of all processed files
def Process_Files(files, temp_directory):
    file_list = []
    for file in files:
        filename, file_extension = os.path.splitext(str(file))
        if(file_extension == '.zip'):
            Extract_Zip(file, temp_directory)
            folder_name = os.listdir(temp_directory)[0]
            full_path = os.path.join(temp_directory, folder_name)
            if (os.path.isdir(full_path)):
                for filename in os.listdir(full_path):
                    file_list.append(File(open(os.path.join(full_path, filename))))
                    #logging throws error here i.e. not a directory
            else: #if file and not directory, scan through files
                for filename in os.listdir(temp_directory):
                    file_list.append(File(open(os.path.join(temp_directory, filename))))
                    
            file_list = Validate(file_list)
        else:
            file_list.append(file)
    return file_list

# Extract zipfiles into temporary directory
def Extract_Zip(file, temp_directory):
    archive = zipfile.ZipFile(file, 'r')
    archive.extractall(temp_directory)
        
# Save files as aiml files, takes setup parameter to save files to and request to specify user
def Save_Aiml(files, setup, request):
    for file in files:
        afile = aiml_file.file_manager.create(docfile=file, text_file=file.read(), author=request.user)	
        afile.save()
        setup.aiml_files.add(afile)
    setup.save()
        



    
        


            
        
    
    
    
            

    