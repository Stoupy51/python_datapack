
# Imports
from ..utils.io import *
from ..utils.print import *

def main(config: dict):

	# Tick structure, tick_2 and second_5 are "offsync" for a better load distribution
	write_to_file(f"{config['datapack_functions']}/tick.mcfunction", f"""
	# Timers
	scoreboard players add #tick_2 {config['namespace']}.data 1
	scoreboard players add #second {config['namespace']}.data 1
	scoreboard players add #second_5 {config['namespace']}.data 1
	scoreboard players add #minute {config['namespace']}.data 1
	execute if score #tick_2 {config['namespace']}.data matches 3.. run function {config['namespace']}:tick_2
	execute if score #second {config['namespace']}.data matches 20.. run function {config['namespace']}:second
	execute if score #second_5 {config['namespace']}.data matches 90.. run function {config['namespace']}:second_5
	execute if score #minute {config['namespace']}.data matches 1200.. run function {config['namespace']}:minute
	""")

	# Write remaining files
	write_to_file(f"{config['datapack_functions']}/tick_2.mcfunction", f"""
	# Reset timer
	scoreboard players set #tick_2 {config['namespace']}.data 1
	""")
	write_to_file(f"{config['datapack_functions']}/second.mcfunction", f"""
	# Reset timer
	scoreboard players set #second {config['namespace']}.data 0
	""")
	write_to_file(f"{config['datapack_functions']}/second_5.mcfunction", f"""
	# Reset timer
	scoreboard players set #second_5 {config['namespace']}.data -10
	""")
	write_to_file(f"{config['datapack_functions']}/minute.mcfunction", f"""
	# Reset timer
	scoreboard players set #minute {config['namespace']}.data 1
	""")


