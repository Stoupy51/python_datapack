
# Imports
from __future__ import annotations
from enum import Enum
from PIL import Image
from mutagen.oggvorbis import OggVorbis

# Import utils
from ..constants import *
from .ingredients import *
from .print import *
from .io import *

# Constants
SLOTS = {"helmet": "head", "chestplate": "chest", "leggings": "legs", "boots": "feet", "sword": "mainhand", "pickaxe": "mainhand", "axe": "mainhand", "shovel": "mainhand", "hoe": "mainhand"}
UNIQUE_SLOTS_VALUES = []
for slot in SLOTS.values():
	if slot not in UNIQUE_SLOTS_VALUES:
		UNIQUE_SLOTS_VALUES.append(slot)

class DEFAULT_ORE(Enum):
	NETHERITE = "netherite"
	DIAMOND = "diamond"
	IRON = "iron"
	GOLD = "golden"
	CHAINMAIL = "stone"		# stone tools
	LEATHER = "wooden"		# wood tools

class VanillaEquipments(Enum):
	""" Default vanilla equipments values (durability, armor, armor_toughness, knockback_resistance, attack_damage, attack_speed) """
	HELMET			= {	DEFAULT_ORE.LEATHER:	{"durability": 55,		"generic.armor": 1},
						DEFAULT_ORE.CHAINMAIL:	{"durability": 165,		"generic.armor": 2},
						DEFAULT_ORE.IRON:		{"durability": 165,		"generic.armor": 2},
						DEFAULT_ORE.GOLD:		{"durability": 77,		"generic.armor": 2},
						DEFAULT_ORE.DIAMOND:	{"durability": 363,		"generic.armor": 3,	"generic.armor_toughness": 2},
			 			DEFAULT_ORE.NETHERITE:	{"durability": 407,		"generic.armor": 3,	"generic.armor_toughness": 3,	"generic.knockback_resistance": 0.1}
					}
	CHESTPLATE		= {	DEFAULT_ORE.LEATHER:	{"durability": 80,		"generic.armor": 3},
						DEFAULT_ORE.CHAINMAIL:	{"durability": 240,		"generic.armor": 5},
						DEFAULT_ORE.IRON:		{"durability": 240,		"generic.armor": 6},
						DEFAULT_ORE.GOLD:		{"durability": 112,		"generic.armor": 5},
						DEFAULT_ORE.DIAMOND: 	{"durability": 528,		"generic.armor": 8,	"generic.armor_toughness": 2},
						DEFAULT_ORE.NETHERITE:	{"durability": 592,		"generic.armor": 8,	"generic.armor_toughness": 3,	"generic.knockback_resistance": 0.1}
					}
	LEGGINGS		= {	DEFAULT_ORE.LEATHER:	{"durability": 75,		"generic.armor": 2},
  						DEFAULT_ORE.CHAINMAIL:	{"durability": 225,		"generic.armor": 4},
						DEFAULT_ORE.IRON:		{"durability": 225,		"generic.armor": 5},
						DEFAULT_ORE.GOLD:		{"durability": 105,		"generic.armor": 3},
						DEFAULT_ORE.DIAMOND:	{"durability": 495,		"generic.armor": 6,	"generic.armor_toughness": 2},
						DEFAULT_ORE.NETHERITE:	{"durability": 555,		"generic.armor": 6,	"generic.armor_toughness": 3,	"generic.knockback_resistance": 0.1}
					}
	BOOTS			= {	DEFAULT_ORE.LEATHER:	{"durability": 65,		"generic.armor": 1},
						DEFAULT_ORE.CHAINMAIL:	{"durability": 195,		"generic.armor": 1},
						DEFAULT_ORE.IRON:		{"durability": 195,		"generic.armor": 2},
						DEFAULT_ORE.GOLD:		{"durability": 95,		"generic.armor": 1},
						DEFAULT_ORE.DIAMOND:	{"durability": 429,		"generic.armor": 3,	"generic.armor_toughness": 2},
						DEFAULT_ORE.NETHERITE:	{"durability": 481,		"generic.armor": 3,	"generic.armor_toughness": 3,	"generic.knockback_resistance": 0.1}
					}
	SWORD			= {	DEFAULT_ORE.LEATHER:	{"durability": 59,		"generic.attack_damage": 4,		"generic.attack_speed": -2.50},
						DEFAULT_ORE.CHAINMAIL:	{"durability": 131,		"generic.attack_damage": 5,		"generic.attack_speed": -2.50},
						DEFAULT_ORE.IRON:		{"durability": 250,		"generic.attack_damage": 6,		"generic.attack_speed": -2.50},
						DEFAULT_ORE.GOLD:		{"durability": 32,		"generic.attack_damage": 4,		"generic.attack_speed": -2.50},
						DEFAULT_ORE.DIAMOND:	{"durability": 1561,	"generic.attack_damage": 7,		"generic.attack_speed": -2.50},
						DEFAULT_ORE.NETHERITE:	{"durability": 2031,	"generic.attack_damage": 8,		"generic.attack_speed": -2.50}
					}
	PICKAXE			= {	DEFAULT_ORE.LEATHER:	{"durability": 59,		"generic.attack_damage": 2,		"generic.attack_speed": -2.75},
						DEFAULT_ORE.CHAINMAIL:	{"durability": 131,		"generic.attack_damage": 3,		"generic.attack_speed": -2.75},
						DEFAULT_ORE.IRON:		{"durability": 250,		"generic.attack_damage": 4,		"generic.attack_speed": -2.75},
						DEFAULT_ORE.GOLD:		{"durability": 32,		"generic.attack_damage": 2,		"generic.attack_speed": -2.75},
						DEFAULT_ORE.DIAMOND:	{"durability": 1561,	"generic.attack_damage": 5,		"generic.attack_speed": -2.75},
						DEFAULT_ORE.NETHERITE:	{"durability": 2031,	"generic.attack_damage": 6,		"generic.attack_speed": -2.75}
					}
	AXE				= {	DEFAULT_ORE.LEATHER:	{"durability": 59,		"generic.attack_damage": 7,		"generic.attack_speed": -3.20},
						DEFAULT_ORE.CHAINMAIL:	{"durability": 131,		"generic.attack_damage": 9,		"generic.attack_speed": -3.20},
						DEFAULT_ORE.IRON:		{"durability": 250,		"generic.attack_damage": 9,		"generic.attack_speed": -3.10},
						DEFAULT_ORE.GOLD:		{"durability": 32,		"generic.attack_damage": 7,		"generic.attack_speed": -3.00},
						DEFAULT_ORE.DIAMOND:	{"durability": 1561,	"generic.attack_damage": 9,		"generic.attack_speed": -3.00},
						DEFAULT_ORE.NETHERITE:	{"durability": 2031,	"generic.attack_damage": 10,	"generic.attack_speed": -3.00}
					}
	SHOVEL			= {	DEFAULT_ORE.LEATHER:	{"durability": 59,		"generic.attack_damage": 2.5,	"generic.attack_speed": -3.20},
						DEFAULT_ORE.CHAINMAIL:	{"durability": 131,		"generic.attack_damage": 3.5,	"generic.attack_speed": -3.20},
						DEFAULT_ORE.IRON:		{"durability": 250,		"generic.attack_damage": 4.5,	"generic.attack_speed": -3.10},
						DEFAULT_ORE.GOLD:		{"durability": 32,		"generic.attack_damage": 2.5,	"generic.attack_speed": -3.00},
						DEFAULT_ORE.DIAMOND:	{"durability": 1561,	"generic.attack_damage": 5.5,	"generic.attack_speed": -3.00},
			 			DEFAULT_ORE.NETHERITE:	{"durability": 2031,	"generic.attack_damage": 6.5,	"generic.attack_speed": -3.00}
					}
	HOE				= {	DEFAULT_ORE.LEATHER:	{"durability": 59,		"generic.attack_damage": 1,		"generic.attack_speed": -3.00},
						DEFAULT_ORE.CHAINMAIL:	{"durability": 131,		"generic.attack_damage": 1,		"generic.attack_speed": -2.00},
						DEFAULT_ORE.IRON:		{"durability": 250,		"generic.attack_damage": 1,		"generic.attack_speed": -1.00},
						DEFAULT_ORE.GOLD:		{"durability": 32,		"generic.attack_damage": 1,		"generic.attack_speed": -3.00},
						DEFAULT_ORE.DIAMOND:	{"durability": 1561,	"generic.attack_damage": 1,		"generic.attack_speed": 0},
						DEFAULT_ORE.NETHERITE:	{"durability": 2031,	"generic.attack_damage": 1,		"generic.attack_speed": 0}
					}

