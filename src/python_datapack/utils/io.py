
from .print import *
import shutil
import json
import os
import io

# For easy file management
def super_open(file_path: str, mode: str, encoding = "utf-8") -> io.TextIOWrapper:
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
def super_copy(src: str, dst: str) -> shutil.copy:
	""" Copy a file (or a folder) from the source to the destination
	Args:
		src	(str): The source path
		dst	(str): The destination path
	"""
	# Make directory
	os.makedirs(os.path.dirname(dst), exist_ok=True)

	# If source is a folder, copy it recursively
	if os.path.isdir(src):
		return shutil.copytree(src, dst, dirs_exist_ok = True)
	else:
		# Remove destination path from old files
		cleaned_dst = clean_path(dst)
		if cleaned_dst in INITIAL_FILES:
			del INITIAL_FILES[cleaned_dst]

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
def super_json_dump(data: dict|list, file: io.TextIOWrapper = None, max_level: int = 2) -> str:
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
				new_dict[key] = list(set(new_dict[key]))
		
		# Else, just overwrite or add value
		else:
			new_dict[key] = value
	
	# Return the new dict
	return new_dict

# Utility function to clean the path
def clean_path(file_path: str) -> str:
	""" Clean the path by replacing backslashes with forward slashes and simplifying the path\n
	Args:
		file_path (str): The path to clean
	Returns:
		str: The cleaned path
	"""
	# Replace backslashes with forward slashes
	file_path = file_path.replace("\\", "/")

	# If the path contains "../", simplify it
	if "../" in file_path:
		file_path = file_path.split("/")
		for i in range(len(file_path)):
			if file_path[i] == ".." and i > 0:
				file_path[i] = ""
				file_path[i-1] = ""
		file_path = "/".join(file_path)

	# Replace "./" with nothing since it's useless
	file_path = file_path.replace("./", "")

	# Return the cleaned path
	return file_path

# Keeping track of the files that have been present before running the program
INITIAL_FILES: dict[str, str] = {}
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
				except:
					pass


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
	contains = contains.replace("\\", "/")
	for file_path, content in FILES_TO_WRITE.items():
		if contains not in file_path:
			continue

		# Make sure the content ends with two break lines
		if not content.endswith("\n\n"):
			if content.endswith("\n"):
				content += "\n"
			else:
				content += "\n\n"

		# If the file already exists and the content didn't change, skip it
		if file_path in INITIAL_FILES and content == INITIAL_FILES[file_path]:
			continue

		# Write the content to the file
		with super_open(file_path, "w") as f:
			f.write(content)

def delete_old_files(contains: str = ""):
	""" Delete all the files that are not in the write queue and contains the given string\n
	Args:
		contains (str): If set, only delete the files that contains this string in their path
	"""
	contains = contains.replace("\\", "/")
	for file_path in INITIAL_FILES.keys():
		if contains not in file_path:
			continue

		# If the file is not in the write queue, delete it
		if file_path not in FILES_TO_WRITE:
			os.remove(file_path)

