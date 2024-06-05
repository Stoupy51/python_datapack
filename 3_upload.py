
import os
LAST_FILES = 2
for root, _, files in os.walk("dist"):
	lasts = files[-2*LAST_FILES:]	# x2 because we have the .tar.gz and the .whl
	for file in lasts:
		if file.endswith(".tar.gz"):
			os.system(f"py -m twine upload --verbose -r python_datapack dist/{file}")

