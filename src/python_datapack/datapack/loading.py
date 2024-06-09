
# Imports
from ..utils.io import *
from ..utils.print import *
from ..constants import *

def main(config: dict):

	# Setup load main and secondary function
	write_to_file(f"{config['datapack_functions']}/load/main.mcfunction", f"""
# Avoiding multiple executions of the same load function
execute unless score {config['datapack_name_simple']} load.status matches 1.. run function {config['namespace']}:load/secondary

""")
	major, minor, patch = config['version'].split(".")
	authors = config['author'].split(" ")
	convention_debug = "".join([f"tag {author} add convention.debug\n" for author in authors])
	content = f"""
# {config['datapack_name']}
scoreboard objectives add {config['namespace']}.data dummy
scoreboard players set #{config['namespace']}.major load.status {major}
scoreboard players set #{config['namespace']}.minor load.status {minor}
scoreboard players set #{config['namespace']}.patch load.status {patch}
{convention_debug}

# Check dependencies and wait for a player to connect (to get server version)
function {config['namespace']}:load/check_dependencies
function {config['namespace']}:load/waiting_for_player

"""
	write_to_file(f"{config['datapack_functions']}/load/secondary.mcfunction", content)

	# Confirm load
	items_storage = ""	# Storage representation of every item in the database
	content = ""
	for item, data in config['database'].items():
		mc_data = {"id":"","count":1, "components":{"custom_model_data":-1}}
		for k, v in data.items():
			if k not in NOT_COMPONENTS:
				mc_data["components"][k] = v
			elif k == "id":
				mc_data[k] = v
		if mc_data["components"]["custom_model_data"] == -1:
			del mc_data["components"]["custom_model_data"]
		items_storage += f"data modify storage {config['namespace']}:items all.{item} set value " + super_json_dump(mc_data, max_level = 0)
		pass

	write_to_file(f"{config['datapack_functions']}/load/confirm_load.mcfunction", f"""
tellraw @a[tag=convention.debug] {{"text":"[Loaded {config['datapack_name']} v{config['version']}]","color":"green"}}

scoreboard objectives add {config['namespace']}.private dummy
scoreboard objectives add {config['namespace']}.right_click minecraft.used:minecraft.warped_fungus_on_a_stick

scoreboard players set #{config['namespace']}.loaded load.status 1
# "#second" starts at a random time for better load distribution
execute store result score #second {config['namespace']}.data run random value 1..19

# Items storage
data modify storage {config['namespace']}:items all set value {{}}
{items_storage}
""")


	# Tick verification
	write_to_file(f"{config['datapack_functions']}/load/tick_verification.mcfunction", f"""
execute if score #{config['namespace']}.loaded load.status matches 1 run function {config['namespace']}:tick

""")
	info("All loading functions and tags created")

