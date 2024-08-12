
# Imports
from .io import *
from .print import *
from .cache import simple_cache
from ..constants import *

# Recipes constants
FURNACES_RECIPES_TYPES = ("smelting", "blasting", "smoking", "campfire_cooking")
CRAFTING_RECIPES_TYPES = ("crafting_shaped", "crafting_shapeless")

# Function mainly used for database generation
@simple_cache
def ingr_repr(id: str, ns: str|None = None, count: int|None = None) -> dict:
	""" Get the identity of the ingredient from its id for custom crafts
	Args:
		id		(str):		The id of the ingredient, ex: adamantium_fragment
		ns		(str|None):	The namespace of the ingredient (optional if 'id' argument is a vanilla item), ex: iyc
		count	(int|None):	The count of the ingredient (optional)
	Returns:
		str: The identity of the ingredient for custom crafts,
			ex: {"components":{"minecraft:custom_data":{"iyc":{"adamantium_fragment":True}}}}
			ex: {"item": "minecraft:stick"}
	"""
	if ":" in id:
		to_return = {"item": id}
	else:
		if ns is None:
			error(f"Namespace must be specified for custom ingredient '{id}', or you may be missing 'minecraft:'")
		to_return = {"components":{"minecraft:custom_data":{ns:{id:True}}}}
	if count is not None:
		to_return["count"] = count
	return to_return

@simple_cache
def item_to_id_ingr_repr(ingr: dict) -> dict:
	""" Replace the "item" key by "id" in an item ingredient representation
	Args:
		ingr (dict): The item ingredient, ex: {"item": "minecraft:stick"}
	Returns:
		dict: The item ingredient representation, ex: {"id": "minecraft:stick"}
	"""
	if ingr.get("item") is None:
		return ingr
	if "Slot" in ingr:
		r = {"Slot": ingr["Slot"], "id": ingr["item"]}
	else:
		r = {"id": ingr["item"]}
	copy = ingr.copy()
	copy.pop("item")
	r.update(copy)
	return r

# Mainly used for manual
@simple_cache
def ingr_to_id(ingredient: dict, add_namespace: bool = True) -> str:
	""" Get the id from an ingredient dict
	Args:
		ingredient (dict): The ingredient dict
			ex: {"components":{"minecraft:custom_data":{iyc:{adamantium_ingot:True}}}}
			ex: {"item": "minecraft:stick"}
	Returns:
		str: The id of the ingredient, ex: "minecraft:stick" or "iyc:adamantium_ingot"
	"""
	if ingredient.get("item"):
		if not add_namespace:
			return ingredient["item"].split(":")[1]
		return ingredient["item"]
	else:
		custom_data: dict = ingredient["components"]["minecraft:custom_data"]
		namespace: str = ""
		id: str = ""
		for cd_ns, cd_data in custom_data.items():
			if isinstance(cd_data, dict):
				values: list = list(cd_data.values())
				if isinstance(values[0], bool):
					namespace = cd_ns
					id = list(cd_data.keys())[0]
					break
		if not namespace:
			error(f"No namespace found in custom data: {custom_data}")
		if add_namespace:
			return namespace + ":" + id
		return id

# Mainly used for recipes
@simple_cache
def get_vanilla_item_id_from_ingredient(config: dict, ingredient: dict, add_namespace: bool = True) -> str:
	""" Get the id of the vanilla item from an ingredient dict
	Args:
		config (dict): The config dict
		ingredient (dict): The ingredient dict
			ex: {"item": "minecraft:stick"}
		add_namespace (bool): Whether to add the namespace to the id
	Returns:
		str: The id of the vanilla item, ex: "minecraft:stick"
	"""
	ns, ingr_id = ingr_to_id(ingredient).split(":")
	if ns == config['namespace']:
		if add_namespace:
			return config['database'][ingr_id]["id"]
		return config['database'][ingr_id]["id"].split(":")[1]
	elif ns == "minecraft":
		if add_namespace:
			return f"{ns}:{ingr_id}"
		return ingr_id
	else:
		if config['external_database'].get(f"{ns}:{ingr_id}"):
			if add_namespace:
				return config['external_database'][f"{ns}:{ingr_id}"]["id"]
			return config['external_database'][f"{ns}:{ingr_id}"]["id"].split(":")[1]
		else:
			error(f"External item '{ns}:{ingr_id}' not found in the external database")

