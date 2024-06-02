
# Imports
from ..utils.print import *
from ..utils.io import *

# Setup custom blocks ticks and second functions calls
def custom_blocks_ticks_and_second_functions(config: dict) -> None:
	""" Setup custom blocks ticks and second functions calls\n
	It will seek for "second.mcfunction" and "tick.mcfunction" files in the custom_blocks folder\n
	Then it will generate all functions to lead to the execution of these files by adding tags\n
	Args:
		config (dict): The config dictionary\n
	"""
	namespace: str = config['namespace']
	build_datapack: str = config['build_datapack']
	custom_blocks = f"{build_datapack}/data/{namespace}/function/custom_blocks/"
	
	# Get second and ticks functions
	custom_blocks_second = []
	custom_blocks_tick = []
	for path in FILES_TO_WRITE:
		if custom_blocks in path:
			custom_block = path.split(custom_blocks)[1]
			if custom_block.count("/") == 1:
				splitted = custom_block.split("/")
				function_name = splitted[1].replace(".mcfunction", "")
				custom_block = splitted[0]
				if function_name == "second":
					custom_blocks_second.append(custom_block)
				elif function_name == "tick":
					custom_blocks_tick.append(custom_block)
	
	# For each custom block, add tags when placed
	for custom_block in custom_blocks_second:
		write_to_file(f"{custom_blocks}{custom_block}/place_secondary.mcfunction", f"\n# Add tag for loop every second\ntag @s add {namespace}.second")
	for custom_block in custom_blocks_tick:
		write_to_file(f"{custom_blocks}{custom_block}/place_secondary.mcfunction", f"\n# Add tag for loop every tick\ntag @s add {namespace}.tick")
	
	# Write second functions
	if custom_blocks_second:
		write_to_file(f"{build_datapack}/data/{namespace}/function/second.mcfunction", f"\n# Custom blocks second functions\nexecute as @e[tag={namespace}.second] at @s run function {namespace}:custom_blocks/second")
		content = "\n".join(f"execute if entity @s[tag={namespace}.{custom_block}] run function {namespace}:custom_blocks/{custom_block}/second" for custom_block in custom_blocks_second)
		write_to_file(f"{build_datapack}/data/{namespace}/function/custom_blocks/second.mcfunction", content)
	
	# Write tick functions
	if custom_blocks_tick:
		write_to_file(f"{build_datapack}/data/{namespace}/function/tick.mcfunction", f"\n# Custom blocks tick functions\nexecute as @e[tag={namespace}.tick] at @s run function {namespace}:custom_blocks/tick")
		content = "\n".join(f"execute if entity @s[tag={namespace}.{custom_block}] run function {namespace}:custom_blocks/{custom_block}/tick" for custom_block in custom_blocks_tick)
		write_to_file(f"{build_datapack}/data/{namespace}/function/custom_blocks/tick.mcfunction", content)

