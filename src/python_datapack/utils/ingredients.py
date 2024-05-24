
# Imports
from .print import *
from .cache import simple_cache

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
			ex: {"components":{"custom_data":{"iyc":{"adamantium_fragment":True}}}}
			ex: {"item": "minecraft:stick"}
	"""
	if ":" in id:
		to_return = {"item": id}
	else:
		if ns is None:
			error(f"Namespace must be specified for custom ingredient '{id}'")
		to_return = {"components":{"custom_data":{ns:{id:True}}}}
	if count is not None:
		to_return["count"] = count
	return to_return

# Mainly used for manual
@simple_cache
def ingr_to_id(ingredient: dict, add_namespace: bool = True) -> str:
	""" Get the id from an ingredient dict
	Args:
		ingredient (dict): The ingredient dict
			ex: {"components":{"custom_data":{iyc:{adamantium_ingot=True}}}}
			ex: {"item": "minecraft:stick"}
	Returns:
		str: The id of the ingredient, ex: "minecraft:stick" or "iyc:adamantium_ingot"
	"""
	if ingredient.get("item"):
		if not add_namespace:
			return ingredient["item"].split(":")[1]
		return ingredient["item"]
	else:
		custom_data = ingredient["components"]["custom_data"]
		namespace = list(custom_data.keys())[0]
		id = list(custom_data[namespace].keys())[0]
		if add_namespace:
			return namespace + ":" + id
		return id

