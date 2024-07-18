
# Imports & font textures
from ..utils.io import *
from ..utils.print import *
from ..utils.cache import simple_cache
from ..utils.ingredients import *
from ..constants import *
from .shared_import import *
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from model_resolver.cli import main as model_resolver_main
import requests

# Generate high res simple case no border
def load_simple_case_no_border(high_res: bool) -> Image.Image:
	path = f"{TEMPLATES_PATH}/simple_case_no_border.png"
	img = Image.open(path)
	if not high_res:
		return img

	# Make the image bigger on the right
	middle_x = img.size[0] // 2
	result = Image.new("RGBA", (img.size[0] + 1, img.size[1]))
	result.paste(img, (0, 0))
	img = img.crop((middle_x, 0, img.size[0], img.size[1]))
	result.paste(img, (middle_x + 1, 0))
	return result

# Careful resize
def careful_resize(image: Image.Image, max_result_size: int) -> Image.Image:
	""" Resize an image while keeping the aspect ratio.\n
	Example 1: if the image is 100x200 and the max_result_size is 150, the result will be 75x150.\n
	Example 2: if the image is 200x100 and the max_result_size is 256, the result will be 256x128.\n
	Args:
		image			(Image):	The image to resize
		max_result_size	(int):		The minimum result size of the image (ex: 256)
	Returns:
		Image: The resized image
	"""
	if image.size[0] >= image.size[1]:
		factor = max_result_size / image.size[0]
		return image.resize((max_result_size, int(image.size[1] * factor)), Image.NEAREST)
	else:
		factor = max_result_size / image.size[1]
		return image.resize((int(image.size[0] * factor), max_result_size), Image.NEAREST)

# Generate a border for a given Image
def add_border(image: Image.Image, border_color: tuple, border_size: int, is_rectangle_shape: bool) -> Image.Image:
	""" Add a border to every part of the image
	Args:
		image				(Image):	The image to add the border
		border_color		(tuple):	The color of the border
		border_size			(int):		The size of the border
		is_rectangle_shape	(bool):		If the shape is a rectangle or not (so we can choose between two algorithms)
	Returns:
		Image: The image with the border
	"""
	# Convert image to RGBA and load
	image = image.convert("RGBA")
	pixels = image.load()

	# Method 1: Image shape is not a rectangle
	if not is_rectangle_shape:
		# Get all transparent pixels
		pixels_to_change = [(x, y) for x in range(image.width) for y in range(image.height) if pixels[x, y][3] == 0]

		# Setup pixel view range (border_size * border_size)
		r = range(-border_size, border_size + 1)

		# For each pixel in the list, try to place border color
		for x, y in pixels_to_change:
			try:
				# If there is a pixel that is not transparent or equal to the border color in the range, place border_color
				if any(pixels[x + dx, y + dy][3] != 0 and pixels[x + dx, y + dy] != border_color for dx in r for dy in r):
					pixels[x, y] = border_color
			except:
				pass
	
	# Method 2: Image shape is a rectangle
	else:
		# Get image real height and width
		height, width = 8, 8
		while height < image.height and pixels[8, height][3]!= 0:
			height += 1
		while width < image.width and pixels[width, 8][3]!= 0:
			width += 1
		
		# Paste the border color in the image
		border = Image.new("RGBA", (width + 2, height + 2), border_color)
		border.paste(image, (0, 0), image)
		image.paste(border, (0, 0), border)
	
	# Return the image
	return image

# Generate an image showing the result count
def image_count(count: int) -> Image.Image:
	""" Generate an image showing the result count
	Args:
		count (int): The count to show
	Returns:
		Image: The image with the count
	"""
	# Create the image
	img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
	draw = ImageDraw.Draw(img)
	font_size = 16
	font = ImageFont.truetype(f"{TEMPLATES_PATH}/minecraft_font.ttf", size = font_size)

	# Calculate text size and positions of the two texts
	text_width = draw.textlength(str(count), font = font)
	text_height = font_size + 4
	pos_1 = (34-text_width), (32-text_height)
	pos_2 = (32-text_width), (30-text_height)
	
	# Draw the count
	draw.text(pos_1, str(count), (50, 50, 50), font = font)
	draw.text(pos_2, str(count), (255, 255, 255), font = font)
	return img

