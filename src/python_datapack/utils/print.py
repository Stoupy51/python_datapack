
import time

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

