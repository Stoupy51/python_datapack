"""
Handles generation of book components and content
"""
from typing import Union
from .text_components import create_hover_event, create_click_event
from .shared_import import *
from ..utils.ingredients import ingr_to_id
from ..utils.print import error
from .utils import high_res_font_from_ingredient, get_page_number, COMPONENTS_TO_INCLUDE, NONE_FONT

def get_item_component(config: dict, ingredient: Union[dict, str], only_those_components: list[str] = [], count: int = 1) -> dict:
	"""Generate item hover text for a craft ingredient"""
	formatted: dict = {
		"text": NONE_FONT,
		"hover_event": create_hover_event("show_item", {"id": "","components": {}})
	}

	if isinstance(ingredient, dict) and ingredient.get("item"):
		formatted["hover_event"]["id"] = ingredient["item"]
	else:
		# Get item from database
		if isinstance(ingredient, str):
			id = ingredient
			item = config['database'][ingredient]
		else:
			custom_data: dict = ingredient["components"]["minecraft:custom_data"]
			id = ingr_to_id(ingredient, add_namespace=False)
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
		formatted["hover_event"]["id"] = item["id"].replace("minecraft:", "")
		components = {}
		if only_those_components:
			for key in only_those_components:
				if key in item:
					components[key] = item[key]
		else:
			for key, value in item.items():
				if key in COMPONENTS_TO_INCLUDE:
					components[key] = value
		formatted["hover_event"]["components"] = components

		# Add page number if from datapack
		page_number = get_page_number(id)
		if page_number != -1:
			formatted["click_event"] = create_click_event("change_page", page_number)
	
	# High resolution
	if config["manual_high_resolution"]:
		formatted["text"] = high_res_font_from_ingredient(config, ingredient, count)

	return formatted