# Generate iso renders for every item in the config['database']
def generate_all_iso_renders(config: dict):
	path = config['manual_path'] + "/items"
	os.makedirs(f"{path}/{config['namespace']}", exist_ok = True)
	for_model_resolver = {}
	for item, data in config['database'].items():
		
		# If it's not a block, simply copy the texture
		try:
			if data["id"] == CUSTOM_BLOCK_VANILLA:
				raise Exception()
			if not os.path.exists(f"{path}/{config['namespace']}/{item}.png") or not config['cache_manual_assets']:
				super_copy(f"{config['textures_folder']}/{item}.png", f"{path}/{config['namespace']}/{item}.png")
		except:
			# Else, add the block to the model resolver list
			# Skip if item is already generated (to prevent launcher OpenGL for nothing)
			if os.path.exists(f"{path}/{config['namespace']}/{item}.png") and config['cache_manual_assets']:
				continue

			# Add to the model resolver queue
			rp_path = f"{config['namespace']}:block/{item}"
			dst_path = f"{path}/{config['namespace']}/{item}.png"
			for_model_resolver[rp_path] = dst_path

	# Launch model resolvers for remaining blocks
	if len(for_model_resolver) > 0:
		load_dir = Path(config['build_resource_pack'])
		debug("Generating iso renders for %d items" % len(for_model_resolver))
		model_resolver_main(
			render_size = config['opengl_resolution'],
			load_dir = load_dir,
			output_dir = None,
			use_cache = False,
			minecraft_version = "latest",
			__special_filter__ = for_model_resolver
		)
	debug("Generated iso renders for all items, or used cached renders")

	## Copy every used vanilla items
	# Get every used vanilla items
	used_vanilla_items = set()
	for item, data in config['database'].items():
		all_crafts: list[dict] = list(data.get(RESULT_OF_CRAFTING,[]))
		all_crafts += list(data.get(USED_FOR_CRAFTING,[]))
		for recipe in all_crafts:
			ingredients = []
			if "ingredients" in recipe:
				ingredients = recipe["ingredients"]
				if isinstance(ingredients, dict):
					ingredients = ingredients.values()
			elif "ingredient" in recipe:
				ingredients = [recipe["ingredient"]]
			for ingredient in ingredients:
				if "item" in ingredient:
					used_vanilla_items.add(ingredient["item"].split(":")[1])
			if "result" in recipe and "item" in recipe["result"]:
				used_vanilla_items.add(recipe["result"]["item"].split(":")[1])
		pass

	# Download all the vanilla textures from the wiki
	for item in used_vanilla_items:
		destination = f"{path}/minecraft/{item}.png"
		if not (os.path.exists(destination) and config['cache_manual_assets']):	# If not downloaded yet or not using cache
			debug(f"Downloading texture for item '{item}'...")
			response = requests.get(f"{DOWNLOAD_VANILLA_ASSETS_RAW}/item/{item}.png")
			if response.status_code == 200:
				with super_open(destination, "wb") as file:
					file.write(response.content)
			else:
				warning(f"Failed to download texture for item '{item}', please add it manually to '{destination}'")
				warning(f"Suggestion link: '{DOWNLOAD_VANILLA_ASSETS_SOURCE}'")
		pass
	debug("Downloaded all the vanilla textures, or using cached ones")


