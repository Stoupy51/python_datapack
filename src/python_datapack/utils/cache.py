
# Imports
from typing import Callable

# Easy cache function
def simple_cache(func: Callable):

	# Create the cache dict
	cache_dict = {}

	# Create the wrapper
	def wrapper(*args, **kwargs):

		# Create the hashed key
		hashed = str(args) + str(kwargs)

		# If the key is in the cache, return it
		if hashed in cache_dict:
			return cache_dict[hashed]

		# Else, call the function and add the result to the cache
		else:
			result = func(*args, **kwargs)
			cache_dict[hashed] = result
			return result
	
	# Return the wrapper
	return wrapper

