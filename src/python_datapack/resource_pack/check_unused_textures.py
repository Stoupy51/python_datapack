
# Imports
from ..utils.io import *
from ..utils.print import *

def main(config: dict):

	# Check for all unused textures
	unused_textures = [x.replace(".png","") for x in config['textures_files']]
	json_files_content = [x[1] for x in FILES_TO_WRITE.items() if x[0].endswith(".json")]
	for file_content in json_files_content:
		for texture in unused_textures.copy():

			# Remove texture from the list if it is used in the json file, ex: /adamantium_ore"
			to_check = f'/{texture}"'
			if to_check in file_content or to_check.replace('"','.png') in file_content:
				unused_textures.remove(texture)

	# Print out loud
	not_used = ""
	for texture in unused_textures:
		path = f"{config['textures_folder']}/{texture}"
		not_used += (f"\n'{path}.png' not found in the resource pack")
	if not_used:
		warning("Some textures are not used in the resource pack: " + not_used)