# Generate page font function (called in utils)
def generate_page_font(config: dict, name: str, page_font: str, craft: dict|None = None, output_name: str = "") -> None:
	""" Generate the page font image with the proper items
	Args:
		name			(str):			Name of the item
		page_font		(str):			Font string for the page
		craft			(dict|None):	Crafting recipe dictionary (None if no craft)
		output_name		(str|None):		The output name (None if default, used for wiki crafts)
	"""
	if not output_name:
		output_filename = name
	else:
		output_filename = output_name

	# Get result texture (to place later)
	image_path = f"{config['manual_path']}/items/{config['namespace']}/{name}.png"
	if not os.path.exists(image_path):
		error(f"Missing item texture at '{image_path}'")
	result_texture = Image.open(image_path)

	# If recipe result is specified, take the right texture
	if craft and craft.get("result"):
		result_id = ingr_to_id(craft["result"])
		result_id = result_id.replace(":", "/")
		image_path = f"{config['manual_path']}/items/{result_id}.png"
		result_texture = Image.open(image_path)

	# Check if there is a craft
	if craft:

		# Resize the texture and get the mask
		result_texture = careful_resize(result_texture, SQUARE_SIZE)
		result_mask = result_texture.convert("RGBA").split()[3]

		# Shaped craft
		if craft["type"] in "crafting_shaped":

			# Get the image template and append the provider
			shaped_size = max(2, max(len(craft["shape"]), len(craft["shape"][0])))
			template = Image.open(f"{TEMPLATES_PATH}/shaped_{shaped_size}x{shaped_size}.png")
			if not config['manual_high_resolution']:
				font_providers.append({"type":"bitmap","file":f"{config['namespace']}:font/page/{output_filename}.png", "ascent": 0 if not output_name else 6, "height": 60, "chars": [page_font]})

			# Loop the shape matrix
			STARTING_PIXEL = (4, 4)
			CASE_OFFSETS = (4, 4)
			for i, row in enumerate(craft["shape"]):
				for j, symbol in enumerate(row):
					if symbol != " ":
						ingredient = craft["ingredients"][symbol]
						if ingredient.get("components"):
							# get "iyc:steel_ingot" in {'components': {'custom_data': {'iyc': {'steel_ingot': True}}}}
							item = ingr_to_id(ingredient)
						else:
							item = ingredient["item"]	# Vanilla item, ex: "minecraft:glowstone"
						
						# Get the texture and place it at the coords
						item = item.replace(":", "/")
						image_path = f"{config['manual_path']}/items/{item}.png"
						if not os.path.exists(image_path):
							error(f"Missing item texture at '{image_path}'")
						item_texture = Image.open(image_path)
						item_texture = careful_resize(item_texture, SQUARE_SIZE)
						coords = (
							j * (SQUARE_SIZE + CASE_OFFSETS[0]) + STARTING_PIXEL[0],
							i * (SQUARE_SIZE + CASE_OFFSETS[1]) + STARTING_PIXEL[1]
						)
						mask = item_texture.convert("RGBA").split()[3]
						template.paste(item_texture, coords, mask)
			
			# Place the result item
			coords = (148, 40) if shaped_size == 3 else (118, 25)
			template.paste(result_texture, coords, result_mask)

			# Place count if the result is greater than 1
			if craft["result_count"] > 1:
				count_img = image_count(craft["result_count"])
				template.paste(count_img, [x + 2 for x in coords], count_img)

			# Save the image
			if not config['manual_high_resolution']:
				template.save(f"{config['manual_path']}/font/page/{output_filename}.png")

		# Smelting craft
		elif craft["type"] in FURNACES_RECIPES_TYPES:
			
			# Get the image template and append the provider
			template = Image.open(f"{TEMPLATES_PATH}/furnace.png")
			if not config['manual_high_resolution']:
				font_providers.append({"type":"bitmap","file":f"{config['namespace']}:font/page/{output_filename}.png", "ascent": 0 if not output_name else 6, "height": 60, "chars": [page_font]})

			# Place input item
			input_item = ingr_to_id(craft["ingredient"])
			input_item = input_item.replace(":", "/")
			image_path = f"{config['manual_path']}/items/{input_item}.png"
			if not os.path.exists(image_path):
				error(f"Missing item texture at '{image_path}'")
			item_texture = Image.open(image_path)
			item_texture = careful_resize(item_texture, SQUARE_SIZE)
			mask = item_texture.convert("RGBA").split()[3]
			template.paste(item_texture, (4, 4), mask)

			# Place the result item and count if the result is greater than 1
			coords = (124, 40)
			template.paste(result_texture, coords, result_mask)
			if craft["result_count"] > 1:
				count_img = image_count(craft["result_count"])
				template.paste(count_img, [x + 2 for x in coords], count_img)
			
			# Save the image
			if not config['manual_high_resolution']:
				template.save(f"{config['manual_path']}/font/page/{output_filename}.png")
	
	# Else, there is no craft, just put the item in a box
	else:
		# Get the image template and append the provider
		template = Image.open(f"{TEMPLATES_PATH}/simple_case_no_border.png")
		factor = 1
		if config['manual_high_resolution']:
			factor = 256 // template.size[0]
			result_texture = careful_resize(result_texture, SQUARE_SIZE * factor)
			template = careful_resize(template, 256)
			result_mask = result_texture.convert("RGBA").split()[3]
		else:
			# Resize the texture and get the mask
			result_texture = careful_resize(result_texture, SQUARE_SIZE)
			result_mask = result_texture.convert("RGBA").split()[3]
		font_providers.append({"type":"bitmap","file":f"{config['namespace']}:font/page/{output_filename}.png", "ascent": 0 if not output_name else 6, "height": 40, "chars": [page_font]})

		# Place the result item
		template.paste(result_texture, (2 * factor, 2 * factor), result_mask)
		template = add_border(template, BORDER_COLOR, BORDER_SIZE, is_rectangle_shape = True)
		template.save(f"{config['manual_path']}/font/page/{output_filename}.png")
	return

