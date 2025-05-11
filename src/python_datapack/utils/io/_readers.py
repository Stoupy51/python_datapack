
# Imports
from .general import path_to_file_path
from .read import read_file


def read_function(config: dict, path: str) -> str:
	""" Read the content of the function at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the function (ex: "namespace:folder/function_name")
	Returns:
		str:    The content of the function
	"""
	return read_file(path_to_file_path(config, path, "function"))


def read_advancement(config: dict, path: str) -> str:
	""" Read the content of the advancement at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the advancement (ex: "namespace:folder/advancement_name")
	Returns:
		str:    The content of the advancement
	"""
	return read_file(path_to_file_path(config, path, "advancement"))


def read_predicate(config: dict, path: str) -> str:
	""" Read the content of the predicate at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the predicate (ex: "namespace:folder/predicate_name")
	Returns:
		str:    The content of the predicate
	"""
	return read_file(path_to_file_path(config, path, "predicate"))


def read_tags(config: dict, path: str) -> str:
	""" Read the content of the tags at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the tags (ex: "namespace:folder/tags_name")
	Returns:
		str:    The content of the tags
	"""
	return read_file(path_to_file_path(config, path, "tags"))


def read_item_modifier(config: dict, path: str) -> str:
	""" Read the content of the item modifier at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the item modifier (ex: "namespace:folder/item_modifier_name")
	Returns:
		str:    The content of the item modifier
	"""
	return read_file(path_to_file_path(config, path, "item_modifier"))


def read_recipe(config: dict, path: str) -> str:
	""" Read the content of the recipe at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the recipe (ex: "namespace:folder/recipe_name")
	Returns:
		str:    The content of the recipe
	"""
	return read_file(path_to_file_path(config, path, "recipe"))


def read_loot_table(config: dict, path: str) -> str:
	""" Read the content of the loot table at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the loot table (ex: "namespace:folder/loot_table_name")
	Returns:
		str:    The content of the loot table
	"""
	return read_file(path_to_file_path(config, path, "loot_table"))


def read_structure(config: dict, path: str) -> str:
	""" Read the content of the structure at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the structure (ex: "namespace:folder/structure_name")
	Returns:
		str:    The content of the structure
	"""
	return read_file(path_to_file_path(config, path, "structure"))


def read_damage_type(config: dict, path: str) -> str:
	""" Read the content of the damage type at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the damage type (ex: "namespace:folder/damage_type_name")
	Returns:
		str:    The content of the damage type
	"""
	return read_file(path_to_file_path(config, path, "damage_type"))


def read_chat_type(config: dict, path: str) -> str:
	""" Read the content of the chat type at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the chat type (ex: "namespace:folder/chat_type_name")
	Returns:
		str:    The content of the chat type
	"""
	return read_file(path_to_file_path(config, path, "chat_type"))


def read_banner_pattern(config: dict, path: str) -> str:
	""" Read the content of the banner pattern at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the banner pattern (ex: "namespace:folder/banner_pattern_name")
	Returns:
		str:    The content of the banner pattern
	"""
	return read_file(path_to_file_path(config, path, "banner_pattern"))


def read_wolf_variant(config: dict, path: str) -> str:
	""" Read the content of the wolf variant at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the wolf variant (ex: "namespace:folder/wolf_variant_name")
	Returns:
		str:    The content of the wolf variant
	"""
	return read_file(path_to_file_path(config, path, "wolf_variant"))


def read_enchantment(config: dict, path: str) -> str:
	""" Read the content of the enchantment at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the enchantment (ex: "namespace:folder/enchantment_name")
	Returns:
		str:    The content of the enchantment
	"""
	return read_file(path_to_file_path(config, path, "enchantment"))


def read_enchantment_provider(config: dict, path: str) -> str:
	""" Read the content of the enchantment provider at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the enchantment provider (ex: "namespace:folder/enchantment_provider_name")
	Returns:
		str:    The content of the enchantment provider
	"""
	return read_file(path_to_file_path(config, path, "enchantment_provider"))


def read_jukebox_song(config: dict, path: str) -> str:
	""" Read the content of the jukebox song at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the jukebox song (ex: "namespace:folder/jukebox_song_name")
	Returns:
		str:    The content of the jukebox song
	"""
	return read_file(path_to_file_path(config, path, "jukebox_song"))


def read_painting_variant(config: dict, path: str) -> str:
	""" Read the content of the painting variant at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the painting variant (ex: "namespace:folder/painting_variant_name")
	Returns:
		str:    The content of the painting variant
	"""
	return read_file(path_to_file_path(config, path, "painting_variant"))


def read_instrument(config: dict, path: str) -> str:
	""" Read the content of the instrument at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the instrument (ex: "namespace:folder/instrument_name")
	Returns:
		str:    The content of the instrument
	"""
	return read_file(path_to_file_path(config, path, "instrument"))


def read_trial_spawner(config: dict, path: str) -> str:
	""" Read the content of the trial spawner at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the trial spawner (ex: "namespace:folder/trial_spawner_name")
	Returns:
		str:    The content of the trial spawner
	"""
	return read_file(path_to_file_path(config, path, "trial_spawner"))


def read_trim_pattern(config: dict, path: str) -> str:
	""" Read the content of the trim pattern at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the trim pattern (ex: "namespace:folder/trim_pattern_name")
	Returns:
		str:    The content of the trim pattern
	"""
	return read_file(path_to_file_path(config, path, "trim_pattern"))


def read_trim_material(config: dict, path: str) -> str:
	""" Read the content of the trim material at the given path.
	
	Args:
		config     (dict):    The main configuration
		path       (str):     The path to the trim material (ex: "namespace:folder/trim_material_name")
	Returns:
		str:    The content of the trim material
	"""
	return read_file(path_to_file_path(config, path, "trim_material"))

