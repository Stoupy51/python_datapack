
# Imports
from ..utils.print import *
from ..utils.io import *
from ..constants import *

# Constants
BLOCKS = [x.replace("minecraft:", "") for x in (CUSTOM_BLOCK_VANILLA, CUSTOM_ITEM_VANILLA, CUSTOM_BLOCK_ALTERNATIVE)]

# Main function
def main(config: dict):

	# Get every vanilla IDs
	vanilla_ids = set()
	for v in config['database'].values():
		if v.get("custom_model_data"):
			vanilla_ids.add(v.get("id", "").replace("minecraft:", ""))

	# For each vanilla ID, create the json model file
	for id in vanilla_ids:

		# Get the parent of the vanilla model
		block_or_item = "block" if id in BLOCKS else "item"
		if f"minecraft:{id}" == CUSTOM_ITEM_VANILLA:
			content = {"parent": f"block/{id}"}
			block_or_item = "item"	# CUSTOM_ITEM_VANILLA is seen as an item (for ingredients so we prefer to use the item model to link)
		else:
			content = {"parent": f"{block_or_item}/{id}"}
		
		# Get the parent textures
		if id not in BLOCKS:
			content["parent"] = "item/generated"
			if any(f"_{x}" in id for x in ["sword", "shovel", "pickaxe", "axe", "hoe"]):
				content["parent"] = "item/handheld"
			
			# Get layer0 and layer1 if needed
			content["textures"] = {"layer0": f"item/{id}"}
			if id in ["leather_helmet", "leather_chestplate", "leather_leggings", "leather_boots"]:
				content["textures"]["layer1"] = f"item/{id}_overlay"

		# Get overrides
		content["overrides"] = []
		for item, data in config['database'].items():
			if data.get("id", "").replace("minecraft:","") == id and data.get("custom_model_data"):
				content["overrides"].append({"predicate": { "custom_model_data": data["custom_model_data"]}, "model": f"{config['namespace']}:{block_or_item}/{item}" })

				# Additionally, add a "_on" model if there is
				if is_in_write_queue(f"{config['build_resource_pack']}/assets/{config['namespace']}/models/{block_or_item}/{item}_on.json"):
					content["overrides"].append({"predicate": { "custom_model_data": data["custom_model_data"] + 1}, "model": f"{config['namespace']}:{block_or_item}/{item}_on" })
				
				# Additionally, add 6 "_slice{i}" models if there are (cake)
				elif is_in_write_queue(f"{config['build_resource_pack']}/assets/{config['namespace']}/models/{block_or_item}/{item}_slice5.json"):
					for i in range(1, 7):
						content["overrides"].append({"predicate": { "custom_model_data": data["custom_model_data"] + i}, "model": f"{config['namespace']}:{block_or_item}/{item}_slice{i}" })

		# Write the content to the file
		content["overrides"].sort(key=lambda x: x["predicate"]["custom_model_data"])
		write_to_file(
			f"{config['build_resource_pack']}/assets/minecraft/models/item/{id}.json",
			super_json_dump(content).replace('{"','{ "').replace('"}','" }').replace(',"', ', "')
		)


	# Generate Common Signals item model
	content = super_json_dump({"parent": "block/deepslate", "overrides": [{"predicate": { "custom_model_data": 2010000}, "model": f"minecraft:item/none"}]})
	write_to_file(
		f"{config['build_resource_pack']}/assets/minecraft/models/item/deepslate.json",
		content.replace('{"','{ "').replace('"}','" }').replace(',"', ', "')
	)	
	write_to_file(f"{config['build_resource_pack']}/assets/minecraft/models/item/none.json", "{}")

	info("Vanilla models created")

