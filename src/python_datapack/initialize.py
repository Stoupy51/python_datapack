
# Imports
from .utils.io import *
from .utils.print import *
import shutil

def main(config: dict):

	# Delete build folder and database_debug
	print()
	shutil.rmtree(config["build_folder"], ignore_errors=True)
	shutil.rmtree(config["database_debug"], ignore_errors=True)

	# Setup pack.mcmeta for the datapack
	pack_mcmeta = {"pack":{"pack_format": config["datapack_format"], "description": config["description"]}, "id": config["namespace"]}
	write_to_file(f"{config['build_datapack']}/pack.mcmeta", super_json_dump(pack_mcmeta))
	info(f"pack.mcmeta file created for datapack")

	# Setup pack.mcmeta for the resource pack
	pack_mcmeta = {"pack":{"pack_format": config["resource_pack_format"], "description": config["description"]}, "id": config["namespace"]}
	write_to_file(f"{config['build_resource_pack']}/pack.mcmeta", super_json_dump(pack_mcmeta))
	info(f"pack.mcmeta file created for resource pack")

	# Convert textures names if needed
	REPLACEMENTS = {
		"_off": "",
		"_down": "_bottom",
		"_up": "_top",
		"_north": "_front",
		"_south": "_back",
		"_west": "_left",
		"_east": "_right",
	}
	for file in config['textures_files']:
		new_name = file.lower()
		for k, v in REPLACEMENTS.items():
			if k in file:
				new_name = new_name.replace(k, v)
		if new_name != file:
			os.rename(f"{config['textures_folder']}/{file}", f"{config['textures_folder']}/{new_name}")
			info(f"Renamed {file} to {new_name}")