class EquipmentsConfig():
	def __init__(self, equivalent_to: DEFAULT_ORE = DEFAULT_ORE.DIAMOND, pickaxe_durability: int = 1561, attributes: dict[str, float] = {}):
		""" Creates a configuration for equipments (based on the pickaxe)
		Args:
			equivalent_to (DEFAULT_ORE):	The equivalent ore to compare to (ex: DEFAULT_ORE.DIAMOND)
			pickaxe_durability (int):		The pickaxe durability that will be used to calculate the durability of other equipments
			attributes (dict[str, float]):	(optional) Attributes with type "add_value" to add (not override) to the equipment (ex: "generic.attack_damage": 1.0, means 6 attack damage for diamond pickaxe)
				{"generic.attack_damage": 1.0, "generic.armor": 1.0, "player.mining_efficiency": 0.1}
				generic.attack_damage and player.mining_efficiency are always on tools
				generic.armor and generic.armor_toughness is always on armor
		If you need a specific attribute for a generated item, you should append it afterward.
		"""
		self.equivalent_to = equivalent_to
		self.pickaxe_durability = pickaxe_durability
		self.attributes = attributes
	def getter(self) -> tuple[DEFAULT_ORE, int, dict[str, float]]:
		return self.equivalent_to, self.pickaxe_durability, self.attributes
	def get_tools_attributes(self) -> dict[str, float]:
		NOT_ON_TOOLS = ["generic.armor", "generic.armor_toughness"]
		return {key: value for key, value in self.attributes.items() if key not in NOT_ON_TOOLS}
	def get_armor_attributes(self) -> dict[str, float]:
		NOT_ON_ARMOR = ["generic.attack_damage", "player.mining_efficiency"]
		return {key: value for key, value in self.attributes.items() if key not in NOT_ON_ARMOR}

# UUIDs utils
def format_attributes(config: dict, attributes: str, slot: str, attr_config: dict = {}) -> list[dict]:
	""" Returns generated attribute_modifiers key for an item (adds up attributes and config) """
	# Get attributes from config
	attribute_modifiers = []
	for attribute_name, value in attr_config.items():
		if attribute_name != "durability":
			attribute_modifiers.append({"type": attribute_name, "amount": value, "operation": "add_value", "slot": slot, "id": f"{config['namespace']}:{attribute_name}.{slot}"})

	# For each attribute, add it to the list if not in, else add the value
	for attribute_name, value in attributes.items():
		found = False
		for attribute in attribute_modifiers:
			if attribute["type"] == attribute_name:
				attribute["amount"] += value
				found = True
				break
		if not found:
			attribute_modifiers.append({"type": attribute_name, "amount": value, "operation": "add_value", "slot": slot, "id": f"{config['namespace']}:{attribute_name}.{slot}"})

	# Return the list of attributes
	return attribute_modifiers

