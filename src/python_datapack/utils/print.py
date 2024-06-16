
# Imports
import time
import sys
import os

# Decorator that make a function silent
def silent(func):
	def wrapper(*args, **kwargs):

		# Disable stdout
		_original_stdout = sys.stdout
		sys.stdout = open(os.devnull, "w", encoding = "utf-8")

		# Call the function
		result = func(*args, **kwargs)

		# Re-Enable stdout
		sys.stdout.close()
		sys.stdout = _original_stdout 
		return result
	
	return wrapper

# Colors constants
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
def current_time() -> str:
	return time.strftime("%H:%M:%S")
def info(text: str = "") -> None:
	print(f"{GREEN}[INFO  {current_time()}] {text}{RESET}")
def debug(text: str = "") -> None:
	print(f"{BLUE}[DEBUG {current_time()}] {text}{RESET}")
def warning(text: str = "") -> None:
	print(f"{YELLOW}[WARNING {current_time()}] {text}{RESET}")
def error(text: str = "", exit: bool = True) -> None:
	print(f"{RED}[ERROR {current_time()}] {text}{RESET}")
	if exit:
		try:
			input("Press enter to ignore error and continue or 'CTRL+C' to stop the program... ")
		except KeyboardInterrupt:
			import sys
			sys.exit(1)

