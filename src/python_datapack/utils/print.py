
# Imports
import time
import sys
import os
from typing import Callable

# Decorator that make a function silent (disable stdout)
def silent(func: Callable, mute_stderr: bool = False):
	""" Decorator that make a function silent (disable stdout, and stderr if specified)\n
	Args:
		func			(Callable):		Function to make silent
		mute_stderr		(bool):			Whether to mute stderr or not
	"""
	def wrapper(*args, **kwargs):

		# Disable stdout and stderr
		_original_stdout = sys.stdout
		sys.stdout = open(os.devnull, "w", encoding="utf-8")
		if mute_stderr:
			_original_stderr = sys.stderr
			sys.stderr = open(os.devnull, "w", encoding="utf-8")

		# Call the function
		result = func(*args, **kwargs)

		# Re-Enable stdout and stderr
		sys.stdout.close()
		sys.stdout = _original_stdout
		if mute_stderr:
			sys.stderr.close()
			sys.stderr = _original_stderr
		return result
	
	return wrapper

# Colors constants
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# Print functions
def current_time() -> str:
	return time.strftime("%H:%M:%S")

def info(*values: object, **print_kwargs: dict):
	print(f"{GREEN}[INFO  {current_time()}]", *values, RESET, **print_kwargs)

def debug(*values: object, **print_kwargs: dict):
	print(f"{BLUE}[DEBUG {current_time()}]", *values, RESET, **print_kwargs)

def warning(*values: object, **print_kwargs: dict):
	print(f"{YELLOW}[WARNING {current_time()}]", *values, RESET, **print_kwargs)

def error(*values: object, exit: bool = True, **print_kwargs: dict) -> None:
	""" Print an error message and optionally ask the user to continue or stop the program\n
	Args:
		values			(object):		Values to print (like the print function)
		exit			(bool):			Whether to ask the user to continue or stop the program, false to ignore the error automatically and continue
		print_kwargs	(dict):			Keyword arguments to pass to the print function
	"""
	print(f"{RED}[ERROR {current_time()}]", *values, RESET, **print_kwargs)
	if exit:
		try:
			input("Press enter to ignore error and continue or 'CTRL+C' to stop the program... ")
		except KeyboardInterrupt:
			import sys
			sys.exit(1)

