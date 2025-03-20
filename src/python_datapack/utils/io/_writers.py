
# Imports
from .write import write_file
from .general import path_to_file_path


def write_function(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the function at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the function (ex: "namespace:folder/function_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "function"), content, overwrite, prepend)


def write_advancement(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the advancement at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the advancement (ex: "namespace:folder/advancement_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "advancement"), content, overwrite, prepend)


def write_predicate(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the predicate at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the predicate (ex: "namespace:folder/predicate_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "predicate"), content, overwrite, prepend)


def write_tags(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the tags at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the tags (ex: "namespace:folder/tags_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "tags"), content, overwrite, prepend)


def write_item_modifier(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the item modifier at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the item modifier (ex: "namespace:folder/item_modifier_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "item_modifier"), content, overwrite, prepend)


def write_recipe(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the recipe at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the recipe (ex: "namespace:folder/recipe_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "recipe"), content, overwrite, prepend)


def write_loot_table(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the loot table at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the loot table (ex: "namespace:folder/loot_table_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "loot_table"), content, overwrite, prepend)


def write_structure(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the structure at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the structure (ex: "namespace:folder/structure_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "structure"), content, overwrite, prepend)


def write_damage_type(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the damage type at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the damage type (ex: "namespace:folder/damage_type_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "damage_type"), content, overwrite, prepend)


def write_chat_type(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the chat type at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the chat type (ex: "namespace:folder/chat_type_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "chat_type"), content, overwrite, prepend)


def write_banner_pattern(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the banner pattern at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the banner pattern (ex: "namespace:folder/banner_pattern_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "banner_pattern"), content, overwrite, prepend)


def write_wolf_variant(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the wolf variant at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the wolf variant (ex: "namespace:folder/wolf_variant_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "wolf_variant"), content, overwrite, prepend)


def write_enchantment(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the enchantment at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the enchantment (ex: "namespace:folder/enchantment_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "enchantment"), content, overwrite, prepend)


def write_enchantment_provider(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the enchantment provider at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the enchantment provider (ex: "namespace:folder/enchantment_provider_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "enchantment_provider"), content, overwrite, prepend)


def write_jukebox_song(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the jukebox song at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the jukebox song (ex: "namespace:folder/jukebox_song_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "jukebox_song"), content, overwrite, prepend)


def write_painting_variant(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the painting variant at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the painting variant (ex: "namespace:folder/painting_variant_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "painting_variant"), content, overwrite, prepend)


def write_instrument(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the instrument at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the instrument (ex: "namespace:folder/instrument_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "instrument"), content, overwrite, prepend)


def write_trial_spawner(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the trial spawner at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the trial spawner (ex: "namespace:folder/trial_spawner_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "trial_spawner"), content, overwrite, prepend)


def write_trim_pattern(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the trim pattern at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the trim pattern (ex: "namespace:folder/trim_pattern_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "trim_pattern"), content, overwrite, prepend)


def write_trim_material(config: dict, path: str, content: str, overwrite: bool = False, prepend: bool = False) -> None:
	""" Write the content to the trim material at the given path.

	Args:
		config          (dict): The main configuration 
		path            (str):  The path to the trim material (ex: "namespace:folder/trim_material_name")
		content         (str):  The content to write
		overwrite       (bool): If the file should be overwritten (default: Append the content)
		prepend         (bool): If the content should be prepended instead of appended (not used if overwrite is True)
	"""
	write_file(path_to_file_path(config, path, "trim_material"), content, overwrite, prepend)

