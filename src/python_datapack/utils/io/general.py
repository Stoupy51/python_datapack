
import os
import json
import shutil
import stouputils as stp
from typing import Literal

# Variable constants
INITIAL_FILES: dict[str, str] = {}
""" The files that have been present before running the program (dict[path, content]) """
INITIAL_FILES_SET: set[str] = set()
""" The files that have been present before running the program (set[path]) """
FILES_TO_WRITE: dict[str, str] = {}
""" The files that have been written to (dict[path, content]) """
DATAPACK_RESOURCE_TYPES: list[str] = [
	"function",
	"advancement", 
	"predicate",
	"tags",
	"item_modifier",
	"recipe",
	"loot_table",

	"structure",
	"damage_type",
	"chat_type", 
	"banner_pattern",
	"wolf_variant",
	"enchantment",
	"enchantment_provider",
	"jukebox_song",
	"painting_variant",
	"instrument",
	"trial_spawner",
	"trim_pattern",
	"trim_material"
]
""" The different resource types for datapack, used to generate write_* and read_from_* functions """


# Keeping track of the files that have been present before running the program
def read_initial_files(folders: list[str]) -> None:
	""" Read all the files in the given folders and store them in INITIAL_FILES

	Args:
		folders (list[str]): The list of folders to read the files from
	"""
	for folder in folders:
		for root, _, files in os.walk(folder):
			for file in files:
				path: str = stp.clean_path(os.path.join(root, file))
				try:
					with stp.super_open(path, "r") as f:
						INITIAL_FILES[path] = f.read()
						INITIAL_FILES_SET.add(path)
				except:
					pass

@stp.handle_error(exceptions=KeyError)
def remove_initial_file(file_path: str) -> None:
	""" Remove the file from the initial files

	Args:
		file_path (str): The path to the file
	"""
	del INITIAL_FILES[file_path]
	INITIAL_FILES_SET.remove(file_path)

def is_in_initial_files(file_paths: list[str]|str) -> bool:
	""" Check if all the given file paths are in the initial files

	Args:
		file_paths (list[str]|str): The list of file paths to check or a single file path
	Returns:
		bool: If all the file paths are in the initial files
	"""
	if isinstance(file_paths, str):
		return file_paths in INITIAL_FILES_SET
	return all(file_path in INITIAL_FILES_SET for file_path in file_paths)

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
		cleaned_dst = stp.clean_path(dst)
		if is_in_initial_files(cleaned_dst):
			remove_initial_file(cleaned_dst)

		# Copy file
		return shutil.copy(src, dst)

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
				new_dict[key] = stp.unique_list(new_dict[key])
		
		# Else, just overwrite or add value
		else:
			new_dict[key] = value
	
	# Return the new dict
	return new_dict

# The majority of files will be written at the end of the program to prevent excessive disk access (reading + appending + writing)
def is_in_write_queue(file_path: str) -> bool:
	return stp.clean_path(file_path) in FILES_TO_WRITE

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

def path_to_file_path(config: dict, path: str, folder: Literal["function", "advancement", "..."] | str) -> str:
	""" Convert a relative path to a file path

	Args:
		config		(dict): The main configuration
		path		(str): The path (ex: "namespace:folder/name")
		folder		(Literal["function", "advancement", ...]): The folder to put the file in
	Returns:
		str: The file path
	"""
	if isinstance(config, str):
		stp.error(f"The first argument should be the configuration dict, not a string. You probably swapped the arguments.")

	# Get the namespace (if any)
	namespace: str = path.split(":")[0] if ":" in path else "minecraft"
	path = path.split(":")[-1] if ":" in path else path

	# Return the file path based on folder
	extension: str = ""
	if folder == "function":
		extension = ".mcfunction"
	else:
		extension = ".json"
	return f"{config['build_datapack']}/data/{namespace}/{folder}/{path}{extension}"


