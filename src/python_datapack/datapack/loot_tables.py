
# Imports
from ..utils.io import *
from ..utils.print import *
from ..constants import *

def main(config: dict):

	# For each item in the database, create a loot table
	for item, data in config['database'].items():
		loot_table = {"pools":[{"rolls":1,"entries":[{"type":"minecraft:item", "name": data.get("id")}]}]}

		# Set components
		set_components = {"function":"minecraft:set_components","components":{}}
		for k, v in data.items():
			if k not in NOT_COMPONENTS:
				set_components["components"][f"minecraft:{k}"] = v
		
		# Add functions
		loot_table["pools"][0]["entries"][0]["functions"] = [set_components]

		write_to_file(f"{config['build_datapack']}/data/{config['namespace']}/loot_table/i/{item}.json", super_json_dump(loot_table, max_level = 9))
	
	# Same for external items
	for item, data in config['external_database'].items():
		namespace, item = item.split(":")
		loot_table = {"pools":[{"rolls":1,"entries":[{"type":"minecraft:item", "name": data.get("id")}]}]}
		set_components = {"function":"minecraft:set_components","components":{}}
		for k, v in data.items():
			if k not in NOT_COMPONENTS:
				set_components["components"][f"minecraft:{k}"] = v
		loot_table["pools"][0]["entries"][0]["functions"] = [set_components]
		write_to_file(f"{config['build_datapack']}/data/{config['namespace']}/loot_table/external/{namespace}/{item}.json", super_json_dump(loot_table, max_level = 9))
	
	info("Made loot tables for every item")


	# Loot tables for items with crafting recipes
	for item, data in config['database'].items():
		if data.get(RESULT_OF_CRAFTING):
			results = []
			for d in data[RESULT_OF_CRAFTING]:
				count = d["result_count"]
				if count != 1:
					results.append(count)

			# For each result count, create a loot table for it
			for result_count in results:
				loot_table = {"pools":[{"rolls":1,"entries":[{"type":"minecraft:loot_table","value":f"{config['namespace']}:i/{item}","functions":[{"function":"minecraft:set_count","count":result_count}]}]}]}
				write_to_file(f"{config['build_datapack']}/data/{config['namespace']}/loot_table/i/{item}_x{result_count}.json", super_json_dump(loot_table, max_level = -1), overwrite = True)
	info("Multiple counts loot tables made for every item with crafting recipes")

	# Second loot table for the manual (if present)
	if "manual" in config['database']:
		loot_table = {"pools":[{"rolls":1,"entries":[{"type":"minecraft:loot_table","value":f"{config['namespace']}:i/manual"}]}]}
		write_to_file(f"{config['build_datapack']}/data/{config['namespace']}/loot_table/i/{config['namespace']}_manual.json", super_json_dump(loot_table, max_level = -1), overwrite = True)

	# Make a give all command that gives chests with all the items
	CHEST_SIZE = 27
	total_chests = (len(config['database']) + CHEST_SIZE - 1) // CHEST_SIZE
	lore = json.dumps(config['source_lore']).replace('"', "'")
	chests = []
	database_copy = list(config['database'].items())
	for i in range(total_chests):
		chest_contents = []
	
		# For each slot of the chest, append an item and remove it from the copy
		for j in range(CHEST_SIZE):
			if not database_copy:
				break
			item, data = database_copy.pop(0)
			data = data.copy()
			id = data.get("id")
			for k in NOT_COMPONENTS:	# Remove non-component data
				if data.get(k):
					del data[k]
			json_content = super_json_dump(data, max_level = 0).replace("\n","")
			chest_contents.append(f'{{slot:{j},item:{{count:1,id:"{id}",components:{json_content}}}}}')
		joined_content = ",".join(chest_contents)
		chests.append(f'give @s chest[container=[{joined_content}],custom_name=\'{{"text":"Chest [{i+1}/{total_chests}]","color":"yellow"}}\',lore=["{lore}"]]')
	write_to_file(f"{config['datapack_functions']}/_give_all.mcfunction", "\n" + "\n\n".join(chests) + "\n\n")
	info("Give all function successfully made")

