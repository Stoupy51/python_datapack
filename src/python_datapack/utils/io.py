
from .print import *
import shutil
import json
import os
import io
from typing import IO


# Utility function to clean the path
def clean_path(file_path: str) -> str:
	""" Clean the path by replacing backslashes with forward slashes and simplifying the path\n
	Args:
		file_path (str): The path to clean
	Returns:
		str: The cleaned path
	"""
	# Replace backslashes with forward slashes and double slashes
	file_path = file_path.replace("\\", "/").replace("//", "/")

	# If the path contains "../", simplify it
	if "../" in file_path:
		splitted = file_path.split("/")
		for i in range(len(splitted)):
			if splitted[i] == ".." and i > 0:
				splitted[i] = ""
				splitted[i-1] = ""
		file_path = "/".join(splitted)

	# Replace "./" with nothing since it's useless
	file_path = file_path.replace("./", "")

	# Return the cleaned path
	return file_path

# Keeping track of the files that have been present before running the program
INITIAL_FILES: dict[str, str] = {}
INITIAL_FILES_SET: set[str] = set()
def read_initial_files(folders: list[str]) -> None:
	""" Read all the files in the given folders and store them in INITIAL_FILES\n
	Args:
		folders (list[str]): The list of folders to read the files from
	"""
	for folder in folders:
		for root, _, files in os.walk(folder):
			for file in files:
				path: str = clean_path(os.path.join(root, file))
				try:
					with super_open(path, "r") as f:
						INITIAL_FILES[path] = f.read()
						INITIAL_FILES_SET.add(path)
				except:
					pass

@handle_error(exceptions=(KeyError,))
def remove_initial_file(file_path: str) -> None:
	""" Remove the file from the initial files\n
	Args:
		file_path (str): The path to the file
	"""
	del INITIAL_FILES[file_path]
	INITIAL_FILES_SET.remove(file_path)

def is_in_initial_files(file_paths: list[str]|str) -> bool:
	""" Check if all the given file paths are in the initial files\n
	Args:
		file_paths (list[str]|str): The list of file paths to check or a single file path
	Returns:
		bool: If all the file paths are in the initial files
	"""
	if isinstance(file_paths, str):
		return file_paths in INITIAL_FILES_SET
	return all(file_path in INITIAL_FILES_SET for file_path in file_paths)


# For easy file management
def super_open(file_path: str, mode: str, encoding = "utf-8") -> IO:
	""" Open a file with the given mode, creating the directory if it doesn't exist
	Args:
		file_path	(str): The path to the file
		mode		(str): The mode to open the file with, ex: "w", "r", "a", "wb", "rb", "ab"
		enconding	(str): The encoding to use when opening the file (default: "utf-8")
	Returns:
		open: The file object, ready to be used
	"""
	# Make directory
	if "/" in file_path or "\\" in file_path:
		os.makedirs(os.path.dirname(file_path), exist_ok=True)

	# Open file and return
	if "b" in mode:
		return open(file_path, mode)
	else:
		return open(file_path, mode, encoding = encoding) # Always use utf-8 encoding to avoid issues


# For easy file copy
def super_copy(src: str, dst: str) -> str:
	""" Copy a file (or a folder) from the source to the destination
	Args:
		src	(str): The source path
		dst	(str): The destination path
	Returns:
		str: The destination path
	"""
	# Make directory
	os.makedirs(os.path.dirname(dst), exist_ok=True)

	# If source is a folder, copy it recursively
	if os.path.isdir(src):
		return shutil.copytree(src, dst, dirs_exist_ok = True)
	else:
		# Remove destination path from old files
		cleaned_dst = clean_path(dst)
		if is_in_initial_files(cleaned_dst):
			remove_initial_file(cleaned_dst)

		# Copy file
		return shutil.copy(src, dst)

# JSON load from file path
def super_json_load(file_path: str) -> dict:
	""" Load a JSON file from the given path
	Args:
		file_path (str): The path to the JSON file
	Returns:
		dict: The content of the JSON file
	"""
	with super_open(file_path, "r") as f:
		return json.load(f)

# JSON dump with indentation for levels
def super_json_dump(data: dict|list, file: io.TextIOWrapper|None = None, max_level: int = 2) -> str:
	""" Dump the given data to a JSON file with indentation for only 2 levels by default
	Args:
		data (dict|list): 			The data to dump
		file (io.TextIOWrapper): 	The file to dump the data to, if None, the data is returned as a string
		max_level (int):			The level of where indentation should stop (-1 for infinite)
	Returns:
		str: The content of the file in every case
	"""
	content = json.dumps(data, indent = '\t', ensure_ascii = False)
	if max_level > -1:

		# Seek in content to remove to high indentations
		longest_indentation = 0
		for line in content.split("\n"):
			indentation = 0
			for char in line:
				if char == "\t":
					indentation += 1
				else:
					break
			longest_indentation = max(longest_indentation, indentation)
		for i in range(longest_indentation, max_level, -1):
			content = content.replace("\n" + "\t" * i, "")
			pass

		# To finalyze, fix the last indentations
		finishes = ('}', ']')
		for char in finishes:
			to_replace = "\n" + "\t" * max_level + char
			content = content.replace(to_replace, char)
	
	# Write file content and return it
	content += "\n"
	if file:
		file.write(content)
	return content

