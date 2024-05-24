
# Imports
from ..utils.io import *
from ..utils.print import *
from ..constants import *

# Function to handle item
def handle_item(config: dict, item: str, data: dict, used_textures: set|None = None):
	block_or_item = "block" if data.get("id") == CUSTOM_BLOCK_VANILLA else "item"
	dest_base_textu = f"{config['build_resource_pack']}/assets/{config['namespace']}/textures/{block_or_item}"

	# Get every block variant
	variants = FACES + SIDES + ("_on",)
	armors = ["helmet", "chestplate", "leggings", "boots"]
	tools = ["sword", "pickaxe", "axe", "shovel", "hoe"]

	# Copy textures to the resource pack
	source = f"{config['textures_folder']}/{item}.png"
	if os.path.exists(source):
		destination = f"{dest_base_textu}/{item}.png"
		super_copy(source, destination)

	# Get all textures for the item
	additional_textures = []
	for file in config['textures_files']:
		if file.startswith(item):
			if any(x in file.replace(item, "") for x in variants):
				additional_textures.append(file.replace(".png", ""))	# Only keep the textures for SIDES/FACES

			# Copy textures to the resource pack
			source = f"{config['textures_folder']}/{file}"
			destination = f"{dest_base_textu}/{file}"
			super_copy(source, destination)
		pass

	# Generate its model file
	powered = ["","_on"] if any(x for x in additional_textures if x.endswith("_on")) > 0 else [""]
	for on_off in powered:
		dest_base_model = f"{config['build_resource_pack']}/assets/{config['namespace']}/models/{block_or_item}"
		if block_or_item == "block":
			content = {"parent": "block/cube_all"}
			content["textures"] = {}

			# If only one, apply everywhere
			if not additional_textures:
				content["textures"]["all"] = f"{config['namespace']}:{block_or_item}/{item}"

			# If more than one, apply to each side
			else:
				content["elements"] = [{"from": [0, 0, 0], "to": [16, 16, 16], "faces": {}}]
				default_texture = f"{config['namespace']}:{block_or_item}/{item}{on_off}"

				# Generate links between FACES and textures
				for face in FACES:
					content["elements"][0]["faces"][face] = {"texture": f"#{face}", "cullface": face}
					content["textures"][face] = default_texture
	
				# For each possible side (in reverse order)
				for i in range(len(SIDES), 0, -1):
					side = SIDES[i - 1].replace("_", "")
	
					# If we have a texture for the side
					if any(side in x for x in additional_textures):

						# Get path
						path = f"{config['namespace']}:{block_or_item}/{item}_{side}"
						if on_off == "_on" and f"{item}_{side}_on" in additional_textures:
							path += "_on"
						if used_textures is not None:
							used_textures.add(path)

						# If it's a side, apply to all FACES (as it is first, it will be overwritten by the others)
						if side == "side":
							for face in FACES:
								content["textures"][face] = path

						# Else, apply the texture to the face with the same name
						else:
							face = FACES[i - 1]
							content["textures"][face] = path
	
							# Exception: apply top texture also to bottom
							if face == "up":
								content["textures"]["down"] = path

		# Else, it's an item
		else:

			path = f"{config['namespace']}:{block_or_item}/{item}{on_off}"
			if used_textures is not None:
				used_textures.add(path)
			content = {"parent": "item/generated",	"textures": {"layer0": path}}
			if any(x in item for x in armors):
				content["textures"]["layer1"] = content["textures"]["layer0"]
			if any(x in item for x in tools):
				content["parent"] = "item/handheld"
			
		# Write content
		write_to_file(f"{dest_base_model}/{item}{on_off}.json", super_json_dump(content, max_level = 4))

		# Generate placed models for item_display if it's a block
		if block_or_item == "block":
			dest_base_model = f"{config['build_resource_pack']}/assets/{config['namespace']}/models/{block_or_item}/for_item_display"
			content["display"] = MODEL_DISPLAY
			write_to_file(f"{dest_base_model}/{item}{on_off}.json", super_json_dump(content, max_level = 4))


def main(config: dict):

	# For each item,
	used_textures = set()
	for item, data in config['database'].items():
		handle_item(config, item, data, used_textures)

	# Make warning for missing textures
	warns = []
	for texture in used_textures:
		path = config['textures_folder'] + "/" + texture.split("/")[-1] + ".png"
		if not os.path.exists(path):
			warns.append(f"Texture '{path}' not found")
	if warns:
		warning("The following textures are used but missing:\n" + "\n".join(sorted(warns)))
	info("Custom models created")

