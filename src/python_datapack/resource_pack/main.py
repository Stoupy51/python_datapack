
# Imports
from .sounds import main as sounds_main
from .item_models import main as item_models_main
from .vanilla_models import main as vanilla_models_main
from .power_of_2 import main as check_all_textures_power_of_2
from ..utils.io import *

def main(config: dict):
	print()

	# Add the sounds folder to the resource pack
	sounds_main(config)

	# For each item, copy textures and make models
	item_models_main(config)

	# For each vanilla ID, create the json model file
	vanilla_models_main(config)

	# Check all textures if they are in power of 2 resolution
	check_all_textures_power_of_2(config)

	# Write resource pack files to write
	write_all_files(contains = config['build_resource_pack'])

