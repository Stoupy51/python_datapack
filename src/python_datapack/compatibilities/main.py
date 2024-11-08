
# Imports
from .simpledrawer import main as simpledrawer
from .neo_enchant import main as neo_enchant

def main(config: dict):

	# Compatibility with SimpleDrawer's compacting drawer
	simpledrawer(config)

	# Compatibility with NeoEnchant's veinminer
	neo_enchant(config)

