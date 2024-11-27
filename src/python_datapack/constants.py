
# Minecraft version constants
DATAPACK_FORMAT: int = 57			# Pack format version, see https://minecraft.wiki/w/Pack_format#List_of_data_pack_formats
RESOURCE_PACK_FORMAT: int = 42		# Resource pack format version, see https://minecraft.wiki/w/Pack_format#List_of_resource_pack_formats
MINECRAFT_VERSION: str = "1.21.3"	# Text used when loading the datapack to warn the user when the data version is not right
DATA_VERSION: int = 4082			# Depending on MC version, given by /data get entity @p DataVersion to check if the datapack is not running in an older version of MC


# Databases
CATEGORY: str = "category"								# Key for the category, used for recipes and the manual, ex: CATEGORY:"material" or CATEGORY:"equipment"
CUSTOM_BLOCK_VANILLA: str = "minecraft:furnace"			# Vanilla block used as base for custom blocks, must have the "facing" blockstate
CUSTOM_BLOCK_ALTERNATIVE: str = "minecraft:item_frame"	# Same purpose as previous, but useful for blocks that can be placed on walls or on player's position (ex: flowers)
CUSTOM_BLOCK_HEAD: str = "minecraft:player_head"		# Same purpose as previous, but useful for blocks does not have a custom model data
CUSTOM_ITEM_VANILLA: str = "minecraft:command_block"	# Vanilla item used as base for custom items, must not have any survival vanilla behaviour
VANILLA_BLOCK: str = "vanilla_block"					# Key to a vanilla block that will be placed for custom block interaction, value needs to be a dict like {"id":"minecraft:chest[type=single,waterlogged=false]", "apply_facing": True}
NO_SILK_TOUCH_DROP: str = "no_silk_touch_drop"			# Key to an item ID that will drop when silk touch is not used. Must be used only when using the vanilla block for ores, ex: "adamantium_fragment" or "minecraft:raw_iron"
VANILLA_BLOCK_FOR_ORES: dict = {"id":"minecraft:polished_deepslate", "apply_facing": False}	# Vanilla block that will be used for an optimization tip for ores, don't ask questions
OVERRIDE_MODEL: str = "override_model"					# Key to a dictionnary that will be used to override the whole model
PULVERIZING: str = "simplenergy_pulverizing"			# Value of a recipe type, used to generate dusts from ores (used by SimplEnergy)
SMITHED_CRAFTER_COMMAND: str = "smithed_crafter_command"	# Key to a command that will be used in a recipe in the Smithed Crafter library. If not present, the command will be defaulted to a loot table. Ex: {"result":...,SMITHED_CRAFTER_COMMAND: "function your_namespace:calls/smithed_crafter/do_something_else"}
WIKI_COMPONENT: str = "wiki_components"				# Key to a text component that will be used to generate the wiki button in the manual
RESULT_OF_CRAFTING: str = "result_of_crafting"			# Key to a list of recipes to craft the item, ex: "adamantium": {RESULT_OF_CRAFTING: [...]}
USED_FOR_CRAFTING: str = "used_for_crafting"			# Should not be used unless you are crafting a vanilla item (ex: iyc.chainmail -> chainmail armor)
NOT_COMPONENTS: list[str] = [							# Keys that should not be considered as components. Used for recipes, loot tables, etc.
	"id",
	WIKI_COMPONENT,
	RESULT_OF_CRAFTING,
	USED_FOR_CRAFTING,
	CATEGORY,
	VANILLA_BLOCK,
	NO_SILK_TOUCH_DROP,
	OVERRIDE_MODEL,
	SMITHED_CRAFTER_COMMAND,
]

# Technical constants
FACES: tuple = ("down", "up", "north", "south", "west", "east")						# Faces of a block, used for resource pack and blocks orientation
SIDES: tuple = ("_bottom", "_top", "_front", "_back", "_left", "_right", "_side")	# Sides of a block, used for resource pack
DOWNLOAD_VANILLA_ASSETS_RAW = "https://raw.githubusercontent.com/edayot/renders/89324614d1be45957936f454b5290910635b0944/resourcepack/assets/minecraft/textures/render"
DOWNLOAD_VANILLA_ASSETS_SOURCE = "https://github.com/edayot/renders/tree/89324614d1be45957936f454b5290910635b0944/resourcepack/assets/minecraft/textures/render"
CUSTOM_BLOCK_HEAD_CUBE_RADIUS: tuple[int, int, int] = (16, 16, 16)	# Size of the region to check around the player when placing a CUSTOM_BLOCK_HEAD
BLOCKS_WITH_INTERFACES: list[str] = [	# List of blocks that are containers and have an interface
	"minecraft:barrel",
	"minecraft:chest",
	"minecraft:furnace",
	"minecraft:shulker_box",
	"minecraft:dispenser",
	"minecraft:hopper",
	"minecraft:dropper",
	"minecraft:smoker",
	"minecraft:blast_furnace",
	"minecraft:brewing_stand",
	"minecraft:trapped_chest",
	"minecraft:crafter",
]

# Automatically handled dependencies for supported libs with additional key "is_used" that is True when the lib is found to be used.
def official_lib_used(lib: str) -> bool:
	is_used: bool = OFFICIAL_LIBS[lib]["is_used"]
	OFFICIAL_LIBS[lib]["is_used"] = True
	return is_used

OFFICIAL_LIBS: dict[str, dict] = {
	"common_signals":		{"version":[0, 1, 0], "name":"Common Signals",					"url":"https://github.com/Stoupy51/CommonSignals",			"is_used": False},
	"smithed.custom_block":	{"version":[0, 5, 0], "name":"Smithed Custom Block",			"url":"https://wiki.smithed.dev/libraries/custom-block/",	"is_used": False},
	"smithed.crafter":		{"version":[0, 5, 0], "name":"Smithed Crafter",					"url":"https://wiki.smithed.dev/libraries/crafter/",		"is_used": False},
	"furnace_nbt_recipes":	{"version":[1, 8, 0], "name":"Furnace NBT Recipes",				"url":"https://github.com/Stoupy51/FurnaceNbtRecipes",		"is_used": False},
	"smart_ore_generation":	{"version":[1, 7, 1], "name":"SmartOreGeneration",				"url":"https://github.com/Stoupy51/SmartOreGeneration",		"is_used": False},
	"itemio":				{"version":[1, 3, 1], "name":"ItemIO",							"url":"https://github.com/edayot/ItemIO",					"is_used": False},
}

