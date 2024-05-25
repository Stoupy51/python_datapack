
import shutil
import os

source = os.path.dirname(os.path.realpath(__file__)).replace("\\","/") + "/src/python_datapack"
destination = "C:/Users/Alexandre-PC/AppData/Local/Programs/Python/Python310/Lib/site-packages/python_datapack"

shutil.rmtree(destination, ignore_errors=True)
shutil.copytree(source, destination)
print("Copied python_datapack to local Python's site-packages")

