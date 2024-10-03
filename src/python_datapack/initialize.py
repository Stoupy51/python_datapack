
# Imports
from .utils.io import *
from .utils.print import *
import shutil

def main(config: dict):
	start_time: float = time.perf_counter()

	# Delete database_debug
	print()
	if config.get("database_debug"):
		shutil.rmtree(config["database_debug"], ignore_errors=True)

	# Read initial files in build folder
	read_initial_files([config["build_datapack"], config["build_resource_pack"]])

	# Setup pack.mcmeta for the datapack
	pack_mcmeta = {"pack":{"pack_format": config["datapack_format"], "description": config["description"]}, "id": config["namespace"]}
	write_to_file(f"{config['build_datapack']}/pack.mcmeta", super_json_dump(pack_mcmeta))

	# Setup pack.mcmeta for the resource pack
	if config.get("resource_pack_format"):
		pack_mcmeta = {"pack":{"pack_format": config["resource_pack_format"], "description": config["description"]}, "id": config["namespace"]}
		write_to_file(f"{config['build_resource_pack']}/pack.mcmeta", super_json_dump(pack_mcmeta))

	# Convert textures names if needed
	if config.get('textures_files'):
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

	# Print total time
	total_time: float = time.perf_counter() - start_time
	info(f"Build initialized in {total_time:.5f}s")

