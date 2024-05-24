
import os
commands = [
	"py 1_upgrades.py",
	"py 2_build.py",
	"py 3_upload.py",
]

for command in commands:
	if os.system(command) != 0:
		print(f"Error while executing '{command}'")
		exit(1)

