
import shutil
import os

source = os.path.dirname(os.path.realpath(__file__)).replace("\\","/") + "/src/python_datapack"
destinations: list[str] = [
	"C:/Users/Alexandre-PC/AppData/Local/Programs/Python/Python312/Lib/site-packages/python_datapack",
	"C:/Users/1053914/AppData/Local/Programs/Python/Python312/Lib/site-packages/python_datapack"
]


for dest in destinations:
	try:
		shutil.rmtree(dest, ignore_errors=True)
		shutil.copytree(source, dest)
	except Exception as e:
		pass

os.system("clear")
print("\nCopied python_datapack to local Python's site-packages\n")

