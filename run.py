import subprocess
import os

currdir = os.path.dirname(os.path.realpath(__file__)) 
print("Starting background task processing")
subprocess.Popen(r'python manage.py process_tasks &',cwd=currdir,shell=True)
print("Running the stores system")
subprocess.Popen(r'python manage.py runserver', cwd=currdir,shell=True)

