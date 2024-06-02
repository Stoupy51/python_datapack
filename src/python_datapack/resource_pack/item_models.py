
# Imports
from ..utils.io import *
from ..utils.print import *
from ..constants import *

# Utility functions
def get_powered_texture(variants: list[str], side: str, on_off: str) -> str:
	if on_off != "":
		for texture in variants:
			if texture.endswith(side + on_off):
				return texture
	for texture in variants:
		if texture.endswith(side):
			return texture
	error(f"Couldn't find texture for side '{side}' in '{variants}', consider adding missing texture or override the model")
	return ""

# Check if all models are in a string of any variant
def model_in_variants(models: list[str], variants: list[str]) -> bool:
	valid = True
	for model in models:
		if not any(model in x for x in variants):
			valid = False
			break
	return valid

# Function to handle item
def handle_item(config: dict, item: str, data: dict, used_textures: set|None = None):
	block_or_item = "block" if data.get("id") == CUSTOM_BLOCK_VANILLA else "item"
	dest_base_textu = f"{config['build_resource_pack']}/assets/{config['namespace']}/textures/{block_or_item}"

	# Get powered states (if any)
	powered = [""]
	on_textures = []
	for p in config['textures_files']:
		if p.split("/")[-1].startswith(item) and p.endswith("_on.png"):
			powered = ["", "_on"]
			on_textures.append(p)

	# Generate its model file(s)
	for on_off in powered:
		dest_base_model = f"{config['build_resource_pack']}/assets/{config['namespace']}/models/{block_or_item}"
		content = {}
		if data.get(OVERRIDE_MODEL):
			content = data[OVERRIDE_MODEL]
			if on_off:	# Check if the override model has the on/off texture
				for key, texture in content["textures"].items():
					on_off_path = "/".join(texture.split("/")[1:]) + on_off + ".png"
					if on_off_path in config["textures_files"]:
						content["textures"][key] = texture + on_off

		else:
			# If it's a block
			if block_or_item == "block":

				# Get parent
				content = {"parent": "block/cube_all", "textures": {}}

				# Get all variants
				variants = [x.replace(".png", "") for x in config['textures_files'] if "gui/" not in x and x.split("/")[-1].startswith(item)]
				
				## Check in which variants state we are
				# If one texture, apply on all faces
				variants_without_on = [x for x in variants if "_on" not in x]
				if len(variants_without_on) == 1:
					content["textures"]["all"] = f"{config['namespace']}:{block_or_item}/" + get_powered_texture(variants, "", on_off)
				else:
					# Prepare models to check
					cube_bottom_top = ["bottom", "side", "top"]
					orientable = ["front", "side", "top"]
					cube_column = ["end", "side"]

					# Check cube_bottom_top model
					if model_in_variants(cube_bottom_top, variants):
						content["parent"] = "block/cube_bottom_top"
						for side in cube_bottom_top:
							content["textures"][side] = f"{config['namespace']}:{block_or_item}/" + get_powered_texture(variants, side, on_off)
					
					# Check orientable model
					elif model_in_variants(orientable, variants):
						content["parent"] = "block/orientable"
						for side in orientable:
							content["textures"][side] = f"{config['namespace']}:{block_or_item}/" + get_powered_texture(variants, side, on_off)
					
					# Check cube_column model
					elif model_in_variants(cube_column, variants):
						content["parent"] = "block/cube_column"
						for side in cube_column:
							content["textures"][side] = f"{config['namespace']}:{block_or_item}/" + get_powered_texture(variants, side, on_off)
					
					else:
						error(f"Block '{item}' has invalid variants: {variants}, consider adding missing textures or override the model")

			# Else, it's an item
			else:

				# Get parent
				parent = "item/generated"
				if data["id"] != CUSTOM_ITEM_VANILLA:
					parent = data["id"].replace(':', ":item/")
				
				# Get textures
				textures = {"layer0": f"{config['namespace']}:{block_or_item}/{item}{on_off}"}
				if "leather_" in data["id"]:
					textures["layer1"] = textures["layer0"]

				# Setup content
				content = {"parent": parent, "textures": textures}
		
		# Add used textures
		if used_textures is not None and content.get("textures"):
			for texture in content["textures"].values():
				used_textures.add(texture)

		# Copy used textures
		if content.get("textures"):
			for texture in content["textures"].values():
				texture_path = "/".join(texture.split(":")[-1].split("/")[1:])
				source = f"{config['textures_folder']}/{texture_path}.png"
				destination = f"{dest_base_textu}/{texture_path}.png"
				super_copy(source, destination)
				if os.path.exists(source + ".mcmeta"):
					super_copy(source + ".mcmeta", destination + ".mcmeta")
			
		# Write content
		write_to_file(f"{dest_base_model}/{item}{on_off}.json", super_json_dump(content, max_level = 4))



def main(config: dict):

	# For each item,
	used_textures = set()
	for item, data in config['database'].items():
		if data.get("custom_model_data"):
			handle_item(config, item, data, used_textures)

	# Make warning for missing textures
	warns = []
	for texture in used_textures:
		path = config['textures_folder'] + "/" + "/".join(texture.split("/")[1:]) + ".png"
		if not os.path.exists(path):
			warns.append(f"Texture '{path}' not found")
	if warns:
		warning("The following textures are used but missing:\n" + "\n".join(sorted(warns)))
	info("Custom models created")

