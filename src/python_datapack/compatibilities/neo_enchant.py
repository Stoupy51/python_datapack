
# Imports
from ..utils.print import *
from ..utils.io import *
from ..constants import *

# Main function
def main(config: dict):
	database: dict[str, dict] = config["database"]

	# If any block use the vanilla block for ores, add the compatibility
	if any(VANILLA_BLOCK_FOR_ORES == data.get(VANILLA_BLOCK) for data in database.values()):

		# Add the block to veinminer tag
		write_to_file(f"{config['build_datapack']}/data/enchantplus/tags/block/veinminer.json", super_json_dump({"values": [VANILLA_BLOCK_FOR_ORES["id"]]}))

		# Final print
		debug("Special datapack compatibility done for NeoEnchant's veinminer!")