# Generate everything related to the ore
def generate_everything_about_this_material(config: dict, database: dict[str, dict], material: str = "adamantium_fragment", equipments_config: EquipmentsConfig|None = EquipmentsConfig(DEFAULT_ORE.NETHERITE, 1873, {"attack_damage": 1.2, "player.mining_efficiency": 0.2})) -> list[str]:
	""" Generate everything related to the ore (armor, tools, weapons, ore, and ingredients (raw, nuggets, blocks)).
		The function will try to find textures in the assets folder to each item
		And return a list of generated items if you want to do something with it.
	Args:
		database			(dict[str, dict]):		The database to update
		material			(str):					The ore/material to generate everything about (ex: "adamantium_fragment", "steel_ingot", "minecraft:emerald", "minecraft:copper_ingot")
		equipments_config	(EquipmentsConfig):	The base multiplier to apply
	Returns:
		list[str]:		The list of generated items (ex: ["adamantium_helmet", "raw_adamantium", "adamantium_block", ...])
	"""
	# Constants
	if '_' in material:
		material_base = "_".join(material.split(":")[-1].split("_")[:-1])			# Get the base material name (ex: "adamantium" from "adamantium_fragment")
	else:
		material_base = material.split(":")[-1]										# Get the base material name (ex: "adamantium" from "adamantium_fragment")
	main_ingredient = ingr_repr(material, config['namespace']) 						# Get the main ingredient for recipes
	if equipments_config:
		equivalent_to = equipments_config.equivalent_to
		durability_factor = equipments_config.pickaxe_durability / VanillaEquipments.PICKAXE.value[equivalent_to]["durability"]
		armor_attributes = equipments_config.get_armor_attributes()
		tools_attributes = equipments_config.get_tools_attributes()

	# Get ore color (for armor dye and other stuff)
	color = None
	if f"{material_base}_chestplate.png" in config['textures_files']:
		color = Image.open(f"{config['textures_folder']}/{material_base}_chestplate.png")
		color = list(color.getdata())										# Get image (1D Array)
		color = [(r,g,b) for (r,g,b,a) in color if a > 0]					# Get all colors that are not transparent
		color = [sum(x) / len(color) for x in zip(*color)]					# Get the average color
		color = int(color[0]) << 16 | int(color[1]) << 8 | int(color[2])	# Convert to int (Minecraft format: Red<<16 + Green<<8 + Blue)

	# Placeables (ore, deepslate_ore, block, raw_block)
	for block in [f"{material_base}_block", f"{material_base}_ore", f"deepslate_{material_base}_ore", f"raw_{material_base}_block"]:
		if block + ".png" not in config['textures_files']:
			continue
		if block not in database:
			database[block] = {}
		database[block]["id"] = CUSTOM_BLOCK_VANILLA		# Item for placing custom block
		database[block][CATEGORY] = "material"				# Category
		database[block]["custom_data"] = {"smithed":{}}		# Smithed convention
		database[block]["custom_data"]["smithed"]["dict"] = {"block": {material_base: True}}
		if block.endswith("ore"):
			database[block]["custom_data"]["smithed"]["dict"]["ore"] = {material_base: True}
		if block.endswith("block"):
			if block.startswith("raw") and f"raw_{material_base}.png" in config['textures_files']:
				database[block][RESULT_OF_CRAFTING] = [{"type":"crafting_shaped","result_count":1,"group":material_base,"category":"misc","shape":["XXX","XXX","XXX"],"ingredients":{"X":ingr_repr(f"raw_{material_base}", config['namespace'])}}]
			else:
				database[block][RESULT_OF_CRAFTING] = [{"type":"crafting_shaped","result_count":1,"group":material_base,"category":"misc","shape":["XXX","XXX","XXX"],"ingredients":{"X":main_ingredient}}]
		pass

	## Ingredients (ingot, nugget, raw, and other)
	for item in [material_base, f"{material_base}_ingot", f"{material_base}_nugget", f"raw_{material_base}", f"{material_base}_fragment", f"{material_base}_dust", f"{material_base}_stick", f"{material_base}_rod"]:
		if item + ".png" not in config['textures_files']:
			continue
		if item not in database:
			database[item] = {}
		item_type = item.replace(f"{material_base}_", "").replace(f"_{material_base}", "")
		database[item]["id"] = CUSTOM_ITEM_VANILLA		# Custom item
		database[item][CATEGORY] = "material"			# Category
		database[item]["custom_data"] = {"smithed":{}}	# Smithed convention
		database[item]["custom_data"]["smithed"]["dict"] = {item_type: {material_base: True}}

		# Recipes
		database[item][RESULT_OF_CRAFTING] = database[item].get(RESULT_OF_CRAFTING, [])
		database[item][USED_FOR_CRAFTING] = database[item].get(USED_FOR_CRAFTING, [])
		if item.endswith("ingot") or item.endswith("fragment") or item == material_base:
			if f"{material_base}_block.png" in config['textures_files']:
				database[item][RESULT_OF_CRAFTING].append({"type":"crafting_shapeless","result_count":9,"category":"misc","group":material_base,"ingredients":[ingr_repr(f"{material_base}_block", config['namespace'])]})
			if f"{material_base}_nugget.png" in config['textures_files']:
				database[item][RESULT_OF_CRAFTING].append({"type":"crafting_shaped","result_count":1,"category":"misc","group":material_base,"shape":["XXX","XXX","XXX"],"ingredients":{"X":ingr_repr(f"{material_base}_nugget", config['namespace'])}})
			if f"raw_{material_base}.png" in config['textures_files']:
				database[item][RESULT_OF_CRAFTING].append({"type":"smelting","result_count":1,"category":"misc","group":material_base,"experience":0.8,"cookingtime":200,"ingredient":ingr_repr(f"raw_{material_base}", config['namespace'])})
				database[item][RESULT_OF_CRAFTING].append({"type":"blasting","result_count":1,"category":"misc","group":material_base,"experience":0.8,"cookingtime":100,"ingredient":ingr_repr(f"raw_{material_base}", config['namespace'])})
			if f"{material_base}_dust.png" in config['textures_files']:
				database[item][RESULT_OF_CRAFTING].append({"type":"smelting","result_count":1,"category":"misc","group":material_base,"experience":0.8,"cookingtime":200,"ingredient":ingr_repr(f"{material_base}_dust", config['namespace'])})
				database[item][RESULT_OF_CRAFTING].append({"type":"blasting","result_count":1,"category":"misc","group":material_base,"experience":0.8,"cookingtime":100,"ingredient":ingr_repr(f"{material_base}_dust", config['namespace'])})
			if f"{material_base}_ore.png" in config['textures_files']:
				database[item][RESULT_OF_CRAFTING].append({"type":"smelting","result_count":1,"category":"misc","group":material_base,"experience":0.8,"cookingtime":200,"ingredient":ingr_repr(f"{material_base}_ore", config['namespace'])})
				database[item][RESULT_OF_CRAFTING].append({"type":"blasting","result_count":1,"category":"misc","group":material_base,"experience":0.8,"cookingtime":100,"ingredient":ingr_repr(f"{material_base}_ore", config['namespace'])})
			if f"deepslate_{material_base}_ore.png" in config['textures_files']:
				database[item][RESULT_OF_CRAFTING].append({"type":"smelting","result_count":1,"category":"misc","group":material_base,"experience":0.8,"cookingtime":200,"ingredient":ingr_repr(f"deepslate_{material_base}_ore", config['namespace'])})
				database[item][RESULT_OF_CRAFTING].append({"type":"blasting","result_count":1,"category":"misc","group":material_base,"experience":0.8,"cookingtime":100,"ingredient":ingr_repr(f"deepslate_{material_base}_ore", config['namespace'])})
		if item.endswith("dust"):
			database[item][USED_FOR_CRAFTING].append({"type":"smelting","result_count":1,"category":"misc","group":material_base,"experience":0.8,"cookingtime":200,"ingredient":ingr_repr(item, config['namespace']),"result":main_ingredient})
			database[item][USED_FOR_CRAFTING].append({"type":"blasting","result_count":1,"category":"misc","group":material_base,"experience":0.8,"cookingtime":100,"ingredient":ingr_repr(item, config['namespace']),"result":main_ingredient})
			database[item][RESULT_OF_CRAFTING].append({"type":PULVERIZING,"result_count":1,"category":"misc","group":material_base,"ingredient":main_ingredient})
			for pulv_ingr in [f"raw_{material_base}",f"{material_base}_ore",f"deepslate_{material_base}_ore"]:
				if f"{pulv_ingr}.png" in config['textures_files']:
					database[item][RESULT_OF_CRAFTING].append({"type":PULVERIZING,"result_count":2,"category":"misc","group":material_base,"ingredient":ingr_repr(pulv_ingr, config['namespace'])})
		if item.endswith("nugget"):
			for gear in SLOTS.keys():
				if f"{material_base}_{gear}.png" in config['textures_files']:
					database[item][RESULT_OF_CRAFTING].append({"type":"smelting","result_count":1,"category":"equipment","experience":0.8,"cookingtime":200,"ingredient":ingr_repr(f"{material_base}_{gear}", config['namespace'])})
		if item.endswith("stick"):
			database[item][RESULT_OF_CRAFTING].append({"type":"crafting_shaped","result_count":4,"category":"misc","shape":["X","X"],"ingredients":{"X":main_ingredient}})
		if item.endswith("rod"):
			database[item][RESULT_OF_CRAFTING].append({"type":"crafting_shaped","result_count":1,"category":"misc","shape":["X","X","X"],"ingredients":{"X":main_ingredient}})
		pass

	# Armor (helmet, chestplate, leggings, boots)
	for gear in ["helmet", "chestplate", "leggings", "boots"]:
		armor = material_base + "_" + gear
		if armor + ".png" not in config['textures_files']:
			continue
		if armor not in database:
			database[armor] = {}
		database[armor]["id"] = f"minecraft:leather_{gear}"		# Leather armor to dye
		database[armor][CATEGORY] = "equipment"					# Category
		database[armor]["custom_data"] = {"smithed":{}}			# Smithed convention
		database[armor]["custom_data"]["smithed"]["dict"] = {"armor": {material_base: True, gear: True}}
		database[armor]["dyed_color"] = {"rgb": color, "show_in_tooltip": False}	# Apply dye to leather armor
		gear_config = {}
		if gear == "helmet":
			database[armor][RESULT_OF_CRAFTING] = [{"type":"crafting_shaped","result_count":1,"category":"equipment","shape":["XXX","X X"],"ingredients":{"X": main_ingredient}}]
			gear_config = VanillaEquipments.HELMET.value[equivalent_to]
			database[armor]["max_damage"] = int(gear_config["durability"] * durability_factor)
		elif gear == "chestplate":
			database[armor][RESULT_OF_CRAFTING] = [{"type":"crafting_shaped","result_count":1,"category":"equipment","shape":["X X","XXX","XXX"],"ingredients":{"X": main_ingredient}}]
			gear_config = VanillaEquipments.CHESTPLATE.value[equivalent_to]
			database[armor]["max_damage"] = int(gear_config["durability"] * durability_factor)
		elif gear == "leggings":
			database[armor][RESULT_OF_CRAFTING] = [{"type":"crafting_shaped","result_count":1,"category":"equipment","shape":["XXX","X X","X X"],"ingredients":{"X": main_ingredient}}]
			gear_config = VanillaEquipments.LEGGINGS.value[equivalent_to]
			database[armor]["max_damage"] = int(gear_config["durability"] * durability_factor)
		elif gear == "boots":
			database[armor][RESULT_OF_CRAFTING] = [{"type":"crafting_shaped","result_count":1,"category":"equipment","shape":["X X","X X"],"ingredients":{"X": main_ingredient}}]
			gear_config = VanillaEquipments.BOOTS.value[equivalent_to]
			database[armor]["max_damage"] = int(gear_config["durability"] * durability_factor)
		database[armor]["attribute_modifiers"] = format_attributes(config, armor_attributes, SLOTS[gear], gear_config)
	
	# Tools (sword, pickaxe, axe, shovel, hoe)
	for gear in ["sword", "pickaxe", "axe", "shovel", "hoe"]:
		tool = material_base + "_" + gear
		if tool + ".png" not in config['textures_files']:
			continue
		if tool not in database:
			database[tool] = {}
		database[tool]["id"] = f"minecraft:{equivalent_to.value}_{gear}"		# Vanilla tool, ex: iron_sword, wooden_hoe
		database[tool][CATEGORY] = "equipment"
		database[tool]["custom_data"] = {"smithed":{}}
		database[tool]["custom_data"]["smithed"]["dict"] = {"tools": {material_base: True, gear: True}}
		tools_ingr = {"X": main_ingredient, "S": ingr_repr("minecraft:stick")}
		gear_config = {}
		if gear == "sword":
			gear_config = VanillaEquipments.SWORD.value[equivalent_to]
			database[tool]["max_damage"] = int(gear_config["durability"] * durability_factor)
			database[tool][RESULT_OF_CRAFTING] = [{"type":"crafting_shaped","result_count":1,"category":"equipment","shape":["X","X","S"],"ingredients": tools_ingr}]
		elif gear == "pickaxe":
			gear_config = VanillaEquipments.PICKAXE.value[equivalent_to]
			database[tool]["max_damage"] = int(gear_config["durability"] * durability_factor)
			database[tool][RESULT_OF_CRAFTING] = [{"type":"crafting_shaped","result_count":1,"category":"equipment","shape":["XXX"," S "," S "],"ingredients": tools_ingr}]
		elif gear == "axe":
			gear_config = VanillaEquipments.AXE.value[equivalent_to]
			database[tool]["max_damage"] = int(gear_config["durability"] * durability_factor)
			database[tool][RESULT_OF_CRAFTING] = [{"type":"crafting_shaped","result_count":1,"category":"equipment","shape":["XX","XS"," S"],"ingredients": tools_ingr}]
		elif gear == "shovel":
			gear_config = VanillaEquipments.SHOVEL.value[equivalent_to]
			database[tool]["max_damage"] = int(gear_config["durability"] * durability_factor)
			database[tool][RESULT_OF_CRAFTING] = [{"type":"crafting_shaped","result_count":1,"category":"equipment","shape":["X","S","S"],"ingredients": tools_ingr}]
		elif gear == "hoe":
			gear_config = VanillaEquipments.HOE.value[equivalent_to]
			database[tool]["max_damage"] = int(gear_config["durability"] * durability_factor)
			database[tool][RESULT_OF_CRAFTING] = [{"type":"crafting_shaped","result_count":1,"category":"equipment","shape":["XX"," S"," S"],"ingredients": tools_ingr}]
		database[tool]["attribute_modifiers"] = format_attributes(config, tools_attributes, SLOTS[gear], gear_config)
	pass

