
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
	block_or_item: str = "item"
	if data.get("id") == CUSTOM_BLOCK_VANILLA or any("block" in x for x in data.get(OVERRIDE_MODEL, {}).values()):
		block_or_item = "block"
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
				cake = ["bottom", "side", "top", "inner"]
				cube_bottom_top = ["bottom", "side", "top"]
				orientable = ["front", "side", "top"]
				cube_column = ["end", "side"]

				# Check cake model
				if model_in_variants(cake, variants):
					content["parent"] = "block/cake"
					for side in cake:
						content["textures"][side.replace("inner","inside")] = f"{config['namespace']}:{block_or_item}/" + get_powered_texture(variants, side, on_off)
					
					# Generate 6 models for each cake slice
					for i in range(1, 7):
						name: str = f"{item}_slice{i}"
						slice_content = {"parent": f"block/cake_slice{i}", "textures": content["textures"]}
						write_to_file(f"{dest_base_model}/{name}{on_off}.json", super_json_dump(slice_content, max_level = 4))

				# Check cube_bottom_top model
				elif model_in_variants(cube_bottom_top, variants):
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
				
				elif data.get(OVERRIDE_MODEL,{}).get("textures") != {}:
					patterns = super_json_dump({
						"cake": cake,
						"cube_bottom_top": cube_bottom_top,
						"orientable": orientable,
						"cube_column": cube_column
					}, max_level = 1)
					error(f"Block '{item}' has invalid variants: {variants},\nconsider overriding the model or adding missing textures to match up one of the following patterns:\n{patterns}")

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
		
		# Add overrides
		for key, value in data.get(OVERRIDE_MODEL, {}).items():
			content[key] = value
		
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
				try:
					super_copy(source, destination)
					if os.path.exists(source + ".mcmeta"):
						super_copy(source + ".mcmeta", destination + ".mcmeta")
				except FileNotFoundError:
					error(f"Texture '{source}' not found")
			
		# Write content if not empty
		if data.get(OVERRIDE_MODEL, None) != {}:
			dump: str = super_json_dump(content, max_level = 4)
		else:
			dump: str = "{}\n"
		write_to_file(f"{dest_base_model}/{item}{on_off}.json", dump)



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

