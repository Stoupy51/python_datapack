
# Imports
from ..utils.io import *
from ..utils.print import *

def main(config: dict):

	# Add the sounds folder to the resource pack
	sounds_names = os.listdir(f"{config['assets_folder']}/sounds")
	if sounds_names:
		for sound in sounds_names:

			# Get sound without spaces and special characters
			sound_file = "".join(char for char in sound.replace(" ", "_") if char.isalnum() or char in "._").lower()
			super_copy(f"{config['assets_folder']}/sounds/{sound}", f"{config['build_resource_pack']}/assets/{config['namespace']}/sounds/{sound_file}")

			# Get sound without file extension
			sound = ".".join(sound.split(".")[:-1])
			sound_file = ".".join(sound_file.split(".")[:-1])

			# Add sound json to sounds.json
			sound_json = {sound_file: {"subtitle": sound, "sounds": [f"{config['namespace']}:{sound_file}"]}}
			write_to_file(f"{config['build_resource_pack']}/assets/{config['namespace']}/sounds.json", super_json_dump(sound_json))	

		info(f"All sounds in '{config['assets_folder']}/sounds/' have been copied to the resource pack")