# Convert craft function
@simple_cache
def convert_shapeless_to_shaped(craft: dict) -> dict:
	""" Convert a shapeless craft to a shaped craft
	Args:
		craft (dict): The craft to convert
	Returns:
		dict: The craft converted
	"""
	new_craft = {"type": "crafting_shaped", "result_count": craft["result_count"], "ingredients": {}}
	if craft.get("result"):
		new_craft["result"] = craft["result"]

	# Get all ingredients to the dictionary
	next_key = "A"
	for ingr in craft["ingredients"]:
		key = next_key
		for new_key, new_ingr in new_craft["ingredients"].items():
			if str(ingr) == str(new_ingr):
				key = new_key
				break

		if key == next_key:
			new_craft["ingredients"][next_key] = ingr
			next_key = chr(ord(next_key) + 1)

	# Make the shape of the craft, with an exception when 2 materials to put one alone in the center
	if len(new_craft["ingredients"]) == 2 and len(craft["ingredients"]) == 9:
		new_craft["shape"] = ["AAA","ABA","AAA"]
	else:

		# For each ingredient, add to the shape depending on the occurences
		new_craft["shape"] = []
		for key, ingr in new_craft["ingredients"].items():
			for ingr_craft in craft["ingredients"]:
				if str(ingr_craft) == str(ingr):
					new_craft["shape"].append(key)
		
		# Fix the shape (ex: ["A","A","A","B","B","B","C","C","C"] -> ["AAA","BBB","CCC"])
		# ex 2: ["A","B","C","D"] -> ["AB","CD"]
		col_size = 3
		if len(new_craft["shape"]) <= 4:
			col_size = 2
		ranged = range(0, len(new_craft["shape"]), col_size)
		new_craft["shape"] = ["".join(new_craft["shape"][i:i + col_size]) for i in ranged]
	
	# Return the shaped craft
	return new_craft


