
# Technical constants
FACES: tuple = ("down", "up", "north", "south", "west", "east")						# Faces of a block, used for resource pack and blocks orientation
SIDES: tuple = ("_bottom", "_top", "_front", "_back", "_left", "_right", "_side")	# Sides of a block, used for resource pack
CUSTOM_BLOCK_VANILLA: str = "minecraft:furnace"			# Vanilla block used as base for custom blocks, must have the "facing" blockstate
CUSTOM_BLOCK_ALTERNATIVE: str = "minecraft:item_frame"	# Same purpose as previous, but useful for blocks that can be placed on walls or on player's position (ex: flowers)
CUSTOM_ITEM_VANILLA: str = "minecraft:command_block"	# Vanilla item used as base for custom items, must not have any survival vanilla behaviour
MODEL_DISPLAY: dict = {"head":{"rotation":[0,0,0],"translation":[0,-30.42,0],"scale":[1.605,1.605,1.605]},"fixed":{"rotation":[-90,0,0],"translation":[0,0,-16],"scale":[2.0075,2.0075,2.0075]}}	# Model display base for custom blocks
DOWNLOAD_VANILLA_ASSETS_RAW = "https://raw.githubusercontent.com/edayot/renders/renders/resourcepack/assets/minecraft/textures/render"
DOWNLOAD_VANILLA_ASSETS_SOURCE = "https://github.com/edayot/renders/tree/renders/resourcepack/assets/minecraft/textures/render"


# Databases
RESULT_OF_CRAFTING: str = "result_of_crafting"			# Key to a list of recipes to craft the item, ex: "adamantium": {RESULT_OF_CRAFTING: [...]}
USED_FOR_CRAFTING: str = "used_for_crafting"			# Should not be used unless you are crafting a vanilla item (ex: iyc.chainmail -> chainmail armor)
CATEGORY: str = "category"								# Key for the category, used for recipes and the manual, ex: CATEGORY:"material" or CATEGORY:"equipment"
COMMANDS_ON_PLACEMENT: str = "commands_on_placement"	# Key to a list of commands to execute when a custom block is placed, should be a list of strings or a single string (with break lines if multiple commands)
COMMANDS_ON_BREAK: str = "commands_on_break"			# Key to a list of commands to execute when a custom block is broken, should be a list of strings or a single string (with break lines if multiple commands)
VANILLA_BLOCK: str = "vanilla_block"					# Key to a vanilla block that will be placed for custom block interaction, value can either a string of a dict {"id":"minecraft:chest", "block_states": ["facing", "type=single", "waterlogged=false"]}
VANILLA_BLOCK_FOR_ORES: str = "minecraft:polished_deepslate"	# Vanilla block that will be used for an optimization tip for ores, don't ask questions
NO_SILK_TOUCH_DROP: str = "no_silk_touch_drop"			# Key to an item ID that will drop when silk touch is not used. Must be used only when using the vanilla block for ores, ex: "adamantium_fragment" or "minecraft:raw_iron"
NOT_COMPONENTS: list[str] = [							# Keys that should not be considered as components. Used for recipes, loot tables, etc.
	"id",
	"wiki",
	CATEGORY,
	RESULT_OF_CRAFTING,
	USED_FOR_CRAFTING,
	VANILLA_BLOCK,
	NO_SILK_TOUCH_DROP,
	COMMANDS_ON_PLACEMENT,
	COMMANDS_ON_BREAK
]

