
# Imports
import os
import time
import stouputils as stp
from ..utils.io import super_copy, write_file


def main(config: dict):
	sounds_folder: str = stp.clean_path(config.get("assets_folder", "") + "/sounds")
	if sounds_folder != "/sounds" and not os.path.exists(sounds_folder):
		return

	# Get all files
	all_files: list[str] = [stp.clean_path(f"{root}/{file}") for root, _, files in os.walk(sounds_folder) for file in files]
	sounds_names = [sound for sound in all_files if sound.endswith(".ogg") or sound.endswith(".wav")]

	# Add the sounds folder to the resource pack
	if sounds_names:
		start_time: float = time.perf_counter()
		for sound in sounds_names:
			sound = sound.replace(sounds_folder + "/", "")
			#stp.breakpoint(sound)

			# Get sound without spaces and special characters
			sound_file = "".join(char for char in sound.replace(" ", "_") if char.isalnum() or char in "._/").lower()
			super_copy(f"{sounds_folder}/{sound}", f"{config['build_resource_pack']}/assets/{config['namespace']}/sounds/{sound_file}")

			# Get sound without file extension
			sound = ".".join(sound.split(".")[:-1])
			sound_file = ".".join(sound_file.split(".")[:-1])

			# Add sound json to sounds.json
			sound_json = {sound_file: {"subtitle": sound, "sounds": [f"{config['namespace']}:{sound_file}"]}}
			write_file(f"{config['build_resource_pack']}/assets/{config['namespace']}/sounds.json", stp.super_json_dump(sound_json))

		total_time: float = time.perf_counter() - start_time
		stp.info(f"All sounds in '{sounds_folder}/' have been copied to the resource pack in {total_time:.5f}s")