# Convert ingredient to formatted JSON for book
COMPONENTS_TO_IGNORE = NOT_COMPONENTS + ["custom_data", "count", "profile", "dyed_color", "container"]
def get_item_component(config: dict, ingredient: dict|str, only_those_components: list[str] = None, count: int = 1) -> dict:
	""" Generate item hover text for a craft ingredient
	Args:
		ingredient (dict|str): The ingredient
			ex: {'components': {'custom_data': {'iyc': {'adamantium_fragment': True}}}}
			ex: {'item': 'minecraft:stick'}
			ex: "adamantium_fragment"	# Only available for the datapack items
	Returns:
		dict: The text component
			ex: {"text":NONE_FONT,"color":"white","hoverEvent":{"action":"show_item","contents":{"id":"minecraft:command_block", "components": {...}}},"clickEvent":{"action":"change_page","value":"8"}}
			ex: {"text":NONE_FONT,"color":"white","hoverEvent":{"action":"show_item","contents":{"id":"minecraft:stick"}}}
	"""
	# Get the item id
	formatted = {"text": NONE_FONT, "hoverEvent":{"action":"show_item","contents":{"id":""}}}	# Default hoverEvent
	if isinstance(ingredient, dict) and ingredient.get("item"):
		formatted["hoverEvent"]["contents"]["id"] = ingredient["item"]
	else:
		# Get the item in the database
		if isinstance(ingredient, str):
			id = ingredient
			item = config['database'][ingredient]
		else:
			custom_data: dict = ingredient["components"]["minecraft:custom_data"]
			id = ingr_to_id(ingredient, add_namespace = False)
			if custom_data.get(config['namespace']):
				item = config['database'].get(id)
			else:
				ns = list(custom_data.keys())[0] + ":"
				for data in custom_data.values():
					item = config['external_database'].get(ns + list(data.keys())[0])
					if item:
						break
		if not item:
			error("Item not found in database or external database: " + str(ingredient))
		
		# Copy id and components
		formatted["hoverEvent"]["contents"]["id"] = item["id"].replace("minecraft:", "")
		components = {}
		if only_those_components:
			for key in only_those_components:
				if key in item:
					components[key] = item[key]
		else:
			for key, value in item.items():
				if key not in COMPONENTS_TO_IGNORE:
					components[key] = value
		formatted["hoverEvent"]["contents"]["components"] = components

		# If item is from my datapack, get its page number
		page_number = get_page_number(id)
		if page_number != -1:
			formatted["clickEvent"] = {"action":"change_page","value":str(page_number)}
	
	# High resolution
	if config['manual_high_resolution']:
		formatted["text"] = high_res_font_from_ingredient(config, ingredient, count)

	# Return
	return formatted


