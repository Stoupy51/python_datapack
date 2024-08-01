
# Imports
from ..utils.io import *
from ..utils.print import *
from ..utils.ingredients import *
from ..utils.cache import simple_cache
from ..constants import *

# Generate recipes
def main(config: dict):
	namespace: str = config['namespace']
	build_datapack: str = config['build_datapack']
	SMITHED_SHAPELESS_PATH: str = f"{build_datapack}/data/{namespace}/function/calls/smithed_crafter/shapeless_recipes.mcfunction"
	SMITHED_SHAPED_PATH: str = f"{build_datapack}/data/{namespace}/function/calls/smithed_crafter/shaped_recipes.mcfunction"
	SIMPLENERGY_PULVERIZER_PATH: str = f"{build_datapack}/data/{namespace}/function/calls/simplenergy/pulverizer_recipes.mcfunction"
	FURNACE_NBT_PATH: str = f"{build_datapack}/data/{namespace}/function/calls/furnace_nbt_recipes"
	SMELTING: list[str] = ["smelting", "blasting", "smoking"]

	# Functions for recipes
	@simple_cache
	def vanilla_shapeless_recipe(recipe: dict, item: str) -> dict:
		""" Generate the dictionnary for the recipe json file
		Args:
			recipe	(dict):	The recipe to generate
			item	(str):	The item to generate the recipe for
		Returns:
			dict: The generated recipe
		"""
		result_ingr = ingr_repr(item, namespace) if not recipe.get("result") else recipe["result"]
		to_return = {
			"type": "minecraft:" + recipe["type"],
			"category": recipe[CATEGORY],
			"group": recipe["group"] if recipe.get("group") else None,
			"ingredients": recipe["ingredients"],
			"result": item_to_id_ingr_repr(get_item_from_ingredient(config, result_ingr)),
		}
		if not to_return["group"]:
			del to_return["group"]
		to_return["result"]["count"] = recipe["result_count"]
		return to_return

	@simple_cache
	def vanilla_shaped_recipe(recipe: dict, item: str) -> dict:
		result_ingr = ingr_repr(item, namespace) if not recipe.get("result") else recipe["result"]
		to_return = {
			"type": "minecraft:" + recipe["type"],
			"category": recipe[CATEGORY],
			"group": recipe["group"] if recipe.get("group") else None,
			"pattern": recipe["shape"],
			"key": recipe["ingredients"],
			"result": item_to_id_ingr_repr(get_item_from_ingredient(config, result_ingr)),
		}
		if not to_return["group"]:
			del to_return["group"]
		to_return["result"]["count"] = recipe["result_count"]
		return to_return
	
	@simple_cache
	def vanilla_furnace_recipe(recipe: dict, item: str) -> dict:
		result_ingr = ingr_repr(item, namespace) if not recipe.get("result") else recipe["result"]
		to_return = {
			"type": "minecraft:" + recipe["type"],
			"category": recipe[CATEGORY],
			"group": recipe["group"] if recipe.get("group") else None,
			"ingredient": recipe["ingredient"],
			"result": item_to_id_ingr_repr(get_item_from_ingredient(config, result_ingr)),
		}
		if not to_return["group"]:
			del to_return["group"]
		to_return["result"]["count"] = recipe["result_count"]
		return to_return
	
	@simple_cache
	def smithed_shapeless_recipe(recipe: dict, result_loot: str) -> str:
		# Get unique ingredients and their count
		unique_ingredients: list[tuple[int,dict]] = []
		for ingr in recipe["ingredients"]:
			index: int = -1
			for i, (_, e) in enumerate(unique_ingredients):
				if str(ingr) == str(e):
					index = i
					break
			if index == -1:
				unique_ingredients.append((1, ingr))
			else:
				unique_ingredients[index] = (unique_ingredients[index][0] + 1, unique_ingredients[index][1])
		
		# Write the line
		line: str = f"execute if score @s smithed.data matches 0 store result score @s smithed.data if score count smithed.data matches {len(unique_ingredients)} if data storage smithed.crafter:input "
		r: dict[str, list] = {"recipe": []}
		for count, ingr in unique_ingredients:
			item: dict = {"count": count}
			item.update(ingr)
			r["recipe"].append(item_to_id_ingr_repr(item))
		line += json.dumps(r)
		if recipe.get(SMITHED_CRAFTER_COMMAND):
			line += f" run {recipe[SMITHED_CRAFTER_COMMAND]}"
		else:
			line += f" run loot replace block ~ ~ ~ container.16 loot {result_loot}"
		return line + "\n"
	
	@simple_cache
	def smithed_shaped_recipe(recipe: dict, result_loot: str) -> str:

		# Convert ingredients to aimed recipes
		ingredients: dict[str, dict] = recipe["ingredients"]
		recipes: dict[int, list[dict]] = {0:[], 1:[], 2:[]}
		for i, row in enumerate(recipe["shape"]):
			for slot, char in enumerate(row):
				ingredient = ingredients.get(char)
				if ingredient:
					ingr = {"Slot": slot}
					ingr.update(ingredient)
					recipes[i].append(item_to_id_ingr_repr(ingr))
				else:
					recipes[i].append({"Slot": slot, "id": "minecraft:air"})

		# Generate the dump
		dump: str = "{"
		for l, ingrs in recipes.items():
			dump += f"{l}:["
			for ingr in ingrs:
				ingr = ingr.copy()
				slot: int = ingr.pop("Slot")
				ingr = json.dumps(ingr)[1:-1]
				dump += f'{{"Slot":{slot}b, {ingr}}},'
			if dump[-1] == ',':
				dump = dump[:-1] + "],"
			else:
				dump += "],"
		if dump[-1] == ',':
			dump = dump[:-1] + "}"
		else:
			dump += "}"
		
		# Return the line
		line = f"execute if score @s smithed.data matches 0 store result score @s smithed.data if data storage smithed.crafter:input recipe{dump}"
		if recipe.get(SMITHED_CRAFTER_COMMAND):
			line += f" run {recipe[SMITHED_CRAFTER_COMMAND]}"
		else:
			line += f" run loot replace block ~ ~ ~ container.16 loot {result_loot}\n"
		return line

	@simple_cache
	def simplenergy_pulverizer_recipe(recipe: dict, item: str) -> str:
		""" Generate the line for the recipe of the Pulverizer
		Args:
			recipe	(dict):	The recipe to generate
			item	(str):	The item to generate the recipe for
		Returns:
			str: The line for the recipe
		"""
		ingredient: dict = item_to_id_ingr_repr(recipe["ingredient"])
		result: dict = item_to_id_ingr_repr(get_item_from_ingredient(config, recipe["result"])) if recipe.get("result") else ingr_repr(item, namespace)
		line: str = f"execute if score #found simplenergy.data matches 0 store result score #found simplenergy.data if data storage simplenergy:main pulverizer.input"
		line += json.dumps(ingredient)
		line += f" run loot replace entity @s contents loot {loot_table_from_ingredient(config, result, recipe['result_count'])}"
		return line + "\n"

	@simple_cache
	def furnace_nbt_recipe(recipe: dict, result_loot: str, result_ingr: dict) -> str:
		ingredient: dict = recipe["ingredient"]
		result: dict = item_to_id_ingr_repr(get_item_from_ingredient(config, result_ingr))

		# Create a vanilla recipe for the furnace
		type: str = recipe["type"]
		ingredient_vanilla: str = get_vanilla_item_id_from_ingredient(config, ingredient)
		result_item: str = ingr_to_id(result_ingr).replace(':','_')
		path: str = f"{build_datapack}/data/furnace_nbt_recipes/recipe/vanilla_items/{type}__{ingredient_vanilla.split(':')[1]}__{result_item}.json"
		type = f"minecraft:{type}" if ":" not in type else type
		json_file: dict = {"type":type,"ingredient":{"item": ingredient_vanilla},"result":result,"experience":recipe.get("experience", 0),"cookingtime":recipe.get("cookingtime", 200)}
		write_to_file(path, super_json_dump(json_file, max_level = -1), overwrite = True)

		# Prepare line and return
		line: str = "execute if score #found furnace_nbt_recipes.data matches 0 store result score #found furnace_nbt_recipes.data if data storage furnace_nbt_recipes:main input"
		line += json.dumps(ingredient)
		line += f" run loot replace block ~ ~ ~ container.3 loot {result_loot}"
		return line + "\n"

	@simple_cache
	def furnace_xp_reward(recipe: dict, experience: float) -> str:

		# Create the function for the reward
		file: str = f"""
# Add RecipesUsed nbt to the furnace
scoreboard players set #count furnace_nbt_recipes.data 0
execute store result score #count furnace_nbt_recipes.data run data get storage furnace_nbt_recipes:main furnace.RecipesUsed."furnace_nbt_recipes:xp/{experience}"
scoreboard players add #count furnace_nbt_recipes.data 1
execute store result block ~ ~ ~ RecipesUsed."furnace_nbt_recipes:xp/{experience}" int 1 run scoreboard players get #count furnace_nbt_recipes.data
scoreboard players reset #count furnace_nbt_recipes.data
"""
		write_to_file(f"{FURNACE_NBT_PATH}/xp_reward/{experience}.mcfunction", file, overwrite = True)

		# Create the recipe for the reward
		json_file: dict = {"type":"minecraft:smelting","ingredient":{"item":"minecraft:command_block"},"result":{"id":"minecraft:command_block"},"experience":experience,"cookingtime":200}
		write_to_file(f"{build_datapack}/data/furnace_nbt_recipes/recipe/xp/{experience}.json", super_json_dump(json_file, max_level = -1), overwrite = True)

		# Prepare line and return
		line: str = f"execute if score #found furnace_nbt_recipes.data matches 0 store result score #found furnace_nbt_recipes.data if data storage furnace_nbt_recipes:main input"
		ingredient: dict = recipe["ingredient"]
		line += json.dumps(ingredient)
		line += f" run function {namespace}:calls/furnace_nbt_recipes/xp_reward/{experience}\n"
		return line

	# Check if smithed crafter and Furnace NBT Recipes will be used
	smithed_crafter_used: bool = False
	furnace_nbt_used: bool = False
	furnace_nbt_vanilla_items: set[str] = set()
	items: list[tuple[str, dict]] = list(config['database'].items())
	any_recipe: bool = False
	for item, data in items:
		crafts: list[dict] = list(data.get(RESULT_OF_CRAFTING, []))
		crafts += list(data.get(USED_FOR_CRAFTING, []))
		for recipe in crafts:
			if recipe["type"] in ["crafting_shapeless", "crafting_shaped"]:
				any_recipe = True

			# Transform ingr to a list of dicts
			ingr: list[dict] = recipe.get("ingredients")
			if isinstance(ingr, dict):
				ingr = list(ingr.values())
			if not ingr:
				ingr = [recipe.get("ingredient")]
			
			# If there is a component in the ingredients of shaped/shapeless, use smithed crafter
			if not smithed_crafter_used and recipe.get("type") in ["crafting_shapeless", "crafting_shaped"] and any(i.get("components") for i in ingr):
				smithed_crafter_used = True
				if not official_lib_used("smithed.crafter"):
					debug(f"Found a crafting table recipe using custom item in ingredients, adding 'smithed.crafter' dependency")
			
			# If there is a component in the ingredient furnace, use furnace nbt recipes
			if not furnace_nbt_used and recipe.get("type") in SMELTING and ingr[0].get("components"):
				furnace_nbt_used = True
				if not official_lib_used("furnace_nbt_recipes"):
					debug(f"Found a furnace recipe using custom item in ingredient, adding 'furnace_nbt_recipes' dependency")
	
	# If there is any shaped or shapeless recipe, link the functions
	if any_recipe:
		shapeless_func_tag: str = f"{build_datapack}/data/smithed.crafter/tags/function/event/shapeless_recipes.json"
		shaped_func_tag: str = f"{build_datapack}/data/smithed.crafter/tags/function/event/recipes.json"
		write_to_file(shapeless_func_tag, super_json_dump({"values": [f"{namespace}:calls/smithed_crafter/shapeless_recipes"]}))
		write_to_file(shaped_func_tag, super_json_dump({"values": [f"{namespace}:calls/smithed_crafter/shaped_recipes"]}))

	# Generate recipes with vanilla input (no components)
	vanilla_generated_recipes = []
	for item, data in items:
		crafts: list[dict] = list(data.get(RESULT_OF_CRAFTING, []))
		crafts += list(data.get(USED_FOR_CRAFTING, []))
				
		i = 1
		for recipe in crafts:

			# Get ingredients
			name = f"{item}" if i == 1 else f"{item}_{i}"
			ingr = recipe.get("ingredients")
			if not ingr:
				ingr = recipe.get("ingredient")
			
			# Get possible result item
			if not recipe.get("result"):
				result_loot_table = loot_table_from_ingredient(config, ingr_repr(item, namespace), recipe["result_count"])
			else:
				result_loot_table = loot_table_from_ingredient(config, recipe["result"], recipe["result_count"])

			# Shapeless
			if recipe["type"] == "crafting_shapeless":

				# Vanilla recipe
				if all(i.get("item") for i in ingr):
					r = vanilla_shapeless_recipe(recipe, item)
					write_to_file(f"{build_datapack}/data/{namespace}/recipe/{name}.json", super_json_dump(r, max_level = 5))
					i += 1
					vanilla_generated_recipes.append(name)
				
				# Custom ingredients recipe
				write_to_file(SMITHED_SHAPELESS_PATH, smithed_shapeless_recipe(recipe, result_loot_table))
			
			# Shaped
			elif recipe["type"] == "crafting_shaped":

				# Vanilla recipe
				if all(i.get("item") for i in ingr.values()):
					r = vanilla_shaped_recipe(recipe, item)
					write_to_file(f"{build_datapack}/data/{namespace}/recipe/{name}.json", super_json_dump(r, max_level = 5))
					i += 1
					vanilla_generated_recipes.append(name)
				
				# Custom ingredients recipe
				write_to_file(SMITHED_SHAPED_PATH, smithed_shaped_recipe(recipe, result_loot_table))
			
			# Furnace
			elif recipe["type"] in SMELTING + ["campfire_cooking"]:

				# Vanilla recipe
				if ingr.get("item"):
					r = vanilla_furnace_recipe(recipe, item)
					write_to_file(f"{build_datapack}/data/{namespace}/recipe/{name}.json", super_json_dump(r, max_level = 5))
					i += 1
					vanilla_generated_recipes.append(name)
				
				if furnace_nbt_used and recipe["type"] in SMELTING:
					if recipe.get("result"):
						line: str = furnace_nbt_recipe(recipe, result_loot_table, recipe["result"])
					else:
						line: str = furnace_nbt_recipe(recipe, result_loot_table, ingr_repr(item, namespace))
					type: str = recipe["type"]
					path: str = f"{FURNACE_NBT_PATH}/{type}_recipes.mcfunction"
					write_to_file(path, line)

					# Add vanilla item
					furnace_nbt_vanilla_items.add(get_vanilla_item_id_from_ingredient(config, ingr))

					# Add xp reward
					experience: float = recipe.get("experience", 0)
					if experience > 0:
						line = furnace_xp_reward(recipe, experience)
						path = f"{FURNACE_NBT_PATH}/recipes_used.mcfunction"
						if line not in FILES_TO_WRITE.get(path, ""):
							write_to_file(path, line)

			# Pulverizer
			elif recipe["type"] == PULVERIZING:
				write_to_file(SIMPLENERGY_PULVERIZER_PATH, simplenergy_pulverizer_recipe(recipe, item))
				write_to_file(f"{build_datapack}/data/simplenergy/tags/function/calls/pulverizer_recipes.json", super_json_dump({"values": [f"{namespace}:calls/simplenergy/pulverizer_recipes"]}))

		pass

	
	# If furnace nbt recipes is used,
	if furnace_nbt_used:

		# Add vanilla items in disable cooking
		for item in sorted(furnace_nbt_vanilla_items):
			write_to_file(f"{FURNACE_NBT_PATH}/disable_cooking.mcfunction", f"execute if score #reset furnace_nbt_recipes.data matches 0 store success score #reset furnace_nbt_recipes.data if data storage furnace_nbt_recipes:main input{{\"id\":\"{item}\"}}\n")

		# Link the functions
		for r in SMELTING:
			if FILES_TO_WRITE.get(f"{FURNACE_NBT_PATH}/{r}_recipes.mcfunction"):
				write_to_file(f"{build_datapack}/data/furnace_nbt_recipes/tags/function/v1/{r}_recipes.json", super_json_dump({"values": [f"{namespace}:calls/furnace_nbt_recipes/{r}_recipes"]}))
		if FILES_TO_WRITE.get(f"{FURNACE_NBT_PATH}/disable_cooking.mcfunction"):
			write_to_file(f"{build_datapack}/data/furnace_nbt_recipes/tags/function/v1/disable_cooking.json", super_json_dump({"values": [f"{namespace}:calls/furnace_nbt_recipes/disable_cooking"]}))
		if FILES_TO_WRITE.get(f"{FURNACE_NBT_PATH}/recipes_used.mcfunction"):
			write_to_file(f"{build_datapack}/data/furnace_nbt_recipes/tags/function/v1/recipes_used.json", super_json_dump({"values": [f"{namespace}:calls/furnace_nbt_recipes/recipes_used"]}))

	# Create a function that will give all recipes
	content = "\n# Get all recipes\n"
	for recipe in vanilla_generated_recipes:
		content += f"recipe give @s {namespace}:{recipe}\n"
	write_to_file(f"{config['datapack_functions']}/utils/get_all_recipes.mcfunction", content + "\n")


	# Unlock vanilla recipes when at least one of the ingredient is in inventory
	if vanilla_generated_recipes:
		ingredients: dict[str, set[str]] = {}

		# For each recipe, get the ingredients and link them to the recipe
		for recipe_name in vanilla_generated_recipes:
			recipe_path: str = f"{build_datapack}/data/{namespace}/recipe/{recipe_name}.json"
			recipe: dict = json.loads(read_file(recipe_path))
			for ingr in get_ingredients_from_recipe(recipe):
				if ingr not in ingredients:
					ingredients[ingr] = set()
				ingredients[ingr].add(recipe_name)
		
		# Write an inventory_changed advancement
		adv_path: str = f"{build_datapack}/data/{namespace}/advancement/unlock_recipes.json"
		adv_json: dict = {"criteria":{"requirement":{"trigger":"minecraft:inventory_changed"}},"rewards":{"function":f"{namespace}:advancements/unlock_recipes"}}
		write_to_file(adv_path, super_json_dump(adv_json, max_level = -1))

		# Write the function that will unlock the recipes
		func_path: str = f"{build_datapack}/data/{namespace}/function/advancements/unlock_recipes.mcfunction"
		content = f"""
# Revoke advancement
advancement revoke @s only {namespace}:unlock_recipes

## For each ingredient in inventory, unlock the recipes
"""
		for ingr, recipes in ingredients.items():
			recipes: list = sorted(recipes)
			
			content += f"# {ingr}\nscoreboard players set #success {namespace}.data 0\nexecute store success score #success {namespace}.data if items entity @s container.* {ingr}\n"
			for recipe in recipes:
				content += f"execute if score #success {namespace}.data matches 1 run recipe give @s {namespace}:{recipe}\n"
			content += "\n"
		write_to_file(func_path, content)

	# Final print
	info("Recipes generated")