def unique_list(list_to_clean: list) -> list:
	""" Remove duplicates from the list while keeping the order
	Args:
		list_to_clean (list): The list to clean
	Returns:
		list: The cleaned list
	"""
	seen: set = set()
	result: list = []
	for item in list_to_clean:
		item_key = tuple(item) if isinstance(item, list) else item	# Convert item to tuple if it's a list to make it hashable
		if item_key not in seen:
			seen.add(item_key)
			result.append(item)
	return result

# Merge two dict recuirsively
def super_merge_dict(dict1: dict, dict2: dict) -> dict:
	""" Merge the two dictionnaries recursively without modifying originals
	Args:
		dict1 (dict): The first dictionnary
		dict2 (dict): The second dictionnary
	Returns:
		dict: The merged dictionnary
	"""
	# Copy first dictionnary
	new_dict = {}
	for key, value in dict1.items():
		new_dict[key] = value
	
	# For each key of the second dictionnary,
	for key, value in dict2.items():

		# If key exists in dict1, and both values are also dict, merge recursively
		if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
			new_dict[key] = super_merge_dict(dict1[key], value)
		
		# Else if it's a list, merge it
		elif key in dict1 and isinstance(dict1[key], list) and isinstance(value, list):
			new_dict[key] = dict1[key] + value
			if not any(isinstance(x, dict) for x in new_dict[key]):
				new_dict[key] = unique_list(new_dict[key])
		
		# Else, just overwrite or add value
		else:
			new_dict[key] = value
	
	# Return the new dict
	return new_dict

# The majority of files will be written at the end of the program to prevent excessive disk access (reading + appending + writing)
FILES_TO_WRITE: dict[str, str] = {}
def is_in_write_queue(file_path: str) -> bool:
	return clean_path(file_path) in FILES_TO_WRITE

def sort_override_model(json_content: dict) -> None:
	for key, value in json_content.items():
		if key == "overrides" \
			and isinstance(value, list) and len(value) > 1 \
			and all(isinstance(x, dict) \
				and x.get("predicate") \
				and isinstance(x["predicate"], dict) \
				and x["predicate"].get("custom_model_data") is not None \
				and isinstance(x["predicate"]["custom_model_data"], int) \
				for x in value
			):
				json_content["overrides"] = sorted(value, key=lambda x: x["predicate"]["custom_model_data"])

def read_file(file_path: str) -> str:
	""" Read the file at the given path\n
	Args:
		file_path (str): The path to the file
	Returns:
		str: The content of the file
	"""
	# Clean path
	file_path = clean_path(file_path)

	# If the file is in the write queue, return it
	if file_path in FILES_TO_WRITE:
		return FILES_TO_WRITE[file_path]

	# If the file exists, read it
	if os.path.exists(file_path):
		with super_open(file_path, "r") as f:
			return f.read()
	
	# Else, return an empty string
	return ""

def function_path_to_file_path(config: dict, function_path: str) -> str:
	""" Convert a function path to a file path\n
	Args:
		config (dict): The main configuration
		function_path (str): The path to the function (ex: "namespace:folder/function_name")
	Returns:
		str: The file path
	"""
	if isinstance(config, str):
		error(f"The first argument should be the configuration dict, not a string. You probably swapped the arguments.")

	# Get the namespace (if any)
	namespace: str = function_path.split(":")[0] if ":" in function_path else "minecraft"
	function_path = function_path.split(":")[-1] if ":" in function_path else function_path

	# Return the file path
	return f"{config['build_datapack']}/data/{namespace}/function/{function_path}.mcfunction"

def read_function(config: dict, function_path: str) -> str:
	""" Read the function at the given path\n
	Args:
		config (dict): The main configuration
		function_path (str): The path to the function (ex: "namespace:folder/function_name")
	Returns:
		str: The content of the function
	"""
	return read_file(function_path_to_file_path(config, function_path))

