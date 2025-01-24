"""
Handles image manipulation utilities for the manual
"""
from PIL import Image
from typing import Any, Tuple

def careful_resize(image: Image.Image, max_result_size: int) -> Image.Image:
	"""Resize an image while keeping the aspect ratio"""
	if image.size[0] >= image.size[1]:
		factor = max_result_size / image.size[0]
		return image.resize((max_result_size, int(image.size[1] * factor)), Image.Resampling.NEAREST)
	else:
		factor = max_result_size / image.size[1]
		return image.resize((int(image.size[0] * factor), max_result_size), Image.Resampling.NEAREST)

def add_border(image: Image.Image, border_color: Tuple[int, int, int, int], border_size: int, is_rectangle_shape: bool) -> Image.Image:
	"""Add a border to every part of the image"""
	image = image.convert("RGBA")
	pixels: Any = image.load()

	if not is_rectangle_shape:
		pixels_to_change = [(x, y) for x in range(image.width) for y in range(image.height) if pixels[x, y][3] == 0]
		r = range(-border_size, border_size + 1)
		for x, y in pixels_to_change:
			try:
				if any(pixels[x + dx, y + dy][3] != 0 and pixels[x + dx, y + dy] != border_color for dx in r for dy in r):
					pixels[x, y] = border_color
			except:
				pass
	else:
		height, width = 8, 8
		while height < image.height and pixels[8, height][3]!= 0:
			height += 1
		while width < image.width and pixels[width, 8][3]!= 0:
			width += 1
		
		border = Image.new("RGBA", (width + 2, height + 2), border_color)
		border.paste(image, (0, 0), image)
		image.paste(border, (0, 0), border)
	
	return image

