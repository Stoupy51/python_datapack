
# Imports
from ..utils.io import *
from ..utils.print import *
from ..utils.cache import simple_cache
import json

def main(config: dict):

	# Prepare lang dictionnary and lang_format function
	lang = {}
	@simple_cache
	def lang_format(text: str) -> str:
		""" Get alphanumeric characters from a string and return it.
		Args:
			text (str): The text to format
		Returns:
			str: The formatted text
		"""
		to_underscore = ["\\n", ".", "/", ":"]
		for char in to_underscore:
			text = text.replace(char, "_")
		alpha_num = "".join(char for char in text if char.isalnum() or char in " _-").lower()
		for char in [' ', '-', "__"]:
			alpha_num = alpha_num.replace(char, "_")
		alpha_num = alpha_num[:64].strip("_").strip()
		if alpha_num.startswith(config['namespace']):
			return alpha_num
		else:
			return (config['namespace'] + "." + alpha_num)


	# For each file in FILES_TO_WRITE
	possibles_texts = ['"text":', '\\"text\\":', "'text':", "\\'text\\':"]
	no_backslashs = [x for x in possibles_texts if '\\' not in x]
	backslashs = [x for x in possibles_texts if '\\' in x]
	for file, content in FILES_TO_WRITE.items():

		# For each line while "text" is in line
		new_content = []
		for line in content.split("\n"):
			for p in possibles_texts:
				line = line.replace(p + " ", p)	# Remove space after "text":
			new_possibles_texts = [p for p in possibles_texts if p in line]
			line_progress = 0
			while any(possible_text in line[line_progress:] for possible_text in new_possibles_texts):
				for possible_text in new_possibles_texts.copy():	# Copy to be able to remove while looping
					if possible_text not in line[line_progress:]:
						new_possibles_texts.remove(possible_text)
						continue

					## Get the text
					splitted = line[line_progress:].split(possible_text)
					used_char = possible_text[-2]	# Get the char used for the text (") or (')
					text = used_char.join(splitted[1].split(used_char)[1:])	# Get the starting text

					# Get the end of the text
					text_end = 0
					for i, char in enumerate(text):
						try:
							if char == possible_text[-2]:
								if (possible_text in no_backslashs and text[i-1] != "\\"):		# "text":"..." &  'text':'...'
									text_end = i
									break
								elif (possible_text in backslashs and text[i-1] == "\\" and text[i-2] != "\\\\"):	# \"text\":\"...\" &  \'text\':\'...\'
									text_end = i - 1
									break
						except IndexError:
							pass

					# Get text position in the line
					text_position = line.find(text, line_progress)
					line_progress = text_position + 1	# Prevent checking all the way before
					text = text[:text_end]	# Get the text without the ending " (and the rest of the line)
					text_breaklines_replaced = text.replace("\\n", "\n").replace("\\","")	# Replace \n by a real new line
					if not any(char.isalnum() for char in text_breaklines_replaced):	# Skip if no alphanumeric character
						continue

					# If key for lang is too short or not alphanumeric, skip
					key_for_lang = lang_format(text_breaklines_replaced)
					verif = key_for_lang.replace(config['namespace'], "").replace(".", "").replace("_","")
					if len(verif) < 3 or not verif.isalnum() or "\\u" in text:
						continue

					# Get the lang format and add the key value to the dictionnary
					if key_for_lang not in lang.keys():
						lang[key_for_lang] = text_breaklines_replaced
					elif lang[key_for_lang] != text_breaklines_replaced:
						continue	# Skip if the key is already used for another text

					# Replace the text in the line by the lang format
					line = line[:text_position] + key_for_lang + line[text_position + len(text):]

					# Replace "text" by "translate"
					text_position -= len(possible_text)
					line = line[:text_position] + line[text_position:].replace("text", "translate", 1)
			new_content.append(line)
		
		# Write the new content to the file
		FILES_TO_WRITE[file] = "\n".join(new_content)


	# Write the lang file
	path = f"{config['build_resource_pack']}/assets/minecraft/lang/en_us.json"
	FILES_TO_WRITE[path] = json.dumps(lang, indent = '\t', ensure_ascii = True)
	debug(f"Lang file generated at '{path}'")

