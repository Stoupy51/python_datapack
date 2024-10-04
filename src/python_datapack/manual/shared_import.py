
# Imports
from ..utils.print import *
from ..utils.io import *

# Utils functions for fonts (item start at 0x0000, pages at 0xa000)
# Return the character that will be used for font, ex: "\u0002" with i = 2
def get_font(i: int):
	i += 0x0020	# Minecraft only allow starting this value
	if i > 0xffff:
		error(f"Font index {i} is too big. Maximum is 0xffff.")
	return f"\\u{i:04x}"
def get_page_font(i: int) -> str:
	return get_font(i + 0x1000)
def get_next_font() -> str:	# Returns an incrementing value for each craft
	global next_craft_font
	next_craft_font += 1
	return get_font(next_craft_font)


# Constants
SQUARE_SIZE = 32
MANUAL_ASSETS_PATH = clean_path(os.path.dirname(os.path.realpath(__file__)) + "/")
TEMPLATES_PATH = MANUAL_ASSETS_PATH + "assets"
FONT_FILE = "manual"
BORDER_COLOR = 0xB64E2F
BORDER_COLOR = (BORDER_COLOR >> 16) & 0xFF, (BORDER_COLOR >> 8) & 0xFF, BORDER_COLOR & 0xFF, 255
BORDER_SIZE = 2
NONE_FONT = get_font(0x0000)
MEDIUM_NONE_FONT = get_font(0x0001)
SMALL_NONE_FONT = get_font(0x0002)
VERY_SMALL_NONE_FONT = get_font(0x0003)
MICRO_NONE_FONT = get_font(0x0004)
WIKI_NONE_FONT = get_font(0x0005)
WIKI_INFO_FONT = get_font(0x0006)
WIKI_RESULT_OF_CRAFT_FONT = get_font(0x0007)
WIKI_INGR_OF_CRAFT_FONT = get_font(0x0008)
SHAPED_2X2_FONT = get_font(0x0009)
SHAPED_3X3_FONT = get_font(0x000A)
FURNACE_FONT = get_font(0x000B)
HOVER_SHAPED_2X2_FONT = get_font(0x000C)
HOVER_SHAPED_3X3_FONT = get_font(0x000D)
HOVER_FURNACE_FONT = get_font(0x000E)
INVISIBLE_ITEM_FONT = get_font(0x000F)	# Invisible item to place
INVISIBLE_ITEM_WIDTH = INVISIBLE_ITEM_FONT + MICRO_NONE_FONT

HOVER_EQUIVALENTS: dict[str, str] = {
	SHAPED_2X2_FONT: HOVER_SHAPED_2X2_FONT,
	SHAPED_3X3_FONT: HOVER_SHAPED_3X3_FONT,
	FURNACE_FONT: HOVER_FURNACE_FONT,
}

# Global variables
next_craft_font = 0x8000
font_providers = []
manual_pages = []

# Get page number
def get_page_number(item_id: str) -> int:
	for p in manual_pages:
		if p["name"] == item_id:
			return p["number"]
	return -1

