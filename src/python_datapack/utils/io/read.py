
# Imports
import os
import stouputils as stp
from .general import FILES_TO_WRITE, DATAPACK_RESOURCE_TYPES, path_to_file_path

# Functions
def read_file(file_path: str) -> str:
	""" Read the file at the given path

	Args:
		file_path (str): The path to the file
	Returns:
		str: The content of the file
	"""
	# Clean path
	file_path = stp.clean_path(file_path)

	# If the file is in the write queue, return it
	if file_path in FILES_TO_WRITE:
		return FILES_TO_WRITE[file_path]

	# If the file exists, read it
	if os.path.exists(file_path):
		with stp.super_open(file_path, "r") as f:
			return f.read()
	
	# Else, return an empty string
	return ""

