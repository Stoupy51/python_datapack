
# Imports
from ..constants import *
from ..utils.print import *
from ..utils.io import *

# This folder path
OFFICIAL_LIBS_PATH = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")

# Util function for checking version
def check_version(config: dict, lib_ns: str, data: dict, run_command: str) -> str:
	namespace: str = config['namespace']
	checks: str = ""
	major, minor, patch = data["version"]
	score_major: str = f"score #{lib_ns}.major load.status matches {major}"
	score_minor: str = f"score #{lib_ns}.minor load.status matches {minor}"
	score_patch: str = f"score #{lib_ns}.patch load.status matches {patch}" if patch > 0 else ""

	# Check if the version is correct
	is_decoder: int = 1 if "tellraw @" in run_command else 0
	checks += f"execute if score #dependency_error {namespace}.data matches {is_decoder} unless {score_major}.. run {run_command}\n"
	checks += f"execute if score #dependency_error {namespace}.data matches {is_decoder} if {score_major} unless {score_minor}.. run {run_command}\n"
	if score_patch:
		checks += f"execute if score #dependency_error {namespace}.data matches {is_decoder} if {score_major} if {score_minor} unless {score_patch}.. run {run_command}\n"
	return checks

# Main function called on finalization process
def main(config: dict) -> None:
	namespace: str = config['namespace']

	# Find if common_signals is used
	if namespace != "common_signals":
		for file_content in FILES_TO_WRITE.values():
			if "common_signals" in file_content:
				OFFICIAL_LIBS["common_signals"]["is_used"] = True
				if not official_lib_used("common_signals"):
					info("Found the use of official supported library 'common_signals', adding it to the datapack")
				break
	dependencies: list[tuple] = [(ns, data) for ns, data in OFFICIAL_LIBS.items() if data["is_used"]]
	dependencies += list(config['dependencies'].items())

	# Setup Lantern Load
	write_to_file(f"{config['build_datapack']}/data/minecraft/tags/function/load.json", super_json_dump({"values": ["#load:_private/load"]}))
	write_to_file(f"{config['build_datapack']}/data/load/tags/function/_private/load.json", super_json_dump({"values": ["#load:_private/init",{"id":"#load:pre_load","required":False},{"id":"#load:load","required":False},{"id":"#load:post_load","required":False}]}))
	write_to_file(f"{config['build_datapack']}/data/load/function/_private/init.mcfunction", f"""
# Reset scoreboards so packs can set values accurate for current load.
scoreboard objectives add load.status dummy
scoreboard players reset * load.status
""")

	# Setup load json files and tick json file
	write_to_file(f"{config['build_datapack']}/data/load/tags/function/load.json", super_json_dump({"values": [f"#{namespace}:load/main"]}))
	write_to_file(f"{config['build_datapack']}/data/{namespace}/tags/function/load/main.json", super_json_dump({"values": [{"id":f"#{namespace}:load/dependencies","required":False}, f"{namespace}:load/main"]}, max_level = 3))
	calls = [{"id":f"#{namespace}:load", "required": False} for namespace, _ in dependencies]
	write_to_file(f"{config['build_datapack']}/data/{namespace}/tags/function/load/dependencies.json", super_json_dump({"values": calls}))
	write_to_file(f"{config['build_datapack']}/data/minecraft/tags/function/tick.json", super_json_dump({"values": [f"{namespace}:load/tick_verification"]}))
	
	# For each used library, show message
	message = ""
	for data in OFFICIAL_LIBS.values():
		if data["is_used"]:
			message += f" - {data['name']}\n"
	if message:
		info(f"Summary of the official supported libraries used in the datapack:\n{message}")

	## Write check_dependencies and waiting_for_player functions now that we have all the dependencies
	encoder_checks = ""
	decoder_checks = ""
	for lib_ns, value in dependencies:

		# Encoder check
		encoder_command: str = f"scoreboard players set #dependency_error {namespace}.data 1"
		encoder_checks += check_version(config, lib_ns, value, encoder_command)

		# Decoder check
		name, url = value["name"], value["url"]
		decoder_command: str = f'tellraw @a {{"text":"- [{name}]","color":"gold","clickEvent":{{"action":"open_url","value":"{url}"}}}}'
		decoder_checks += check_version(config, lib_ns, value, decoder_command)

	# Write check_dependencies.mcfunction
	write_to_file(f"{config['datapack_functions']}/load/check_dependencies.mcfunction", f"""
## Check if {config['datapack_name']} is loadable (dependencies)
scoreboard players set #dependency_error {namespace}.data 0
{encoder_checks}
""")

	# Waiting for player
	write_to_file(f"{config['datapack_functions']}/load/waiting_for_player.mcfunction", f"""
# Waiting for a player to get the game version, but stop function if no player found
execute unless entity @p run schedule function {namespace}:load/waiting_for_player 1t replace
execute unless entity @p run return 0
execute store result score #game_version {namespace}.data run data get entity @p DataVersion

# Check if the game version is supported
scoreboard players set #mcload_error {namespace}.data 0
execute unless score #game_version {namespace}.data matches {config['data_version']}.. run scoreboard players set #mcload_error {namespace}.data 1

# Decode errors
execute if score #mcload_error {namespace}.data matches 1 run tellraw @a {{"text":"{config['datapack_name']} Error: This version is made for Minecraft {config['minecraft_version']}+.","color":"red"}}
execute if score #dependency_error {namespace}.data matches 1 run tellraw @a {{"text":"{config['datapack_name']} Error: Libraries are missing\\nplease download the right {config['datapack_name']} datapack\\nor download each of these libraries one by one:","color":"red"}}
{decoder_checks}
# Load {config['datapack_name']}
execute if score #game_version {namespace}.data matches 1.. if score #mcload_error {namespace}.data matches 0 if score #dependency_error {namespace}.data matches 0 run function {namespace}:load/confirm_load

""")

	return

