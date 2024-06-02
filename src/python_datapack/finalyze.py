
# Imports
from .utils.io import *
from .utils.print import *
from .utils.weld import weld_datapack, weld_resource_pack
from .datapack.lang import main as lang_main
from .datapack.headers import main as headers_main
from .datapack.custom_block_ticks import custom_blocks_ticks_and_second_functions
from .resource_pack.check_unused_textures import main as check_unused_textures_main
import shutil

def main(config: dict, user_code: callable):

	# For every file in the merge folder, copy it to the build folder (with append content)
	print()
	for root, _, files in os.walk(config['merge_folder']):
		for file in files:
			merge_path = f"{root}/{file}".replace("\\", "/")
			build_path = merge_path.replace(config['merge_folder'], config['build_folder'])
			
			# Append content to the build file is any
			if FILES_TO_WRITE.get(build_path):

				# If file is not JSON format,
				if not file.endswith(".json"):
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
				if file.endswith((".json",".mcfunction")):
					with super_open(merge_path, "r") as f:
						write_to_file(build_path, f.read())
				
				# Else, just copy the file, such as pack.mcmeta, pack.png, ...
				else:
					super_copy(merge_path, build_path)
	info(f"All content in the '{config['merge_folder']}' folder copied to '{config['build_folder']}'")

	# Run user code
	if user_code:
		user_code(config)
	
	# Second and tick functions for custom blocks
	custom_blocks_ticks_and_second_functions(config)

	# Generate lang file
	if config['enable_translations']:
		lang_main(config)

	# Add a small header for each .mcfunction file
	headers_main(config)

	# Write every pending files
	write_all_files()
	debug("All pending files written")

	# Check not used textures
	check_unused_textures_main(config)


	# Generate zip files
	processes = [
		(config['build_datapack'], f"{config['build_folder']}/{config['datapack_name_simple']}_datapack", config['build_copy_destinations'][0]),
		(config['build_resource_pack'], f"{config['build_folder']}/{config['datapack_name_simple']}_resource_pack", config['build_copy_destinations'][1])
	]
	for source, destination, copy_destination in processes:
		if os.path.exists(source):
			shutil.make_archive(destination, 'zip', source)
			debug(f"'{destination}.zip' file generated")
		else:
			warning(f"'{source}' folder not found")
		if copy_destination:
			try:
				file = f"{destination}.zip".split("/")[-1]
				shutil.copy(f"{destination}.zip", f"{copy_destination}/{file}")
				debug(f"'{destination}.zip' file copied to '{copy_destination}/{file}'")
			except:
				warning(f"Unable to copy '{destination}.zip' to '{copy_destination}'")


	# Copy datapack libraries
	try:
		for root, _, files in os.walk(config['libs_folder'] + "/datapack"):
			for file in files:
				if file.endswith(".zip"):
					shutil.copy(f"{root}/{file}", config['build_copy_destinations'][0])
					info(f"Library '{file}' copied to '{config['build_copy_destinations'][0]}/'")
	except:
		warning(f"Could not copy datapack libraries to '{config['build_copy_destinations'][0]}/'")


	# If merge libs is enabled, use weld to generate datapack and resource pack with bundled libraries
	if config['merge_libs']:
		weld_dp = f"{config['build_folder']}/{config['datapack_name_simple']}_datapack_with_libs.zip"
		weld_rp = f"{config['build_folder']}/{config['datapack_name_simple']}_resource_pack_with_libs.zip"
		weld_datapack(weld_dp)
		weld_resource_pack(weld_rp)
		try:
			shutil.copy(weld_rp, config['build_copy_destinations'][1])
		except OSError:
			pass
		info("Datapack and resource pack merged with bundled libraries")

