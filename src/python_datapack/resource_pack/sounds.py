
# Imports
import os
import time
import stouputils as stp
from ..utils.io import super_copy, write_file

def main(config: dict):
	if not config.get("assets_folder") or not os.path.exists(config["assets_folder"] + "/sounds"):
		return

	# Add the sounds folder to the resource pack
	sounds_names: list[str] = os.listdir(f"{config['assets_folder']}/sounds")
	sounds_names = [sound for sound in sounds_names if sound.endswith(".ogg") or sound.endswith(".wav")]
	if sounds_names:
		start_time: float = time.perf_counter()
		for sound in sounds_names:

			# Get sound without spaces and special characters
			sound_file = "".join(char for char in sound.replace(" ", "_") if char.isalnum() or char in "._").lower()
			super_copy(f"{config['assets_folder']}/sounds/{sound}", f"{config['build_resource_pack']}/assets/{config['namespace']}/sounds/{sound_file}")

			# Get sound without file extension
			sound = ".".join(sound.split(".")[:-1])
			sound_file = ".".join(sound_file.split(".")[:-1])

			# Add sound json to sounds.json
			sound_json = {sound_file: {"subtitle": sound, "sounds": [f"{config['namespace']}:{sound_file}"]}}
			write_file(f"{config['build_resource_pack']}/assets/{config['namespace']}/sounds.json", stp.super_json_dump(sound_json))	

		total_time: float = time.perf_counter() - start_time
		stp.info(f"All sounds in '{config['assets_folder']}/sounds/' have been copied to the resource pack in {total_time:.5f}s")


