
# Imports
import stouputils as stp

from ..utils.io import FILES_TO_WRITE


def main(config: dict) -> None:
	"""Check for unused textures in the resource pack.

	Args:
		config (dict): Configuration containing texture files and assets folder.
	"""
	# Create a set of textures for efficient lookups and removals
	unused_textures: set[str] = {x.replace(".png", "") for x in config["textures_files"]}

	# Only process JSON files
	json_files_content: list = [content for path, content in FILES_TO_WRITE.items() if path.endswith(".json")]

	# Check each JSON file for texture references
	for file_content in json_files_content:

		# Create a copy since we'll modify while iterating
		for texture in unused_textures.copy():

			# Check different formats of texture references
			for prefix in "/:":
				ref: str = f'{prefix}{texture}"'
				png_ref: str = ref.replace('"', '.png')

				# Remove texture from unused set if it's referenced
				if ref in file_content or png_ref in file_content:
					unused_textures.discard(texture)
					break

	# Report unused textures
	if unused_textures:
		unused_paths = [f"'{config['assets_folder']}/textures/{texture}.png'" for texture in unused_textures]
		warning_msg = "Some textures are not used in the resource pack:\n" + "\n".join(
			f"{path} not used in the resource pack" for path in sorted(unused_paths)
		)
		stp.warning(warning_msg)

