
# Imports
from .utils import *

# Page optimizer
def optimize_array(page_content: list) -> list:
	""" Optimize the page content by associating compounds when possible
	Args:
		page_content (list): The page content
	Returns:
		list: The optimized page content
	"""
	# For each compound
	new_page_content = []
	for i, compound in enumerate(page_content):
		if isinstance(compound, list):
			new_page_content.append(optimize_array(compound))
		elif i == 0:
			if isinstance(compound, dict):
				new_page_content.append(compound.copy())
			else:
				new_page_content.append(compound)
		else:
			# For checks
			compound_without_text = compound.copy() if isinstance(compound, dict) else compound
			previous_without_text = new_page_content[-1].copy() if isinstance(new_page_content[-1], dict) else new_page_content[-1]
			if isinstance(compound, dict) and isinstance(new_page_content[-1], dict):
				compound_without_text.pop("text", None)
				previous_without_text.pop("text", None)

			# If the previous compound is the same as the current one, merge the text
			if str(compound_without_text) == str(previous_without_text):

				# If the previous compound is a text, merge the text
				if isinstance(new_page_content[-1], str):
					new_page_content[-1] += str(compound)

				# If the previous compound is a dict, merge the dict
				elif isinstance(new_page_content[-1], dict):
					new_page_content[-1]["text"] += compound["text"]
			
			# Always add break lines to the previous part
			elif compound == "\n":
				if isinstance(new_page_content[-1], str):
					new_page_content[-1] += "\n"
				elif isinstance(new_page_content[-1], dict):
					new_page_content[-1]["text"] += "\n"
			
			# Always merge two strings
			elif isinstance(compound, str) and isinstance(new_page_content[-1], str):
				new_page_content[-1] += compound
			
			# DISABLED, REASON: You may not want that invisible items shows up for mouse cursor
			# # Merge the compound if the previous compound is a dict of the same font and the current one is a small none font (that is always at the very left)
			# elif isinstance(compound, str) and isinstance(new_page_content[-1], dict) and not new_page_content[-1].get("font") and compound == SMALL_NONE_FONT:
			# 	new_page_content[-1]["text"] += compound
			
			# Otherwise, just add the compound
			else:
				if isinstance(compound, dict):
					new_page_content.append(compound.copy())
				else:
					new_page_content.append(compound)
	
	# Return
	return new_page_content

# Function
def optimize_book(book_content: list) -> list:
	""" Optimize the book content by associating compounds when possible
	Args:
		book_content (list): The book content
	Returns:
		list: The optimized book content
	"""
	# For each page
	new_book_content = []
	for page in book_content:
		if isinstance(page, list):
			new_book_content.append(optimize_array(page))
		else:
			new_book_content.append(page)

	# Return
	return new_book_content