# Generate everything about these ores
def generate_everything_about_these_materials(config: dict, database: dict[str, dict], ores: dict[str, EquipmentsConfig|None]) -> dict[str, list[str]]:
	""" Uses function 'generate_everything_about_this_material' for each ore in the ores dictionary.
	Args:
		config		(dict):				The configuration to use.
		database	(dict[str, dict]):	The database to apply the ores to.
		ores		(dict[str, EquipmentsConfig|None]):	The ores to apply.
	Returns:
		dict[str, list[str]]:	The list of generated items for each ore.
	"""
	generated_items = {}
	for material, ore_config in ores.items():
		generated_items[material] = generate_everything_about_this_material(config, database, material, ore_config)
	return generated_items

# Add recipes for dust
def add_recipes_for_dust(config: dict, database: dict[str, dict], material: str, pulverize: list[str|dict], smelt_to: dict) -> None:
	""" Add recipes for dust (pulverize and smelt). If dust isn't found in the database, it will be added automagically.\n
	All items in the pulverize list will be pulverized to get 2 times the dust.\n
	If the item is a string, their ingr_repr will be used as "minecraft:{item}"\n
	Args:
		config		(dict):				The configuration to use.
		database	(dict[str, dict]):	The database to add the dust recipes to.
		material	(str):				The material to add dust recipes for, ex: "copper" will add recipes for "copper_dust".
		pulverize	(list[str|dict]):	The list of items to pulverize to get 2 times the dust, ex: ["raw_copper", "copper_ore", "deepslate_copper_ore", ingr_repr("custom_copper", "some_namespace")]
		smelt_to	(dict):				The ingredient representation of the result of smelting the dust, ex: ingr_repr("minecraft:copper_ingot")}
	"""
	dust = material + "_dust"
	if f"{dust}.png" not in config['textures_files']:
		error(f"Error during dust recipe generation: texture '{dust}.png' not found (required for '{material}' dust)")
		return
	
	# Add dust to the database if not found
	if dust not in database:
		database[dust] = {"id": CUSTOM_ITEM_VANILLA, CATEGORY: "material"}
	
	# Add smelting and blasting recipes
	ingredient: dict = ingr_repr(dust, config['namespace'])
	database[dust][USED_FOR_CRAFTING] = database[dust].get(USED_FOR_CRAFTING, [])
	database[dust][USED_FOR_CRAFTING].append({"type":"smelting","result_count":1,"category":"misc","group":material,"experience":0.8,"cookingtime":200,"ingredient":ingredient, "result":smelt_to})
	database[dust][USED_FOR_CRAFTING].append({"type":"blasting","result_count":1,"category":"misc","group":material,"experience":0.8,"cookingtime":100,"ingredient":ingredient, "result":smelt_to})

	# Add reverse recipe
	database[dust][RESULT_OF_CRAFTING] = database[dust].get(RESULT_OF_CRAFTING, [])
	database[dust][RESULT_OF_CRAFTING].append({"type":PULVERIZING,"result_count":1,"category":"misc","group":material,"ingredient":smelt_to})

	# Add pulverizing recipes
	for item in pulverize:
		pulv_ingr = item if isinstance(item, dict) else ingr_repr(f"minecraft:{item}")
		database[dust][RESULT_OF_CRAFTING].append({"type":PULVERIZING,"result_count":2,"category":"misc","group":material,"ingredient":pulv_ingr})
	return

