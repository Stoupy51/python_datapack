
# Imports
from ..utils.io import *
from ..utils.print import *
from ..utils.cache import simple_cache
import json

# Utility functions for finding text end
def find_text_end_no_backslash(text: str, used_char: str) -> int:
	text_end: int = 0
	while True:
		text_end = text.find(used_char, text_end + 1)
		if (text_end == -1) or (text[text_end - 1] != "\\"):		# "text":"..." &  'text':'...'
			return text_end
def find_text_end_backslash(text: str, used_char: str) -> int:
	text_end: int = 0
	while True:
		text_end = text.find(used_char, text_end + 1)
		if (text_end == -1):
			return text_end
		if (text[text_end - 1] == "\\" and text[text_end - 2] != "\\\\"):	# \"text\":\"...\" &  \'text\':\'...\'
			return text_end - 1

# Main function
def main(config: dict):
	start_time: float = time.perf_counter()

	# Prepare lang dictionnary and lang_format function
	lang = {}
	@simple_cache
	def lang_format(text: str) -> str:
		""" Get alphanumeric characters from a string and return it.
		Args:
			text (str): The text to format
		Returns:
			tuple[str,str]: The formatted text and a simplified version of it
		"""
		to_underscore: list[str] = ["\\n", ".", "/", ":"]
		for char in to_underscore:
			text = text.replace(char, "_")
		alpha_num: str = "".join(char for char in text if char.isalnum() or char in " _-").lower()
		for char in [' ', '-', "__"]:
			alpha_num = alpha_num.replace(char, "_")
		alpha_num = alpha_num[:64].strip("_").strip()
		if alpha_num.startswith(config['namespace']):
			return alpha_num, alpha_num.replace(".", "").replace("_","")
		else:
			return (config['namespace'] + "." + alpha_num), alpha_num.replace(".", "").replace("_","")

	# For each file in FILES_TO_WRITE
	POSSIBLES_TEXTS = ['"text":', '\\"text\\":', "'text':", "\\'text\\':"]
	NO_BACKSLASHS = [x for x in POSSIBLES_TEXTS if '\\' not in x]
	for file, content in FILES_TO_WRITE.items():

		# Some content adjustments
		for p in POSSIBLES_TEXTS:
			content = content.replace(p + " ", p)	# Remove space after "text":

		# For each possible text, while it is in content or we reached the end of the content,
		for possible_text in [p for p in POSSIBLES_TEXTS if p in content]:
			content_progress: int = 0
			used_char: str = possible_text[-2]	# Get the char used for the text (") or (')

			# Get function to find the end of the text
			find_text_end: function = find_text_end_no_backslash if possible_text in NO_BACKSLASHS else find_text_end_backslash

			while True:
				content_progress = content.find(possible_text, content_progress)
				if content_progress == -1:
					break

				## Get the text
				splitted: str = content[content_progress:].split(possible_text)[1]
				index: int = splitted.find(used_char)
				text: str = splitted[index+1:]	# Get the starting text

				# Get the end of the text
				text_end: int = find_text_end(text, used_char)

				# Get text position in the content
				text = text[:text_end]	# Get the text without the ending " (and the rest of the content)
				text_position: int = content.find(text, content_progress)
				content_progress = text_position	# Prevent checking all the way before

				# Replace \n by a real new line
				text_breaklines_replaced: str = text.replace("\\n", "\n").replace("\\","")
				if not any(char.isalnum() for char in text_breaklines_replaced):	# Skip if no alphanumeric character
					continue

				# If key for lang is too short or not alphanumeric, skip
				key_for_lang, verif = lang_format(text_breaklines_replaced)
				if len(verif) < 3 or not verif.isalnum() or "\\u" in text:
					continue

				# Get the lang format and add the key value to the dictionnary
				if key_for_lang not in lang:
					lang[key_for_lang] = text_breaklines_replaced
				elif lang[key_for_lang] != text_breaklines_replaced:
					continue	# Skip if the key is already used for another text

				# Replace the text in the content by the lang format
				content = content[:text_position] + key_for_lang + content[text_position + len(text):]

				# Replace "text" by "translate"
				text_position -= len(possible_text)
				content = content[:text_position] + content[text_position:].replace("text", "translate", 1)
		
		# Write the new content to the file
		FILES_TO_WRITE[file] = content

	# Write the lang file
	path: str = f"{config['build_resource_pack']}/assets/minecraft/lang/en_us.json"
	FILES_TO_WRITE[path] = json.dumps(lang, indent = '\t', ensure_ascii = True)
	end_time: float = time.perf_counter()
	info(f"Lang file generated at '{path}' in {end_time - start_time:.5f}s")

