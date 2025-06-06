
# Imports
import os

import stouputils as stp

from .constants import (
	CATEGORY,
	CUSTOM_BLOCK_ALTERNATIVE,
	CUSTOM_BLOCK_VANILLA,
	NO_SILK_TOUCH_DROP,
	RESULT_OF_CRAFTING,
	USED_FOR_CRAFTING,
	VANILLA_BLOCK,
	VANILLA_BLOCK_FOR_ORES,
)
from .utils.ingredients import FURNACES_RECIPES_TYPES


def main(config: dict):
	database: dict[str, dict] = config['database']

	# Remove empty lists of recipes
	for data in database.values():
		if data.get(RESULT_OF_CRAFTING) == []:
			data.pop(RESULT_OF_CRAFTING)
		if data.get(USED_FOR_CRAFTING) == []:
			data.pop(USED_FOR_CRAFTING)

	# Create a copy of the database without OVERRIDE_MODEL key
	database_copy: dict[str, dict] = {}
	for item, data in database.items():
		database_copy[item] = data.copy()
		if "override_model" in database_copy[item]:
			del database_copy[item]["override_model"]

	# Export database to JSON for debugging generation
	database_debug: str = config["database_debug"]
	with stp.super_open(database_debug, "w") as f:
		stp.super_json_dump(database_copy, file = f)

	rel_debug: str = stp.clean_path(os.path.relpath(database_debug, os.getcwd()))
	stp.debug(f"Received database exported to './{rel_debug}'")

	# Check every single thing in the database
	errors: list[str] = []
	for item, data in database.items():

		# Check if the item uses a reserved name
		if item == "heavy_workbench":
			errors.append(f"'{item}' is reserved for the heavy workbench used for NBT recipes, please use another name")

		# Check for a proper ID
		if not data.get("id"):
			errors.append(f"'id' key missing for '{item}'")
		else:
			if not isinstance(data["id"], str):
				errors.append(f"'id' key should be a string for '{item}'")
			elif ":" not in data["id"]:
				errors.append(f"'id' key should be namespaced in the format 'minecraft:{data['id']}' for '{item}'")
			elif data["id"] == "minecraft:deepslate":
				errors.append(f"'id' key should not be 'minecraft:deepslate' for '{item}', it's a reserved ID")

			# Force VANILLA_BLOCK key for custom blocks
			elif data["id"] in [CUSTOM_BLOCK_VANILLA, CUSTOM_BLOCK_ALTERNATIVE]:
				if not data.get(VANILLA_BLOCK):
					errors.append(f"VANILLA_BLOCK key missing for '{item}', needed format: VANILLA_BLOCK: {{\"id\":\"minecraft:stone\", \"apply_facing\":False}}.")
				elif not isinstance(data[VANILLA_BLOCK], dict):
					errors.append(f"VANILLA_BLOCK key should be a dictionary for '{item}', found '{data[VANILLA_BLOCK]}', needed format: VANILLA_BLOCK: {{\"id\":\"minecraft:stone\", \"apply_facing\":False}}.")
				elif data[VANILLA_BLOCK].get("id", None) is None:
					errors.append(f"VANILLA_BLOCK key should have an 'id' key for '{item}', found '{data[VANILLA_BLOCK]}', needed format: VANILLA_BLOCK: {{\"id\":\"minecraft:stone\", \"apply_facing\":False}}.")
				elif data[VANILLA_BLOCK].get("apply_facing", None) is None:
					errors.append(f"VANILLA_BLOCK key should have a 'apply_facing' key to boolean for '{item}', found '{data[VANILLA_BLOCK]}', needed format: VANILLA_BLOCK: {{\"id\":\"minecraft:stone\", \"apply_facing\":False}}.")

			# Prevent the use of "container" key for custom blocks
			elif data["id"] == CUSTOM_BLOCK_VANILLA and data.get("container"):
				errors.append(f"'container' key should not be used for '{item}', it's a reserved key for custom blocks, prefer writing to the place function to fill in the container")

		# If a category is present but wrong format, log an error
		if data.get(CATEGORY) and not isinstance(data[CATEGORY], str):
			errors.append(f"CATEGORY key should be a string for '{item}'")

		# Check for a proper custom data
		if data.get("custom_data") and not isinstance(data["custom_data"], dict):
			errors.append(f"'custom_data' key should be a dictionary for '{item}'")
		elif not data.get("custom_data") or not data["custom_data"].get(config['namespace']) or not isinstance(data["custom_data"][config['namespace']], dict) or not data["custom_data"][config['namespace']].get(item) or not isinstance(data["custom_data"][config['namespace']][item], bool):
			errors.append(f"'custom_data' key missing proper data for '{item}', should have at least \"custom_data\": {{config['namespace']: {{\"{item}\": True}}}}")

		# Check for wrong custom ores data
		if data.get(VANILLA_BLOCK) == VANILLA_BLOCK_FOR_ORES and not data.get(NO_SILK_TOUCH_DROP):
			errors.append(f"NO_SILK_TOUCH_DROP key missing for '{item}', should be the ID of the block that drops when mined without silk touch")
		if data.get(VANILLA_BLOCK) != VANILLA_BLOCK_FOR_ORES and data.get(NO_SILK_TOUCH_DROP):
			errors.append(f"NO_SILK_TOUCH_DROP key should not be used for '{item}' if it doesn't use VANILLA_BLOCK_FOR_ORES")
		if data.get(NO_SILK_TOUCH_DROP) and not isinstance(data[NO_SILK_TOUCH_DROP], str):
			errors.append(f"NO_SILK_TOUCH_DROP key should be a string for '{item}', ex: \"adamantium_fragment\" or \"minecraft:stone\"")

		# Force the use of "item_name" key for every item
		if not data.get("item_name"):
			errors.append(f"'item_name' key missing for '{item}', should be a dict or a list (SNBT), ex: {{\"text\":\"This is an Item Name\"}} or [\"This is an Item Name\"]")
		elif not isinstance(data["item_name"], dict | list | str):
			errors.append(f"'item_name' key should be a dict or a list (SNBT) for '{item}'")

		# Force the use of "lore" key to be in a correct format
		if data.get("lore"):
			if not isinstance(data["lore"], list):
				errors.append(f"'lore' key should be a list for '{item}'")
			else:
				for i, line in enumerate(data["lore"]):
					if not isinstance(line, dict | list | str):
						errors.append(f"Line #{i} in 'lore' key should be a dict or a list (SNBT) for '{item}', ex: {{\"text\":\"This is a lore line\"}} or [\"This is a lore line\"]")
					else:
						# Verify format {"text":"..."} or "..."
						line = str(line)
						if not (line.startswith('{') and line.endswith('}')) \
							and not (line.startswith('[') and line.endswith(']')) \
							and not (line.startswith('"') and line.endswith('"')) \
							and not (line.startswith("'") and line.endswith("'")) \
							and not line == "":
							errors.append(f"Item '{item}' has a lore line that is not in a correct text component format: {line}\n We recommend using 'https://misode.github.io/text-component/' to generate the text component")

		# Check all the recipes
		if data.get(RESULT_OF_CRAFTING) or data.get(USED_FOR_CRAFTING):

			# Get a list of recipes
			crafts_to_check: list[dict] = list(data.get(RESULT_OF_CRAFTING, []))
			crafts_to_check += list(data.get(USED_FOR_CRAFTING,[]))

			# Check each recipe
			for i, recipe in enumerate(crafts_to_check):

				# A recipe is always a dictionnary
				if not isinstance(recipe, dict):
					errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should be a dictionary for '{item}'")
				else:

					# Verify "type" key
					if not recipe.get("type") or not isinstance(recipe["type"], str):
						errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have a string 'type' key for '{item}'")
					else:

						# Check the crafting_shaped type
						if recipe["type"] == "crafting_shaped":
							if not recipe.get("shape") or not isinstance(recipe["shape"], list):
								errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have a list[str] 'shape' key for '{item}'")
							elif len(recipe["shape"]) > 3 or len(recipe["shape"][0]) > 3:
								errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have a maximum of 3 rows and 3 columns for '{item}'")
							else:
								row_size = len(recipe["shape"][0])
								if any(len(row) != row_size for row in recipe["shape"]):
									errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have the same number of columns for each row for '{item}'")

							if not recipe.get("ingredients") or not isinstance(recipe["ingredients"], dict):
								errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have a dict 'ingredients' key for '{item}'")
							else:
								for symbol, ingredient in recipe["ingredients"].items():
									if not isinstance(ingredient, dict):
										errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have a dict ingredient for symbol '{symbol}' for '{item}'")
									elif not ingredient.get("item") and not ingredient.get("components"):
										errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have an 'item' or 'components' key for ingredient of symbol '{symbol}' for '{item}', please use 'ingr_repr' function")
									elif ingredient.get("components") and not isinstance(ingredient["components"], dict):
										errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have a dict 'components' key for ingredient of symbol '{symbol}' for '{item}', please use 'ingr_repr' function")
									if not any(symbol in line for line in recipe["shape"]):
										errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have a symbol '{symbol}' in the shape for '{item}'")

						# Check the crafting_shapeless type
						elif recipe["type"] == "crafting_shapeless":
							if not recipe.get("ingredients") or not isinstance(recipe["ingredients"], list):
								errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have a list 'ingredients' key for '{item}'")
							else:
								for ingredient in recipe["ingredients"]:
									if not isinstance(ingredient, dict):
										errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have a dict ingredient for '{item}'")
									elif not ingredient.get("item") and not ingredient.get("components"):
										errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have an 'item' or 'components' key for ingredient for '{item}', please use 'ingr_repr' function")
									elif ingredient.get("components") and not isinstance(ingredient["components"], dict):
										errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have a dict 'components' key for ingredient for '{item}', please use 'ingr_repr' function")

						# Check the furnaces recipes
						elif recipe["type"] in FURNACES_RECIPES_TYPES:
							if not recipe.get("ingredient") or not isinstance(recipe["ingredient"], dict):
								errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have a dict 'ingredient' key for '{item}'")
							elif not recipe["ingredient"].get("item") and not recipe["ingredient"].get("components"):
								errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have an 'item' or 'components' key for ingredient for '{item}', please use 'ingr_repr' function")
							elif recipe["ingredient"].get("components") and not isinstance(recipe["ingredient"]["components"], dict):
								errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have a dict 'components' key for ingredient for '{item}', please use 'ingr_repr' function")

							if not recipe.get("experience") or not isinstance(recipe["experience"], float | int):
								errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have a float 'experience' key for '{item}'")
							if not recipe.get("cookingtime") or not isinstance(recipe["cookingtime"], int):
								errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have an int 'cookingtime' key for '{item}'")

					# Check the result count
					if not recipe.get("result_count") or not isinstance(recipe["result_count"], int):
						errors.append(f"Recipe #{i} in RESULT_OF_CRAFTING should have an int 'result_count' key for '{item}'")

	# Log errors if any
	if errors:
		stp.error("Errors found in the database during verification:\n" + "\n".join(errors))
	else:
		stp.info("No errors found in the database during verification")


	# Add additional data to the custom blocks
	for item, data in database.items():
		if data.get("id") == CUSTOM_BLOCK_VANILLA:
			data["container"] = [{"slot": 0, "item": {"id": "minecraft:stone", "count": 1,"components": {"minecraft:custom_data": {"smithed": {"block": {"id": f"{config['namespace']}:{item}", "from": config['namespace']}}}}}}]

			# Hide the container tooltip
			if not data.get("tooltip_display"):
				data["tooltip_display"] = {"hidden_components": []}
			elif not data["tooltip_display"].get("hidden_components"):
				data["tooltip_display"]["hidden_components"] = []
			data["tooltip_display"]["hidden_components"].append("minecraft:container")
	pass