def write_to_file(file_path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the file at the given path\n
	If you wish to write to the load/tick files or other versioned files, use the dedicated function instead (write_to_versioned_file)\n
	Args:
		file_path	(str):	The path to the file
		content		(str):	The content to write
		overwrite	(bool):	If the file should be overwritten (default: Append the content)
		prepend		(bool):	If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	# Clean path
	file_path = clean_path(file_path)

	# If content is a dictionnary, dump it
	if isinstance(content, dict):
		content = super_json_dump(content)

	# If file doesn't exists or overwrite is true, made it empty
	if file_path not in FILES_TO_WRITE or overwrite:
		if is_in_initial_files(file_path):
			remove_initial_file(file_path)
		FILES_TO_WRITE[file_path] = ""
	
	# If the file already exists as JSON and the content is a dict, merge both dict
	if not overwrite and file_path in FILES_TO_WRITE and file_path.endswith((".json",".mcmeta")) and FILES_TO_WRITE[file_path] != "":
		dict_content = json.loads(content)
		old_content = json.loads(FILES_TO_WRITE[file_path])
		merged = super_merge_dict(old_content, dict_content)
		sort_override_model(merged)
		FILES_TO_WRITE[file_path] = super_json_dump(merged)
		return
	
	# Add the content to the file
	if prepend:
		FILES_TO_WRITE[file_path] = str(content) + FILES_TO_WRITE[file_path]
	else:
		FILES_TO_WRITE[file_path] += str(content)

def write_to_function(config: dict, function_path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the function where the path is like when calling a function\n
	If no namespace is given, it will default to "minecraft"\n
	Args:
		config			(dict):	The main configuration
		function_path	(str):	The path to the function (ex: "namespace:folder/function_name")
		content			(str):	The content to write
		overwrite		(bool):	If the file should be overwritten (default: Append the content)
		prepend			(bool):	If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_to_file(function_path_to_file_path(config, function_path), content, overwrite, prepend)


def delete_file(file_path: str, clean_on_disk: bool = True) -> bool:
	""" Delete the file at the given path\n
	Args:
		file_path		(str):	The path to the file
		clean_on_disk	(bool):	If the file should be deleted on disk (default: True)
	Returns:
		bool: If the file was deleted
	"""
	# Clean path
	file_path = clean_path(file_path)
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
		warning(f"Couldn't delete the file '{file_path}', it doesn't exists")
	return deleted

def delete_files(contains: str = "", clean_on_disk: bool = True) -> list[str]:
	""" Delete all the files that contains the given string\n
	Args:
		contains		(str):	The string that the path must contain
		clean_on_disk	(bool):	If the files should be deleted on disk (default: True)
	"""
	contains = clean_path(contains)
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
			files: list[str] = [clean_path(f"{root}/{path}") for root, _, files in os.walk(build_folder) for path in files]
			for file_path in files:
				if contains in file_path:
					if os.path.isfile(file_path) and delete_file(file_path, clean_on_disk):
						deleted_files.append(file_path)

	return deleted_files



def write_to_versioned_file(config: dict, relative_path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the versioned file at the given path\n
	This function should be used to write to the confirm_load/tick mcfunction files or other versioned files such as tick_2, second, ...\n
	Args:
		config			(dict):	The main configuration
		relative_path	(str):	The path to the file relative to the versioned folder (ex: "load" refers to "data/namespace/function/vX/load.mcfunction")
		content			(str):	The content to write
		overwrite		(bool):	If the file should be overwritten (default: Append the content)
		prepend			(bool):	If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	# Force the path to be .mcfunction
	if relative_path.endswith((".json",".mcmeta")):
		error(f"Writing to a {relative_path.split('.')[-1]} file is not allowed using write_to_versioned_file(), use write_to_file() instead.")
	
	# Make sure the path is correct for load/confirm_load
	if relative_path in ["load","confirm_load"]:
		warning(f"You tried to write to the '{relative_path}' file, did you mean to write to the 'load/confirm_load' file instead?")

	# Add .mcfunction to the path
	if relative_path.endswith(".mcfunction"):
		warning(f"The method write_to_versioned_file() already adds the '.mcfunction' extension to the path, you don't need to add it yourself.")
	else:
		relative_path += ".mcfunction"
	
	# Write to the file
	functions_path: str = f"{config['build_datapack']}/data/{config['namespace']}/function/v{config['version']}"
	write_to_file(f"{functions_path}/{relative_path}", content, overwrite, prepend)


def write_to_load_file(config: dict, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the load file\n
	Args:
		config		(dict):	The main configuration
		content		(str):	The content to write
		overwrite	(bool):	If the file should be overwritten (default: Append the content)
		prepend		(bool):	If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_to_versioned_file(config, "load/confirm_load", content, overwrite, prepend)


def write_to_tick_file(config: dict, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the tick file\n
	Args:
		config		(dict):	The main configuration
		content		(str):	The content to write
		overwrite	(bool):	If the file should be overwritten (default: Append the content)
		prepend		(bool):	If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_to_versioned_file(config, "tick", content, overwrite, prepend)


def write_all_files(contains: str = ""):
	""" Write all the files in the write queue to their respective files\n
	If a file content didn't change, it won't be written\n
	Args:
		contains (str): If set, only write the files that contains this string in their path
	"""
	contains = clean_path(contains)
	
	# Pre-process all contents to have two newlines at the end
	processed_contents: dict[str, str] = {}
	for path, content in FILES_TO_WRITE.items():
		if contains not in path:
			continue
			
		if not content.endswith("\n\n"):
			content = content.rstrip("\n") + "\n\n"
		processed_contents[path] = content

	# Filter out unchanged files
	files_to_write: dict[str, str] = {
		path: content for path, content in processed_contents.items()
		if path not in INITIAL_FILES_SET or content != INITIAL_FILES[path]
	}

	# Batch write all files
	for file_path, content in files_to_write.items():
		with super_open(file_path, "w") as f:
			f.write(content)

def delete_old_files(contains: str = ""):
	""" Delete all the files that are not in the write queue and contains the given string\n
	Args:
		contains (str): If set, only delete the files that contains this string in their path
	"""
	contains = clean_path(contains)
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

