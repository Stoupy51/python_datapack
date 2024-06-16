
# Imports
from .loading import main as loading_main
from .basic_structure import main as basic_structure_main
from .custom_blocks import main as custom_blocks_main
from .loot_tables import main as loot_tables_main
from .recipes import main as recipes_main
from ..utils.print import *

def main(config: dict):
	print()
	start_time: float = time.perf_counter()

	# Generate datapack loading
	loading_main(config)

	# Generate basic datapack structure (tick, tick_2, second, second_5, minute)
	basic_structure_main(config)

	# Generate custom recipes
	recipes_main(config)

	# Custom Blocks (place + destroy)
	custom_blocks_main(config)

	# Generate items loot tables
	loot_tables_main(config)

	# Info print
	total_time: float = time.perf_counter() - start_time
	info(f"Datapack successfully generated in {total_time:.5f} seconds!")

