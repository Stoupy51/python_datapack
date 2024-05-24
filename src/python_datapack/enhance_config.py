
import os
def main(config: dict) -> dict:

	# Assets files
	config['assets_files'] = [f"{root}/{f}".replace("\\","/") for root, _, files in os.walk(config['assets_folder']) for f in files]
	config['textures_files'] = [path.split(f"{config['textures_folder']}/")[1] for path in config['assets_files'] if path.startswith(config['textures_folder']) and path.endswith(".png")]

	# Datapack related constants
	config['datapack_name_simple'] = "".join([c for c in config['datapack_name'] if c.isalnum()])		# Simplified version of the datapack name, used for paths

	# Technical constants
	config['build_datapack'] = f"{config['build_folder']}/datapack"										# Folder where the final datapack will be built
	config['datapack_functions'] = f"{config['build_datapack']}/data/{config['namespace']}/function"	# Folder where the datapack functions are built
	config['build_resource_pack'] = f"{config['build_folder']}/resource_pack"							# Folder where the final resource pack will be built

	return config

