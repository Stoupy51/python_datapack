
import shutil
import os

source = os.path.dirname(os.path.realpath(__file__)).replace("\\","/") + "/src/python_datapack"
destination = "C:/Users/Alexandre-PC/AppData/Local/Programs/Python/Python310/Lib/site-packages/python_datapack"

shutil.rmtree(destination, ignore_errors=True)
shutil.copytree(source, destination)
os.system("clear")
print("\nCopied python_datapack to local Python's site-packages\n")

