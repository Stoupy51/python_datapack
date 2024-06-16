
# Imports
from ..utils.io import *
from ..utils.print import *
from ..constants import *

def main(config: dict):
	version: str = config['version']
	namespace: str = config['namespace']
	major, minor, patch = version.split(".")

	# Setup enumerate and resolve functions
	write_to_file(f"{config['datapack_functions']}/v{version}/load/enumerate.mcfunction", f"""
# If current major is too low, set it to the current major
execute unless score #{namespace}.major load.status matches {major}.. run scoreboard players set #{namespace}.major load.status {major}

# If current minor is too low, set it to the current minor (only if major is correct)
execute if score #{namespace}.major load.status matches {major} unless score #{namespace}.minor load.status matches {minor}.. run scoreboard players set #{namespace}.minor load.status {minor}

# If current patch is too low, set it to the current patch (only if major and minor are correct)
execute if score #{namespace}.major load.status matches {major} if score #{namespace}.minor load.status matches {minor} unless score #{namespace}.patch load.status matches {patch}.. run scoreboard players set #{namespace}.patch load.status {patch}
""")
	write_to_file(f"{config['datapack_functions']}/v{version}/load/resolve.mcfunction", f"""
# If correct version, load the datapack
execute if score #{namespace}.major load.status matches {major} if score #{namespace}.minor load.status matches {minor} if score #{namespace}.patch load.status matches {patch} run function {namespace}:v{version}/load/main
""")
	
	# Setup enumerate and resolve function tags
	write_to_file(f"{config['build_datapack']}/data/{namespace}/tags/function/enumerate.json", super_json_dump({"values": [f"{namespace}:v{version}/load/enumerate"]}))
	write_to_file(f"{config['build_datapack']}/data/{namespace}/tags/function/resolve.json", super_json_dump({"values": [f"{namespace}:v{version}/load/resolve"]}))

	# Setup load main function
	write_to_file(f"{config['datapack_functions']}/v{version}/load/main.mcfunction", f"""
# Avoiding multiple executions of the same load function
execute unless score #{namespace}.loaded load.status matches 1 run function {namespace}:v{version}/load/secondary

""")

	# Confirm load
	items_storage = ""	# Storage representation of every item in the database
	if config['database']:
		items_storage += f"\n# Items storage\ndata modify storage {namespace}:items all set value {{}}\n"
		for item, data in config['database'].items():
			mc_data = {"id":"","count":1, "components":{"custom_model_data":-1}}
			for k, v in data.items():
				if k not in NOT_COMPONENTS:
					mc_data["components"][k] = v
				elif k == "id":
					mc_data[k] = v
			if mc_data["components"]["custom_model_data"] == -1:
				del mc_data["components"]["custom_model_data"]
			items_storage += f"data modify storage {namespace}:items all.{item} set value " + super_json_dump(mc_data, max_level = 0)
		pass

	write_to_file(f"{config['datapack_functions']}/v{version}/load/confirm_load.mcfunction", f"""
tellraw @a[tag=convention.debug] {{"text":"[Loaded {config['datapack_name']} v{version}]","color":"green"}}

scoreboard players set #{namespace}.loaded load.status 1
""" + items_storage)

	info("All loading functions and tags created")