# Generate all craft types content
def generate_craft_content(config: dict, craft: dict, name: str, page_font: str) -> list:
	""" Generate the content for the craft type
	Args:
		craft		(dict):	The craft dictionary, ex: {"type": "crafting_shaped","result_count": 1,"category": "equipment","shape": ["XXX","X X"],"ingredients": {"X": {"components": {"custom_data": {"iyc": {"adamantium": true}}}}}}
		name		(str):	The name of the item, ex: "adamantium_pickaxe"
		page_font	(str):	The font for the page, ex: "\u0002"
	Returns:
		list:	The content of the craft, ex: [{"text": ...}]
	"""
	craft_type = craft["type"]
	content = [{"text": "", "font": config['namespace'] + ':' + FONT_FILE, "color": "white"}]	# Make default font for every next component

	# Convert shapeless crafting to shaped crafting
	if craft_type == "crafting_shapeless":
		craft = convert_shapeless_to_shaped(craft)
		craft_type = "crafting_shaped"
	
	# If high resolution, get proper page font
	if config['manual_high_resolution']:
		page_font = high_res_font_from_craft(craft)
	
	# Show up item title and page font
	titled = name.replace("_", " ").title() + "\n"
	content.append({"text": titled, "font": "minecraft:default", "color": "black", "underlined": True})
	content.append(SMALL_NONE_FONT + page_font + "\n")
	
	# Generate the image for the page
	generate_page_font(config, name, page_font, craft)

	# Get result component
	result_count = craft.get("result_count", 1)
	if not craft.get("result"):
		result_component = get_item_component(config, name, count = result_count)
	else:
		result_component = get_item_component(config, craft["result"], count = result_count)
	if result_component.get("clickEvent"):
		del result_component["clickEvent"]	# Remove clickEvent for result item (as we already are on the page)
	result_component["text"] = MICRO_NONE_FONT + result_component["text"]	# Left adjustment

	# If the craft is shaped
	if craft_type == "crafting_shaped":

		# Convert each ingredients to its text component
		formatted_ingredients: dict[str, dict] = {}
		for k, v in craft["ingredients"].items():
			formatted_ingredients[k] = get_item_component(config, v)

		# Add each ingredient to the craft
		for line in craft["shape"]:
			for i in range(2):	# We need two lines to make a square, otherwise it will be a rectangle
				content.append(SMALL_NONE_FONT)
				for k in line:
					if k == " ":
						content.append(INVISIBLE_ITEM_WIDTH)
					else:
						if i == 0:
							content.append(formatted_ingredients[k])
						else:
							copy = formatted_ingredients[k].copy()
							copy["text"] = INVISIBLE_ITEM_WIDTH
							content.append(copy)
				content.append("\n")
		if len(craft["shape"]) == 1 and len(craft["shape"][0]) < 3:
			content.append("\n")
			pass
		
		# Add the result to the craft
		if len(craft["shape"]) <= 2 and len(craft["shape"][0]) <= 2:

			# First layer of the square
			len_1 = len(craft["shape"][0])
			offset_1 = 3 - len_1
			break_line_pos = content.index("\n", content.index("\n") + 1)	# Find the second line break
			content.insert(break_line_pos, (INVISIBLE_ITEM_WIDTH * offset_1))
			content.insert(break_line_pos + 1, result_component)
			
			# Second layer of the square
			len_2 = len(craft["shape"][1]) if len(craft["shape"]) > 1 else 0
			offset_2 = 3 - len_2
			if len_2 == 0:
				content.insert(break_line_pos + 2, "\n" + SMALL_NONE_FONT)
			break_line_pos = content.index("\n", break_line_pos + 3)	# Find the third line break
			content.insert(break_line_pos, (INVISIBLE_ITEM_WIDTH * offset_2))
			copy = result_component.copy()
			copy["text"] = INVISIBLE_ITEM_WIDTH
			content.insert(break_line_pos + 1, copy)
		else:
			# First layer of the square
			len_line = len(craft["shape"][1]) if len(craft["shape"]) > 1 else 0
			offset = 4 - len_line
			break_line_pos = content.index("\n", content.index("\n") + 1)	# Find the second line break
			try:
				break_line_pos = content.index("\n", break_line_pos + 1) # Find the third line break
			except:
				content.append(SMALL_NONE_FONT)
				break_line_pos = len(content)
			content.insert(break_line_pos, (INVISIBLE_ITEM_WIDTH * (offset - 1) + SMALL_NONE_FONT * 2))
			content.insert(break_line_pos + 1, result_component)

			# Second layer of the square
			try:
				break_line_pos = content.index("\n", break_line_pos + 3)	# Find the fourth line break
			except:
				content.append("\n" + SMALL_NONE_FONT)
				break_line_pos = len(content)
			content.insert(break_line_pos, (INVISIBLE_ITEM_WIDTH * (offset - 1) + SMALL_NONE_FONT * 2))
			copy = result_component.copy()
			copy["text"] = INVISIBLE_ITEM_WIDTH
			content.insert(break_line_pos + 1, copy)

			# Add break lines for the third layer of a 3x3 craft
			if len(craft["shape"]) < 3 and len(craft["shape"][0]) == 3:
				content.append("\n\n")
				if len(craft["shape"]) < 2:
					content.append("\n")
		
	
	# If the type is furnace type,
	elif craft_type in FURNACES_RECIPES_TYPES:
		
		# Convert ingredient to its text component
		formatted_ingredient = get_item_component(config, craft["ingredient"])

		# Add the ingredient to the craft
		for i in range(2):
			content.append(SMALL_NONE_FONT)
			if i == 0:
				content.append(formatted_ingredient)
			else:
				copy = formatted_ingredient.copy()
				copy["text"] = INVISIBLE_ITEM_WIDTH
				content.append(copy)
			content.append("\n")
		
		# Add the result to the craft
		for i in range(2):
			content.append(SMALL_NONE_FONT * 4 + INVISIBLE_ITEM_WIDTH * 2)
			if i == 0:
				content.append(result_component)
			else:
				copy = result_component.copy()
				copy["text"] = INVISIBLE_ITEM_WIDTH
				content.append(copy)
			content.append("\n")
		content.append("\n\n")

	return content

# Extract unique crafts from a craft list
def unique_crafts(crafts: list[dict]) -> list[dict]:
	""" Get unique crafts from a list of crafts
	Args:
		list (list[dict]): The list of crafts
	Returns:
		list[dict]: The unique crafts
	"""
	unique = []
	strings = []
	for craft in crafts:
		if str(craft) not in strings:
			unique.append(craft)
			strings.append(str(craft))
	return unique

