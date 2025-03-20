
# Imports
import stouputils as stp
from .general import *

# Functions
def delete_file(file_path: str, clean_on_disk: bool = True) -> bool:
	""" Delete the file at the given path

	Args:
		file_path		(str):	The path to the file
		clean_on_disk	(bool):	If the file should be deleted on disk (default: True)
	Returns:
		bool: If the file was deleted
	"""
	# Clean path
	file_path = stp.clean_path(file_path)
	deleted: bool = False

	# If the file is in the write queue, delete it
	if file_path in FILES_TO_WRITE:
		del FILES_TO_WRITE[file_path]
		deleted = True
	if is_in_initial_files(file_path):
		remove_initial_file(file_path)

	# If the file exists, delete it
	if clean_on_disk and os.path.exists(file_path):
		os.remove(file_path)
		deleted = True
	
	# If the file wasn't deleted, print a warning
	if not deleted:
		stp.warning(f"Couldn't delete the file '{file_path}', it doesn't exists")
	return deleted

def delete_files(contains: str = "", clean_on_disk: bool = True) -> list[str]:
	""" Delete all the files that contains the given string

	Args:
		contains		(str):	The string that the path must contain
		clean_on_disk	(bool):	If the files should be deleted on disk (default: True)
	"""
	contains = stp.clean_path(contains)
	deleted_files: list[str] = []
	files_to_delete: list[str] = list(FILES_TO_WRITE.keys())

	# Delete all the files
	for file_path in [x for x in files_to_delete if contains in x]:
		if delete_file(file_path, clean_on_disk):
			deleted_files.append(file_path)

	# If clean_on_disk is true, add the files present on disk to the list
	if clean_on_disk:

		# Get the build folder by searching the data folder
		has_data: list[str] = [x for x in files_to_delete if "datapack/data/" in x]
		if len(has_data) != 0:
			build_folder: str = os.path.dirname(has_data[0].split("datapack/data/")[0])

			# Add all the files that contains the string to the list
			files: list[str] = [stp.clean_path(f"{root}/{path}") for root, _, files in os.walk(build_folder) for path in files]
			for file_path in files:
				if contains in file_path:
					if os.path.isfile(file_path) and delete_file(file_path, clean_on_disk):
						deleted_files.append(file_path)

	return deleted_files

def delete_old_files(contains: str = ""):
	""" Delete all the files that are not in the write queue and contains the given string

	Args:
		contains (str): If set, only delete the files that contains this string in their path
	"""
	contains = stp.clean_path(contains)
	for file_path in INITIAL_FILES_SET:
		if contains not in file_path:
			continue

		# If the file is not in the write queue, delete it
		if file_path not in FILES_TO_WRITE and os.path.exists(file_path):
			os.remove(file_path)

	# Delete empty folders
	for root, _, _ in os.walk(".", topdown=False):
		if not os.listdir(root):
			os.rmdir(root)