# Add recipes for all dusts
def add_recipes_for_all_dusts(config: dict, database: dict[str, dict], dusts_configs: dict[str, tuple[list[str|dict],dict]]) -> None:
	""" Add recipes for all dusts in the dusts_configs dictionary using the add_recipes_for_dust function.\n
	Args:
		config			(dict):										The configuration to use.\n
		database		(dict[str, dict]):							The database to add the dust recipes to.\n
		dusts_configs	(dict[str, tuple[list[str|dict],dict]]):	The dusts to add recipes for, ex:\n
		{
			"copper": (
				["raw_copper", "copper_ore", "deepslate_copper_ore", ingr_repr("custom_copper", "some_namespace")],
				ingr_repr("minecraft:copper_ingot")
			)
		}
	"""
	for dust, (pulverize, smelt_to) in dusts_configs.items():
		add_recipes_for_dust(config, database, dust, pulverize, smelt_to)
	return

# Clean record name
A_Z = "abcdefghijklmnopqrstuvwxyz"
ZERO_NINE = "0123456789"
UNDERSCORE = "_"
def clean_record_name(name: str) -> str:
	name = name.replace(".ogg","").lower()
	to_replace = [" ", "-", "___"]
	for r in to_replace:
		name = name.replace(r, "_")
	return "".join([c for c in name if c in A_Z + ZERO_NINE + UNDERSCORE])
			