def remove_unknown_crafts(crafts: list[dict]) -> list[dict]:
	""" Remove crafts that are not recognized by the program
	Args:
		crafts (list[dict]): The list of crafts
	Returns:
		list[dict]: The list of crafts without unknown crafts
	"""
	supported_crafts = []
	for craft in crafts:
		if craft["type"] in CRAFTING_RECIPES_TYPES or craft["type"] in FURNACES_RECIPES_TYPES:
			supported_crafts.append(craft)
	return supported_crafts

# Generate USED_FOR_CRAFTING key like
def generate_otherside_crafts(config: dict, item: str) -> list[dict]:
	""" Generate the USED_FOR_CRAFTING key like
	Args:
		item (str): The item to generate the key for
	Returns:
		list[dict]: ex: [{"type": "crafting_shaped","result_count": 1,"category": "equipment","shape": ["XXX","X X"],"ingredients": {"X": {"components": {"custom_data": {"iyc": {"chainmail": true}}}}},"result": {"item": "minecraft:chainmail_helmet","count": 1}}, ...]
	"""
	# Get all crafts that use the item
	crafts = []
	for key, value in config['database'].items():
		if key != item and value.get(RESULT_OF_CRAFTING):
			for craft in value[RESULT_OF_CRAFTING]:
				craft: dict = craft
				if ("ingredient" in craft and item == ingr_to_id(craft["ingredient"], False)) or \
					("ingredients" in craft and isinstance(craft["ingredients"], dict) and item in [ingr_to_id(x, False) for x in craft["ingredients"].values()]) or \
					("ingredients" in craft and isinstance(craft["ingredients"], list) and item in [ingr_to_id(x, False) for x in craft["ingredients"]]):
					# Convert craft, ex:
					# before:	chainmail_helmet	{"type": "crafting_shaped","result_count": 1,"category": "equipment","shape": ["XXX","X X"],"ingredients": {"X": {"components": {"custom_data": {"iyc": {"chainmail": true}}}}}}}
					# after:	chainmail			{"type": "crafting_shaped","result_count": 1,"category": "equipment","shape": ["XXX","X X"],"ingredients": {"X": {"components": {"custom_data": {"iyc": {"chainmail": true}}}}},"result": {"item": "minecraft:chainmail_helmet","count": 1}}
					craft_copy = craft.copy()
					craft_copy["result"] = ingr_repr(key, ns = config['namespace'], count = craft["result_count"])
					crafts.append(craft_copy)
	return crafts


# Generate small craft icon
def generate_wiki_font_for_ingr(config: dict, name: str, craft: dict) -> str:
	""" Generate the wiki icon font to display in the manual for wiki buttons showing the result of the craft
	If no texture found for the resulting item, return the default wiki font
	Args:
		name	(str):	The name of the item, ex: "adamantium_fragment"
		craft	(dict):	The associed craft, ex: {"type": "crafting_shaped","result_count": 1,"category": "equipment","shape": ["XXX","X X"],"ingredients": {"X": {"components": {"custom_data": {"iyc": {"adamantium_fragment": true}}}}},"result": {"components": {"custom_data": {"iyc": {"adamantium_helmet": true}}},"count": 1}}
	Returns:
		str: The craft icon
	"""
	# Default wiki font
	font = WIKI_INGR_OF_CRAFT_FONT

	# If no result found, return the default font
	if not craft.get("result"):
		return font
	
	# Get result item texture and paste it on the wiki_ingredient_of_craft_template
	try:
		result_item = ingr_to_id(craft["result"]).replace(":", "/")
		texture_path = f"{config['manual_path']}/items/{result_item}.png"
		result_item = result_item.replace("/", "_")
		dest_path = f"{config['manual_path']}/font/wiki_icons/{result_item}.png"

		# Load texture and resize it
		item_texture = Image.open(texture_path)
		item_res = 64 if not config["manual_high_resolution"] else 256
		item_res_adjusted = int(item_res * 0.75)
		item_texture = careful_resize(item_texture, item_res_adjusted)
		item_texture = item_texture.convert("RGBA")

		# Load the template and paste the texture on it
		template = Image.open(f"{TEMPLATES_PATH}/wiki_ingredient_of_craft_template.png")
		template = careful_resize(template, item_res)
		offset = (item_res - item_res_adjusted) // 2
		template.paste(item_texture, (offset, offset), item_texture)

		# Save the result
		template.save(dest_path)

		# Prepare provider
		font = get_next_font()
		font_providers.append({"type":"bitmap","file":f"{config['namespace']}:font/wiki_icons/{result_item}.png", "ascent": 8, "height": 16, "chars": [font]})

	except Exception as e:
		warning(f"Failed to generate craft icon for {name}: {e}\nreturning default font...")
		pass

	# Return the font
	return font

