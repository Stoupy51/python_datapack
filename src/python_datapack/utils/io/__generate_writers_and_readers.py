
# Imports
import stouputils as stp
from general import DATAPACK_RESOURCE_TYPES

# Constants
ROOT: str = stp.get_root_path(__file__)

# Generate content for _writers.py
writers_content: str = """
# Imports
from .general import path_to_file_path
from .write import write_file

"""

for resource_type in DATAPACK_RESOURCE_TYPES:
	writers_content += f"""
def write_{resource_type}(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	\"\"\" Write the content to the {resource_type.replace('_', ' ')} at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the {resource_type.replace('_', ' ')} (ex: "namespace:folder/{resource_type}_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	\"\"\"
	write_file(path_to_file_path(config, path, "{resource_type}"), content, overwrite, prepend)

"""

# Generate content for _readers.py
readers_content: str = """
# Imports
from .read import read_file
from .general import path_to_file_path

"""

for resource_type in DATAPACK_RESOURCE_TYPES:
	readers_content += f"""
def read_{resource_type}(config: dict, path: str) -> str:
	\"\"\" Read the content of the {resource_type.replace('_', ' ')} at the given path.

	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the {resource_type.replace('_', ' ')} (ex: "namespace:folder/{resource_type}_name")
	Returns:
		str:    The content of the {resource_type.replace('_', ' ')}
	\"\"\"
	return read_file(path_to_file_path(config, path, "{resource_type}"))

"""

# Write the generated content to _writers.py and _readers.py
with open(f"{ROOT}/_writers.py", "w", encoding="utf-8") as f:
	f.write(writers_content)

with open(f"{ROOT}/_readers.py", "w", encoding="utf-8") as f:
	f.write(readers_content)

