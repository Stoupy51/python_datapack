
# Imports
from .utils.io import *
from .utils.print import *
from .utils.weld import weld_datapack, weld_resource_pack
from .utils.archive import make_archive
from .datapack.lang import main as lang_main
from .datapack.headers import main as headers_main
from .datapack.basic_structure import main as basic_structure_main
from .datapack.custom_block_ticks import custom_blocks_ticks_and_second_functions
from .resource_pack.check_unused_textures import main as check_unused_textures_main
from .dependencies.main import main as dependencies_main, OFFICIAL_LIBS_PATH, OFFICIAL_LIBS
import shutil

def main(config: dict, user_code: callable):

	# Copy original_icon.png to pack.png if it exists
	if config.get('assets_folder') and os.path.exists(f"{config['assets_folder']}/original_icon.png"):
		super_copy(f"{config['assets_folder']}/original_icon.png", f"{config['build_datapack']}/pack.png")
		if config.get('resource_pack_format'):
			super_copy(f"{config['assets_folder']}/original_icon.png", f"{config['build_resource_pack']}/pack.png")

	# For every file in the merge folder, copy it to the build folder (with append content)
	if config.get('merge_folder'):
		print()
		start_time: float = time.perf_counter()
		for root, _, files in os.walk(config['merge_folder']):
			for file in files:
				merge_path = f"{root}/{file}".replace("\\", "/")
				build_path = merge_path.replace(config['merge_folder'], config['build_folder'])
				
				# Append content to the build file is any
				if FILES_TO_WRITE.get(build_path):

					# If file is not JSON format,
					if not file.endswith(".json") and not file.endswith(".mcmeta"):
						with super_open(merge_path, "r") as f:
							write_to_file(build_path, f.read())

					else:
						# Load to two dictionnaries
						with super_open(merge_path, "r") as f:
							merge_dict = json.load(f)
						build_dict = json.loads(FILES_TO_WRITE[build_path])
						
						# Write the merged dictionnaries to the build file
						FILES_TO_WRITE[build_path] = super_json_dump(super_merge_dict(build_dict, merge_dict), max_level = -1)
				else:
					# Get content of .mcfunction file to correctly append headers
					if file.endswith((".json",".mcfunction",".mcmeta")):
						with super_open(merge_path, "r") as f:
							write_to_file(build_path, f.read())
					
					# Else, just copy the file, such as pack.mcmeta, pack.png, ...
					else:
						super_copy(merge_path, build_path)
		total_time: float = time.perf_counter() - start_time
		info(f"All content in the '{config['merge_folder']}' folder copied to '{config['build_folder']}' in {total_time:.5f}s")

	# Run user code
	if user_code:
		start_time: float = time.perf_counter()
		user_code(config)
		total_time: float = time.perf_counter() - start_time
		info(f"User code ran in {total_time:.5f}s")
	
	# Second and tick functions for custom blocks
	custom_blocks_ticks_and_second_functions(config)

	# Generate basic datapack structure (tick, tick_2, second, second_5, minute) if needed
	basic_structure_main(config)

	# Check for official libs uses
	dependencies_main(config)

	# Generate lang file
	if config.get('enable_translations') == True:
		lang_main(config)

	# Add a small header for each .mcfunction file
	headers_main(config)

	# Write every pending files
	start_time: float = time.perf_counter()
	write_all_files()
	total_time: float = time.perf_counter() - start_time
	info(f"All pending files written in {total_time:.5f}s")

	# Check not used textures
	if config.get('textures_folder'):
		check_unused_textures_main(config)


	# Generate zip files
	datapack_dest: list[str] = config['build_copy_destinations'][0] if config.get('build_copy_destinations') else []
	resourcepack_dest: list[str] = config['build_copy_destinations'][1] if config.get('build_copy_destinations') and len(config['build_copy_destinations']) > 1 else []
	processes = [
		(config['build_datapack'],			f"{config['build_folder']}/{config['datapack_name_simple']}_datapack",			datapack_dest),
		(config['build_resource_pack'],		f"{config['build_folder']}/{config['datapack_name_simple']}_resource_pack",		resourcepack_dest)
	]
	for source, destination, copy_destinations in processes:
		if os.path.exists(source):
			total_time: float = make_archive(source, destination, copy_destinations)
			debug(f"'{destination}.zip' file generated and copied to destinations in {total_time:.5f}s")

	# Copy datapack libraries
	try:
		
		# Copy lib folder
		if config.get('libs_folder'):
			for root, _, files in os.walk(config['libs_folder'] + "/datapack"):
				for file in files:
					if file.endswith(".zip"):
						shutil.copy(f"{root}/{file}", datapack_dest)
						info(f"Library '{file}' copied to '{datapack_dest}/'")
		
		# Copy official used libs
		for data in OFFICIAL_LIBS.values():
			if data["is_used"]:
				name: str = data["name"]
				shutil.copy(f"{OFFICIAL_LIBS_PATH}/datapack/{name}.zip", datapack_dest)
				info(f"Library '{name}.zip' copied to '{datapack_dest}/'")
		
	except OSError as e:
		warning(f"Could not copy datapack libraries to '{datapack_dest}/': {e}")


	# If merge libs is enabled, use weld to generate datapack and resource pack with bundled libraries
	if config.get('merge_libs') == True:

		# Merge weld dp
		weld_dp: str = f"{config['build_folder']}/{config['datapack_name_simple']}_datapack_with_libs.zip"
		weld_dp_time: float = weld_datapack(config, weld_dp)

		# Merge weld rp and copy to resourcepack_dest if possible
		weld_rp: str = f"{config['build_folder']}/{config['datapack_name_simple']}_resource_pack_with_libs.zip"
		weld_rp_time: float = weld_resource_pack(config, weld_rp)
		try:
			shutil.copy(weld_rp, resourcepack_dest)
		except OSError:
			pass

		# Debug time taken
		total_time: float = weld_dp_time + weld_rp_time
		info(f"Datapack and resource pack merged with bundled libraries in {total_time:.5f}s ({weld_dp_time:.5f}s + {weld_rp_time:.5f}s)")

