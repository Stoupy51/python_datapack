
# Imports
import json

import stouputils as stp

from .general import (
	FILES_TO_WRITE,
	INITIAL_FILES,
	INITIAL_FILES_SET,
	is_in_initial_files,
	remove_initial_file,
	sort_override_model,
	super_merge_dict,
)


# Functions
def write_all_files(contains: str = "", verbose: int = 0):
	""" Write all the files in the write queue to their respective files

	If a file content didn't change, it won't be written

	Args:
		contains (str): If set, only write the files that contains this string in their path
		verbose (int): If set, turn verbose for multithreading
	"""
	contains = stp.clean_path(contains)

	# Pre-process all contents to have two newlines at the end
	processed_contents: dict[str, str] = {}
	for path, content in FILES_TO_WRITE.items():
		if contains not in path:
			continue

		if not content.endswith("\n\n"):
			content = content.rstrip("\n") + "\n\n"
		processed_contents[path] = content

	# Filter out unchanged files
	filtered_files: dict[str, str] = {
		path: content for path, content in processed_contents.items()
		if path not in INITIAL_FILES_SET or content != INITIAL_FILES[path]
	}

	# Write all the files
	def really_write(file_path: str, content: str):
		with stp.super_open(file_path, "w") as f:
			f.write(content)
	stp.multithreading(really_write, filtered_files.items(), use_starmap=True, desc="Writing all files" if verbose > 0 else "")

def write_file(file_path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the file at the given path.

	If you wish to write to the load/tick files or other versioned files,
	use the dedicated function instead (write_versioned_file)

	Args:
		file_path	(str):	The path to the file
		content		(str):	The content to write
		overwrite	(bool):	If the file should be overwritten (default: Append the content)
		prepend		(bool):	If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	# Clean path
	file_path = stp.clean_path(file_path)

	# If content is a dictionnary, dump it
	if isinstance(content, dict):
		content = stp.super_json_dump(content)

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
		FILES_TO_WRITE[file_path] = stp.super_json_dump(merged)
		return

	# Add the content to the file
	if prepend:
		FILES_TO_WRITE[file_path] = str(content) + FILES_TO_WRITE[file_path]
	else:
		FILES_TO_WRITE[file_path] += str(content)

def write_versioned_function(config: dict, relative_path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the versioned function at the given path\n
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
		stp.error(f"Writing to a {relative_path.split('.')[-1]} file is not allowed using write_versioned_file(), use write_file() instead.")

	# Make sure the path is correct for load/confirm_load
	if relative_path in ["load","confirm_load"]:
		stp.warning(f"You tried to write to the '{relative_path}' file, did you mean to write to the 'load/confirm_load' file instead?")

	# Add .mcfunction to the path
	if relative_path.endswith(".mcfunction"):
		stp.warning("The method write_versioned_file() already adds the '.mcfunction' extension to the path, you don't need to add it yourself.")
	else:
		relative_path += ".mcfunction"

	# Write to the file
	functions_path: str = f"{config['build_datapack']}/data/{config['namespace']}/function/v{config['version']}"
	write_file(f"{functions_path}/{relative_path}", content, overwrite, prepend)

def write_load_file(config: dict, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the load file\n
	Args:
		config		(dict):	The main configuration
		content		(str):	The content to write
		overwrite	(bool):	If the file should be overwritten (default: Append the content)
		prepend		(bool):	If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_versioned_function(config, "load/confirm_load", content, overwrite, prepend)

def write_tick_file(config: dict, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the tick file\n
	Args:
		config		(dict):	The main configuration
		content		(str):	The content to write
		overwrite	(bool):	If the file should be overwritten (default: Append the content)
		prepend		(bool):	If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_versioned_function(config, "tick", content, overwrite, prepend)


