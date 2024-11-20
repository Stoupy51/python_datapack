
# Imports
import os
import sys
import time
import traceback
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
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"

# Print functions
def current_time() -> str:
	return time.strftime("%H:%M:%S")

def info(*values: object, prefix: str = "", **print_kwargs) -> None:
	print(f"{prefix}{GREEN}[INFO  {current_time()}]", *values, RESET, **print_kwargs)

def debug(*values: object, prefix: str = "", **print_kwargs) -> None:
	print(f"{prefix}{BLUE}[DEBUG {current_time()}]", *values, RESET, **print_kwargs)

def suggestion(*values: object, prefix: str = "", **print_kwargs) -> None:
	print(f"{prefix}{CYAN}[SUGGESTION {current_time()}]", *values, RESET, **print_kwargs)

def progress(*values: object, prefix: str = "", **print_kwargs) -> None:
	print(f"{prefix}{MAGENTA}[PROGRESS {current_time()}]", *values, RESET, **print_kwargs)

def warning(*values: object, prefix: str = "", **print_kwargs) -> None:
	print(f"{prefix}{YELLOW}[WARNING {current_time()}]", *values, RESET, **print_kwargs)

def error(*values: object, exit: bool = True, prefix: str = "", **print_kwargs) -> None:
	""" Print an error message and optionally ask the user to continue or stop the program\n
	Args:
		values			(object):		Values to print (like the print function)
		exit			(bool):			Whether to ask the user to continue or stop the program, false to ignore the error automatically and continue
		print_kwargs	(dict):			Keyword arguments to pass to the print function
	"""
	print(f"{prefix}{RED}[ERROR {current_time()}]", *values, RESET, **print_kwargs)
	if exit:
		try:
			input("Press enter to ignore error and continue or 'CTRL+C' to stop the program... ")
		except KeyboardInterrupt:
			sys.exit(1)


# Execution time decorator
def measure_time(print_func: Callable = debug, message: str = "", perf_counter: bool = True) -> Callable:
	""" Decorator that will measure the execution time of a function\n
	Args:
		print_func	(Callable):	Function to use to print the execution time
		message		(str):		Message to display with the execution time (e.g. "Execution time of Something"), defaults to "Execution time of {func.__name__}"
		perf_counter	(bool):	Whether to use time.perf_counter_ns or time.time_ns
	"""
	ns: Callable = time.perf_counter_ns if perf_counter else time.time_ns
	def decorator(func: Callable) -> Callable:

		# Set the message if not specified
		nonlocal message
		if not message:
			message = f"Execution time of {func.__name__}"

		def wrapper(*args, **kwargs) -> object:

			# Measure the execution time (nanoseconds and seconds)
			start_ns: int = ns()
			result = func(*args, **kwargs)
			total_ns: int = ns() - start_ns
			total_ms: float = total_ns / 1_000_000
			total_s: float = total_ns / 1_000_000_000

			# Print the execution time (nanoseconds if less than 0.3s, seconds otherwise)
			if total_ms < 300:
				print_func(f"{message}: {total_ms:.3f}ms ({total_ns}ns)")
			elif total_s < 60:
				print_func(f"{message}: {(total_s):.5f}s")
			else:
				minutes: int = int(total_s) // 60
				seconds: int = int(total_s) % 60
				if minutes < 60:
					print_func(f"{message}: {minutes}m {seconds}s")
				else:
					hours: int = minutes // 60
					minutes: int = minutes % 60
					if hours < 24:
						print_func(f"{message}: {hours}h {minutes}m {seconds}s")
					else:
						days: int = hours // 24
						hours: int = hours % 24
						print_func(f"{message}: {days}d {hours}h {minutes}m {seconds}s")
			return result
		return wrapper
	return decorator


# Decorator that handle an error with different log levels
def handle_error(exceptions: tuple[type[Exception], ...] = (Exception,), message: str = "", error_log: int = 3) -> Callable:
	""" Decorator that handle an error with different log levels.\n
	Args:
		exceptions		(tuple[Exception]):	Exceptions to handle
		message			(str):				Message to display with the error. (e.g. "Error during something")
		error_log		(int):				Log level for the errors (0: None, 1: Show as warning, 2: Show as warning with traceback, 3: Show as error with traceback, 4: Raise exception)
	"""
	def decorator(func: Callable) -> Callable:
		if message != "":
			msg = f"{message}:\n"
		else:
			msg = message
			
		def wrapper(*args, **kwargs) -> object:
			try:
				return func(*args, **kwargs)
			except exceptions as e:
				if error_log == 1:
					warning(f"{msg}Error during {func.__name__}:\n {e}")
				elif error_log == 2:
					warning(f"{msg}Error during {func.__name__}:\n{traceback.format_exc()}")
				elif error_log == 3:
					error(f"{msg}Error during {func.__name__}:\n{traceback.format_exc()}", exit=True)
				else:
					raise e
		return wrapper
	return decorator

