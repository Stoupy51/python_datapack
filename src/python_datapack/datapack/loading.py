
# Imports
from ..utils.io import *
from ..utils.print import *
from ..constants import *

def main(config: dict):

	# Setup load json files and tick json file
	write_to_file(f"{config['build_datapack']}/data/load/tags/function/load.json", super_json_dump({"values": [f"#{config['namespace']}:load/main"]}))
	write_to_file(f"{config['build_datapack']}/data/{config['namespace']}/tags/function/load/main.json", super_json_dump({"values": [{"id":f"#{config['namespace']}:load/dependencies","required":False}, f"{config['namespace']}:load/main"]}, max_level = 3))
	calls = [{"id":f"#{namespace}:load", "required": False} for namespace in config['dependencies'].keys()]
	write_to_file(f"{config['build_datapack']}/data/{config['namespace']}/tags/function/load/dependencies.json", super_json_dump({"values": calls}))
	write_to_file(f"{config['build_datapack']}/data/minecraft/tags/function/tick.json", super_json_dump({"values": [f"{config['namespace']}:load/tick_verification"]}))


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


	# Check dependencies
	checks = ""
	for namespace, value in config['dependencies'].items():
		major, minor, patch = value["version"]
		unless_major = f"unless score #{namespace}.major load.status matches {major}.. "
		unless_minor = f"unless score #{namespace}.minor load.status matches {minor}.. " if minor > 0 else ""
		unless_patch = f"unless score #{namespace}.patch load.status matches {patch}.. " if patch > 0 else ""
		checks += f"execute if score #dependency_error {config['namespace']}.data matches 0 {unless_major}{unless_minor}{unless_patch}run scoreboard players set #dependency_error {config['namespace']}.data 1\n"
	content = f"""
## Check if {config['datapack_name']} is loadable (dependencies)
scoreboard players set #dependency_error {config['namespace']}.data 0"""
	content += "\n" + checks + "\n"
	write_to_file(f"{config['datapack_functions']}/load/check_dependencies.mcfunction", content)


	# Waiting for player
	decoder_checks = ""
	for namespace, value in config['dependencies'].items():
		major, minor, patch = value["version"]
		unless_major = f"unless score #{namespace}.major load.status matches {major}.. "
		unless_minor = f"unless score #{namespace}.minor load.status matches {minor}.. " if minor > 0 else ""
		unless_patch = f"unless score #{namespace}.patch load.status matches {patch}.. " if patch > 0 else ""
		name = value["name"]
		url = value["url"]
		decoder_checks += f'execute if score #dependency_error {config["namespace"]}.data matches 1 {unless_major}{unless_minor}{unless_patch}run tellraw @a {{"text":"- [{name}]","color":"gold","clickEvent":{{"action":"open_url","value":"{url}"}}}}\n'
	write_to_file(f"{config['datapack_functions']}/load/waiting_for_player.mcfunction", f"""
# Waiting for a player to get the game version, but stop function if no player found
execute unless entity @p run schedule function {config['namespace']}:load/waiting_for_player 1t replace
execute unless entity @p run return 0
execute store result score #game_version {config['namespace']}.data run data get entity @p DataVersion

# Check if the game version is supported
scoreboard players set #mcload_error {config['namespace']}.data 0
execute unless score #game_version {config['namespace']}.data matches {config['data_version']}.. run scoreboard players set #mcload_error {config['namespace']}.data 1

# Decode errors
execute if score #mcload_error {config['namespace']}.data matches 1 run tellraw @a {{"text":"{config['datapack_name']} Error: This version is made for Minecraft {config['minecraft_version']}+.","color":"red"}}
execute if score #dependency_error {config['namespace']}.data matches 1 run tellraw @a {{"text":"{config['datapack_name']} Error: Libraries are missing\\nplease download the right {config['datapack_name']} datapack\\nor download each of these libraries one by one:","color":"red"}}
{decoder_checks}
# Load {config['datapack_name']}
execute if score #game_version {config['namespace']}.data matches 1.. if score #mcload_error {config['namespace']}.data matches 0 if score #dependency_error {config['namespace']}.data matches 0 run function {config['namespace']}:load/confirm_load

""")


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