# Used for recipes
@simple_cache
def get_item_from_ingredient(config: dict, ingredient: dict) -> dict:
	""" Get the item dict from an ingredient dict
	Args:
		config (dict): The config dict
		ingredient (dict): The ingredient dict
			ex: {"item": "minecraft:stick"}
	Returns:
		dict: The item data dict, ex: {"id": "minecraft:stick", "count": 1}
	"""
	ingr_id = ingr_to_id(ingredient)
	ns, id = ingr_id.split(":")

	# Get from internal database
	if ns == config['namespace']:
		item_data: dict = config['database'][id].copy()
		result: dict = {"id": item_data.pop("id"), "count": 1}

		# Add components
		for k, v in item_data.items():
			if k not in NOT_COMPONENTS:
				if result.get("components") is None:
					result["components"] = {}
				result["components"][f"minecraft:{k}"] = v
		return result
	
	# External database
	if config['external_database'].get(ingr_id):
		item_data: dict = config['external_database'][ingr_id].copy()
		result: dict = {"id": item_data.pop("id"), "count": 1}

		# Add components
		for k, v in item_data.items():
			if k not in NOT_COMPONENTS:
				if result.get("components") is None:
					result["components"] = {}
				result["components"][f"minecraft:{k}"] = v
		return result
	
	# Minecraft item
	if ns == "minecraft":
		return {"id": id, "count": 1}
	error(f"External item '{ingr_id}' not found in the external database")

# Make a loot table
@simple_cache
def loot_table_from_ingredient(config: dict, result_ingredient: dict, result_count: int) -> str:

	# If item from this datapack
	item: str = ingr_to_id(result_ingredient)
	if item.startswith(config['namespace']):
		item = item.split(":")[1]
		loot_table = f"{config['namespace']}:i/{item}"
		if result_count > 1:
			loot_table += f"_x{result_count}"
		return loot_table
	
	namespace, item = item.split(":")
	loot_table = f"{config['namespace']}:recipes/{namespace}/{item}"
	if result_count > 1:
		loot_table += f"_x{result_count}"

	# If item from another datapack, generate the loot table
	path: str = f"{config['build_datapack']}/data/{config['namespace']}/loot_table/recipes/{namespace}/{item}.json"
	if namespace != "minecraft":
		file: dict = {"pools":[{"rolls":1,"entries":[{"type":"minecraft:loot_table","value": f"{config['namespace']}:external/{namespace}/{item}"}] }] }
	else:
		file: dict = {"pools":[{"rolls":1,"entries":[{"type":"minecraft:item","name":f"{namespace}:{item}"}] }] }
	if result_count > 1:
		file["pools"][0]["entries"][0]["functions"] = [{"function": "minecraft:set_count","count": result_count}]
	write_to_file(path, super_json_dump(file, max_level = 9))
	return loot_table

@simple_cache
def get_ingredients_from_recipe(recipe: dict) -> list[str]:
	""" Get the ingredients from a recipe dict
	Args:
		recipe (dict): The final recipe JSON dict, ex:\n
		{
			"type": "minecraft:crafting_shaped",
			"pattern": [...],
			"key": {...},
			"result": {...}
		}
	Returns:
		list[str]: The ingredients ids
	"""
	ingredients: list[str] = []
	if recipe.get("key"):
		for value in recipe["key"].values():
			ingredients.append(value["item"])
	elif recipe.get("ingredients"):
		for ingr in recipe["ingredients"]:
			ingredients.append(ingr["item"])
	elif recipe.get("ingredient"):
		ingredients.append(recipe["ingredient"]["item"])
	elif recipe.get("template"):
		ingredients.append(recipe["template"]["item"])
	return ingredients