# Generate high res image for item
def generate_high_res_font(config: dict, item: str, item_image: Image.Image, count: int = 1) -> str:
	""" Generate the high res font to display in the manual for the item
	Args:
		item		(str):		The name of the item, ex: "adamantium_fragment"
		item_image	(Image):	The image of the item
		count		(int):		The count of the item
	Returns:
		str: The font to the generated texture
	"""
	font = get_next_font()
	item = f"{item}_{count}" if count > 1 else item
	
	# Get output path
	path = f"{config['manual_path']}/font/high_res/{item}.png"
	provider_path = f"{config['namespace']}:font/high_res/{item}.png"
	for p in font_providers:	# Check if it already exists
		if p["file"] == provider_path:
			return MICRO_NONE_FONT + p["chars"][0]
	font_providers.append({"type":"bitmap","file": provider_path, "ascent": 7, "height": 16, "chars": [font]})


	# Generate high res font
	os.makedirs(os.path.dirname(path), exist_ok = True)
	high_res: int = 256
	resized = careful_resize(item_image, high_res)
	resized = resized.convert("RGBA")

	# Add the item count
	if count > 1:
		img_count = image_count(count)
		img_count = careful_resize(img_count, high_res)
		resized.paste(img_count, (0, 0), img_count)

	# Add invisible pixels for minecraft font at each corner
	total_width = resized.size[0] - 1
	total_height = resized.size[1] - 1
	angles = [(0, 0), (total_width, 0), (0, total_height), (total_width, total_height)]
	for angle in angles:
		resized.putpixel(angle, (0, 0, 0, 100))

	# Save the result and return the font
	resized.save(path)
	return MICRO_NONE_FONT + font

# Call the previous function
def high_res_font_from_ingredient(config: dict, ingredient: str|dict, count: int = 1) -> str:
	""" Generate the high res font to display in the manual for the ingredient
	Args:
		ingredient	(str|dict):	The ingredient, ex: "adamantium_fragment" or {"item": "minecraft:stick"} or {"components": {"custom_data": {"iyc": {"adamantium_fragment": true}}}}
		count		(int):		The count of the item
	Returns:
		str: The font to the generated texture
	"""
	# Decode the ingredient
	if isinstance(ingredient, dict):
		ingredient = ingr_to_id(ingredient, add_namespace = True)
	if ':' in ingredient:
		image_path = f"{config['manual_path']}/items/{ingredient.replace(':', '/')}.png"
		if not os.path.exists(image_path):
			error(f"Missing item texture at '{image_path}'")
		item_image = Image.open(image_path)
		ingredient = ingredient.split(":")[1]
	else:
		item_image = Image.open(f"{config['manual_path']}/items/{config['namespace']}/{ingredient}.png")
	
	# Generate the high res font
	return generate_high_res_font(config, ingredient, item_image, count)

# Util function
@simple_cache
def high_res_font_from_craft(craft: dict) -> str:
	if craft["type"] in FURNACES_RECIPES_TYPES:
		return FURNACE_FONT
	elif craft["type"] == "crafting_shaped":
		if len(craft["shape"]) == 3 or len(craft["shape"][0]) == 3:
			return SHAPED_3X3_FONT
		else:
			return SHAPED_2X2_FONT
	else:
		error(f"Unknown craft type '{craft['type']}'")
		return ""

