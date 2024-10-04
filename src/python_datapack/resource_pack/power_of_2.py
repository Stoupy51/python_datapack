
# Imports
from ..utils.io import *
from ..utils.print import *
from PIL import Image

def main(config: dict):

	# Create a test texture (to comment this line after testing)
	# img = Image.new('RGB', (17,17), color = 'red')
	# img.save(f"{config['build_resource_pack']}/assets/{config['namespace']}/textures/item/test.png")

	# Get all textures in the resource pack folder
	wrongs: list[str] = []
	for root, _, files in os.walk(f"{config['build_resource_pack']}/assets/{config['namespace']}/textures"):
		for file in files:
			if file.endswith(".png") and ("block" in root or "item" in root):
				file_path: str = clean_path(f"{root}/{file}")

				# Check if the texture is in power of 2 resolution
				image: Image.Image = Image.open(file_path)
				width, height = image.size
				if bin(width).count("1") != 1 or bin(height).count("1") != 1:
					wrongs.append((file_path, width, height))

	# Print all wrong textures
	if wrongs:
		text: str = f"The following textures are not in power of 2 resolution (2x2, 4x4, 8x8, 16x16, ...):\n"
		for file_path, width, height in wrongs:
			text += f"- {file_path}\t({width}x{height})\n"
		warning(text)