# Custom records
def generate_custom_records(config: dict, database: dict[str, dict], records: dict[str, str]|str|None, category: str|None = None) -> None:
	""" Generate custom records by searching in config['assets_folder']/records/ for the files and copying them to the database and resource pack folder.
	Args:
		database	(dict[str, dict]):	The database to add the custom records items to, ex: {"record_1": "song.ogg", "record_2": "another_song.ogg"}
		records		(dict[str, str]):	The custom records to apply, ex: {"record_1": "My first Record.ogg", "record_2": "A second one.ogg"}
		category	(str):				The category to apply to the custom records (ex: "music").
	"""
	# Check records format,
	if records and not (isinstance(records, dict) or records in ["auto", "all"]):
		error(f"Error during custom record generation: records must be a dictionary, 'auto', or 'all' (got {type(records).__name__})")

	# If no records specified, search in the records folder
	if not records or records in ["auto", "all"]:
		
		songs: list[str] = [x for x in os.listdir(config["assets_folder"] + "/records") if x.endswith((".ogg",".wav"))]
		records = { clean_record_name(file): file for file in songs }
		debug(f"No records specified, searching in '{config['assets_folder']}/records' folder. Found {len(records)} records.")

	# For each record, add it to the database
	for record, sound in records.items():
		if not isinstance(sound, str):
			error(f"Error during custom record generation: sound '{sound}' is not a string, got {type(sound).__name__}")
		if not sound.endswith(".ogg"):
			warning(f"Error during custom record generation: sound '{sound}' is not an ogg file")
			continue
		item_name = ".".join(sound.split(".")[:-1])	# Remove the file extension
		database[record] = {
			"id": CUSTOM_ITEM_VANILLA,
			"custom_data": {config['namespace']:{record: True}, "smithed":{"dict":{"record": {record: True}}}},
			"item_name": "{'text':'Music Disc', 'italic': false}",
			"jukebox_playable": {"song": f"{config['namespace']}:{record}", "show_in_tooltip": True},
			"max_stack_size": 1,
			"rarity": "rare",
		}
		if category:
			database[record][CATEGORY] = category
		
		# Get song duration
		file_path = f"{config['assets_folder']}/records/{sound}"
		if os.path.exists(file_path):
			duration: int = round(OggVorbis(file_path).info.length)
			
			# Set jukebox song
			json_song = {"comparator_output": duration % 16, "length_in_seconds": duration + 1, "sound_event": {"sound_id":f"{config['namespace']}:{record}"}, "description": {"text": item_name}}
			write_to_file(f"{config['build_datapack']}/data/{config['namespace']}/jukebox_song/{record}.json", super_json_dump(json_song))

			# Copy sound to resource pack
			super_copy(file_path, f"{config['build_resource_pack']}/assets/{config['namespace']}/sounds/{record}.ogg")

			json_sound = {"category": "music", "sounds": [{"name": f"{config['namespace']}:{record}","stream": True}]}
			json_sound = {record: json_sound}
			write_to_file(f"{config['build_resource_pack']}/assets/{config['namespace']}/sounds.json", super_json_dump(json_sound))
		else:
			warning(f"Error during custom record generation: path '{file_path}' does not exist")




# Deterministic custom model data
def deterministic_custom_model_data(config: dict, database: dict[str, dict], starting_cmd: int, black_list: list[str] = []) -> None:
	""" Apply custom model data to all items using a cache method.
	Args:
		database		(dict[str, dict]):	The database to apply custom model data to.
		starting_cmd	(int):				The starting custom model data.
		blacklist		(list[str]):		The list of items to ignore.
	"""
	# Load cached custom model data
	cached_custom_model_data = {}
	if os.path.exists(config['cmd_cache']):
		with open(config['cmd_cache'], "r") as f:
			cached_custom_model_data = json.load(f)
	
	# For each item in the database, apply its cached custom model data if it exists
	for item, data in database.items():
		if item in cached_custom_model_data:
			data["custom_model_data"] = cached_custom_model_data[item]

	# Get maximum custom model data
	max_cmd: int = starting_cmd - 1
	for item, data in database.items():
		if data.get("custom_model_data") and isinstance(data["custom_model_data"], int):
			cmd: int = int(data["custom_model_data"])

			# Add two custom model data if the item has an on/off texture
			if any(item in texture and "_on" in texture for texture in config['textures_files']):
				cmd += 1

			# If it is a cake, add 6 custom model data for each slice
			elif item.endswith("cake") and all(f"{item}_{face}.png" in config['textures_files'] for face in ["top","bottom","side","inner"]):
				cmd += 7

			# Increment the maximum custom model data
			max_cmd = max(max_cmd, cmd)
	
	# For each item in the database, apply its new custom model data if it doesn't exist
	for item, data in database.items():
		if item not in black_list and (not data.get("custom_model_data") or not isinstance(data["custom_model_data"], int)):
			data["custom_model_data"] = max_cmd + 1

			# Add two custom model data if the item has an on/off texture
			if any(item in texture and "_on" in texture for texture in config['textures_files']):
				max_cmd += 2
			
			# If it is a cake, add 6 custom model data for each slice
			elif item.endswith("cake") and all(f"{item}_{face}.png" in config['textures_files'] for face in ["top","bottom","side","inner"]):
				max_cmd += 7
			
			# Else, add one custom model data
			else:
				max_cmd += 1
	
	# Update cache
	for item, data in database.items():
		if data.get("custom_model_data"):
			cached_custom_model_data[item] = data["custom_model_data"]
	with open(config['cmd_cache'], "w") as f:
		super_json_dump(cached_custom_model_data, f)
	return

