
## Python script that modifies the pyproject.toml to go to the next version
# Imports
import os

# Constants
PYPROJECT_PATH = "pyproject.toml"
VERSION_KEY = "version = "

# Read the file
with open(PYPROJECT_PATH, "r", encoding="utf-8") as file:
	lines = file.readlines()

# Find the version line
version_line = None
for i, line in enumerate(lines):
	if line.startswith(VERSION_KEY):
		version_line = i
		break

if version_line:
	# Get the version
	version = lines[version_line].replace(VERSION_KEY, "").strip().replace('"', "")
	splitted_version = version.split(".")

	# Increment the last number
	splitted_version[-1] = str(int(splitted_version[-1]) + 1)

	# Join the version
	new_version = ".".join(splitted_version)

	# Replace the version
	lines[version_line] = f'{VERSION_KEY}"{new_version}"\n'

	# Write the file
	with open(PYPROJECT_PATH, "w", encoding="utf-8") as file:
		file.writelines(lines)