# Add item name and lore
def add_item_name_and_lore_if_missing(config: dict, database: dict[str, dict], is_external: bool = False) -> None:
	""" Add item name and lore to all items in the database if they are missing.
	Args:
		config		(dict):				The configuration to get the source lore from.
		database	(dict[str, dict]):	The database to add item name and lore to.
		is_external	(bool):				Whether the database is the external one or not (meaning the namespace is in the item name).
	"""
	lore = json.dumps(config['source_lore']) if len(config['source_lore']) > 1 else json.dumps(config['source_lore'][0])
	lore = lore.replace('"', "'")
	for item, data in database.items():

		# Add item name if none
		if not data.get("item_name"):
			if not is_external:
				item_str = item.replace("_"," ").title()
			else:
				item_str = item.split(":")[-1].replace("_"," ").title()
			data["item_name"] = json.dumps( {"text": item_str, "italic": False, "color":"white"} ).replace("'", "\\'").replace('"', "'")

		# Apply namespaced lore if none
		if not data.get("lore"):
			data["lore"] = []
		if not is_external:
			if not data["lore"] or data["lore"][-1] != lore:
				data["lore"].append(lore)
		else:
			ns = item.split(":")[0].replace("_"," ").title()
			ns_lore  = json.dumps(config['source_lore']).replace('"', "'").replace(config['datapack_name'], ns)
			if not data["lore"] or data["lore"][-1] != ns_lore:
				data["lore"].append(ns_lore)
	return

# Add private custom data for namespace ( namespace:{item:true} )
def add_private_custom_data_for_namespace(config: dict, database: dict[str, dict], is_external: bool = False) -> None:
	""" Add private custom data for namespace to all items in the database if they are missing.
	Args:
		config		(dict):				The configuration to get the namespace from.
		database	(dict[str, dict]):	The database to add private custom data for namespace to.
		is_external	(bool):				Whether the database is the external one or not (meaning the namespace is in the item name).
	"""
	for item, data in database.items():
		if not data.get("custom_data"):
			data["custom_data"] = {}
		if not is_external:
			data["custom_data"][config['namespace']] = {item: True}
		else:
			ns, id = item.split(":")
			data["custom_data"][ns] = {id: True}
	return

# Smithed ignore convention
def add_smithed_ignore_vanilla_behaviours_convention(database: dict[str, dict]) -> None:
	""" Add smithed convention to all items in the database if they are missing.
		Refer to https://wiki.smithed.dev/conventions/tag-specification/#custom-items for more information.
	Args:
		database	(dict[str, dict]):	The database to add smithed convention to.
	"""
	for data in database.values():
		if not data.get("custom_data"):
			data["custom_data"] = {}
		if not data["custom_data"].get("smithed"):
			data["custom_data"]["smithed"] = {}
		if not data["custom_data"]["smithed"].get("ignore"):
			data["custom_data"]["smithed"]["ignore"] = {}
		if not data["custom_data"]["smithed"]["ignore"].get("functionality"):
			data["custom_data"]["smithed"]["ignore"]["functionality"] = True
		if not data["custom_data"]["smithed"]["ignore"].get("crafting"):
			data["custom_data"]["smithed"]["ignore"]["crafting"] = True
	return

class CustomOreGeneration():
	def __init__(self, dimensions: list[str], maximum_height: int = 70, minimum_height: int|None = None, veins_per_region: int = 4, vein_size_logic: float = 0.4, provider: str|list[str] = "#minecraft:overworld_carver_replaceables", placer_command: str = "") -> None:
		""" Creates a custom ore generation configuration.\n
		Args:
			dimensions (list[str]):			The dimensions to generate the ore in (ex: ["minecraft:overworld"])
			maximum_height (int):			The maximum height the ore can generate at
			minimum_height (int|None):		The minimum height the ore can generate at (default: None for bedrock to maximum_height)
			veins_per_region (int):			The number of veins per region
			vein_size_logic (float):		The logic to calculate the vein size, higher = more ores
			provider (str|list[str]):		The block or block tag to check for the ore to generate (default is same as vanilla ores in overworld), can be either a string or a list of strings
			placer_command (str):			The placer command to use for the ore generation, usually a function to place the custom ore but can be anything, default is autogenerated
		"""
		self.dimensions: list[str] = dimensions
		self.maximum_height: int = maximum_height
		self.minimum_height: int|None = minimum_height
		self.veins_per_region: int = veins_per_region
		self.vein_size_logic: float = vein_size_logic
		self.provider: str|list[str] = provider
		self.placer_command: str = placer_command
		if not official_lib_used("smart_ore_generation"):
			debug("Found custom ore generation, adding 'smart_ore_generation' dependency")
		self.check_validity()
	
	def check_validity(self) -> list[str]:
		""" Check if the custom ore generation configuration is valid """
		if not isinstance(self.dimensions, list) or not all(isinstance(dimension, str) for dimension in self.dimensions):
			error("Custom ore generation 'dimensions' must be a list of strings")
		if not isinstance(self.maximum_height, int):
			error("Custom ore generation 'maximum_height' must be an integer")
		if self.minimum_height is not None and not isinstance(self.minimum_height, int):
			error("Custom ore generation 'minimum_height' must be an integer or None")
		elif self.minimum_height is not None and self.minimum_height > self.maximum_height:
			error("Custom ore generation 'minimum_height' must be less or equal to 'maximum_height'")
		if not isinstance(self.veins_per_region, int):
			error("Custom ore generation 'veins_per_region' must be an integer")
		if not isinstance(self.vein_size_logic, float) or self.vein_size_logic < 0:
			error("Custom ore generation 'vein_size_logic' must be a float >= 0")
		if not isinstance(self.provider, str) and not isinstance(self.provider, list):
			error("Custom ore generation 'provider' must be a string or a list of strings")
		if isinstance(self.provider, list) and not all(isinstance(provider, str) for provider in self.provider):
			error("Custom ore generation 'provider' must be a list of strings")
		if not isinstance(self.placer_command, str):
			error("Custom ore generation 'placer_command' must be a string")
	
	def generate_files(self, config: dict, custom_ore: str, number: int|None = None):
		""" Generate the files for the custom ore generation\n
		Args:
			config (dict):			The configuration dictionary
			custom_ore (str):		The custom ore to generate, ex: "adamantium_ore"
			number (int|None):		(optional) The number of the custom ore to generate, ex: 1 for "adamantium_ore_1", used when having multiple configurations for the same ore
		"""
		namespace: str = config['namespace']
		database: dict[str, dict] = config['database']
		lib_folder: str = f"{config['build_datapack']}/data/{config['namespace']}/function/calls/smart_ore_generation"
		beautify_ore: str = custom_ore.replace("_", " ").title()

		# Setup placer command if not done yet
		if not self.placer_command:
			self.placer_command = f"run function {namespace}:custom_blocks/{custom_ore}/place_main"

			# If the custom ore is a deepslate ore and normal ore exists, cancel the command if the block is not stone
			if custom_ore.startswith("deepslate_") and custom_ore.replace("deepslate_", "") in database:
				self.placer_command = "unless block ~ ~ ~ minecraft:stone " + self.placer_command

			# If the custom ore is a normal ore and deepslate ore exists, cancel the command if the block is not deepslate
			elif f"deepslate_{custom_ore}" in database:
				self.placer_command = "unless block ~ ~ ~ minecraft:deepslate " + self.placer_command
		
		# Add ore to generate ores function
		path: str = f"{lib_folder}/generate_ores.mcfunction"
		dimensions_check: str = ""
		for index, dimension in enumerate(self.dimensions):
			dimensions_check += f"\nexecute if dimension {dimension} run scoreboard players set #dimension smart_ore_generation.data {index}"
		if self.minimum_height == None:
			op_mini: str = f"scoreboard players operation #min_height smart_ore_generation.data = _OVERWORLD_BOTTOM smart_ore_generation.data"
		else:
			op_mini: str = f"scoreboard players set #min_height smart_ore_generation.data {self.minimum_height}"
		content: str = f"""
# Generate {beautify_ore} (x{self.veins_per_region})
scoreboard players set #dimension smart_ore_generation.data -1{dimensions_check}
{op_mini}
scoreboard players set #max_height smart_ore_generation.data {self.maximum_height}
"""
		place_vein: str = f"execute if score #dimension smart_ore_generation.data matches 0.. run function {config['namespace']}:calls/smart_ore_generation/veins/{custom_ore}\n"
		content += self.veins_per_region * place_vein
		write_to_file(path, content)

		# Add ore to veins folder
		path: str = f"{lib_folder}/veins/{custom_ore}.mcfunction"
		content: str = f"""
# Try to find a random position adjacent to air in the region to generate the ore
function #smart_ore_generation:v1/slots/random_position

# Placing {beautify_ore} patch
execute at @s if block ~ ~ ~ {self.provider} {self.placer_command}
"""
		if self.vein_size_logic > 0:
			radius: float = self.vein_size_logic % 1
			while radius <= self.vein_size_logic:
				
				# Make a sphere of radius
				for x in range(-1, 2):
					for y in range(-1, 2):
						for z in range(-1, 2):
							content += f"execute at @s positioned ~{x*radius} ~{y*radius} ~{z*radius} if block ~ ~ ~ {self.provider} {self.placer_command}\n"
				
				# Increase radius
				radius += 1
		
		# Write file
		write_to_file(path, content)

	@staticmethod
	def all_with_config(config: dict, ore_configs: dict[str, list[CustomOreGeneration]]) -> None:
		""" Generate all custom ore generation files with the configurations provided\n
		Args:
			config (dict):										The configuration dictionary\n
			ore_configs (dict[str, list[CustomOreGeneration]]):	The custom ore generation configurations, ex:\n
				{
					"super_iron_ore": [
						CustomOreGeneration(
							dimensions = ["minecraft:overworld","stardust:cavern","some_other:dimension"],
							maximum_height = 50,
							minimum_height = 0,
							veins_per_region = 2,
							vein_size_logic = 0.4,
						)
					],
					"deepslate_super_iron_ore": [
						CustomOreGeneration(
							dimensions = ["minecraft:overworld"],
							maximum_height = 0,
							veins_per_region = 2,
							vein_size_logic = 0.4,
						),
						CustomOreGeneration(
							dimensions = ["stardust:cavern"],
							maximum_height = 0,
							veins_per_region = 8,
							vein_size_logic = 0.8,
						)
					], ...
				}
		"""
		for ore, config_list in ore_configs.items():
			for i, gen_config in enumerate(config_list):
				if len(config_list) > 1:
					gen_config.generate_files(config, ore, i)
				else:
					gen_config.generate_files(config, ore)
		return


