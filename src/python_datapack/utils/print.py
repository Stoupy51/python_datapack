
# Imports
import os
import sys
import time
import traceback
from typing import Callable
from functools import wraps

# Decorator that make a function silent (disable stdout)
def silent(func: Callable, mute_stderr: bool = False):
	""" Decorator that make a function silent (disable stdout, and stderr if specified)\n
	Args:
		func			(Callable):		Function to make silent
		mute_stderr		(bool):			Whether to mute stderr or not
	"""
	@wraps(func)
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
RESET: str   = "\033[0m"
RED: str     = "\033[91m"
GREEN: str   = "\033[92m"
YELLOW: str  = "\033[93m"
BLUE: str    = "\033[94m"
MAGENTA: str = "\033[95m"
CYAN: str    = "\033[96m"
LINE_UP: str = "\033[1A"

# Print functions
previous_args_kwards: tuple = (None, None)
nb_values: int = 0

def is_same_print(*args, **kwargs) -> bool:
	""" Checks if the current print call is the same as the previous one.\n
	Args:
		args (tuple): The arguments passed to the print function.
		kwargs (dict): The keyword arguments passed to the print function.
	Returns:
		bool: True if the current print call is the same as the previous one, False otherwise.
	"""
	global previous_args_kwards, nb_values
	if previous_args_kwards == (args, kwargs):
		nb_values += 1
		return True
	else:
		previous_args_kwards = (args, kwargs)
		nb_values = 0
		return False

def current_time() -> str:
	""" Get the current time in the format HH:MM:SS	"""
	return time.strftime("%H:%M:%S")

def info(*values, prefix: str = "", **print_kwargs) -> None:
	""" Print an information message looking like "[INFO HH:MM:SS] message"\n
	Args:
		values			(object):	Values to print (like the print function)
		prefix			(str):		Prefix to add to the values
		print_kwargs	(dict):		Keyword arguments to pass to the print function
	"""
	if not is_same_print(*values, **print_kwargs):
		print(f"{prefix}{GREEN}[INFO  {current_time()}]", *values, RESET, **print_kwargs)
	else:
		print(f"{LINE_UP}{prefix}{GREEN}[INFO  {current_time()}] (x{nb_values})", *values, RESET, **print_kwargs)

def debug(*values, prefix: str = "", **print_kwargs) -> None:
	""" Print a debug message looking like "[DEBUG HH:MM:SS] message"\n
	Args:
		values			(object):		Values to print (like the print function)
		prefix			(str):		Prefix to add to the values
		print_kwargs	(dict):		Keyword arguments to pass to the print function
	"""
	if not is_same_print(*values, **print_kwargs):
		print(f"{prefix}{BLUE}[DEBUG {current_time()}]", *values, RESET, **print_kwargs)
	else:
		print(f"{LINE_UP}{prefix}{BLUE}[DEBUG {current_time()}] (x{nb_values})", *values, RESET, **print_kwargs)

def suggestion(*values, prefix: str = "", **print_kwargs) -> None:
	""" Print a suggestion message looking like "[SUGGESTION HH:MM:SS] message"\n
	Args:
		values			(object):		Values to print (like the print function)
		prefix			(str):		Prefix to add to the values
		print_kwargs	(dict):		Keyword arguments to pass to the print function
	"""
	if not is_same_print(*values, **print_kwargs):
		print(f"{prefix}{CYAN}[SUGGESTION {current_time()}]", *values, RESET, **print_kwargs)
	else:
		print(f"{LINE_UP}{prefix}{CYAN}[SUGGESTION {current_time()}] (x{nb_values})", *values, RESET, **print_kwargs)

def progress(*values, prefix: str = "", **print_kwargs) -> None:
	""" Print a progress message looking like "[PROGRESS HH:MM:SS] message"\n
	Args:
		values			(object):		Values to print (like the print function)
		prefix			(str):		Prefix to add to the values
		print_kwargs	(dict):		Keyword arguments to pass to the print function
	"""
	if not is_same_print(*values, **print_kwargs):
		print(f"{prefix}{MAGENTA}[PROGRESS {current_time()}]", *values, RESET, **print_kwargs)
	else:
		print(f"{LINE_UP}{prefix}{MAGENTA}[PROGRESS {current_time()}] (x{nb_values})", *values, RESET, **print_kwargs)

def warning(*values, prefix: str = "", **print_kwargs) -> None:
	""" Print a warning message looking like "[WARNING HH:MM:SS] message"\n
	Args:
		values			(object):		Values to print (like the print function)
		prefix			(str):		Prefix to add to the values
		print_kwargs	(dict):		Keyword arguments to pass to the print function
	"""
	if not is_same_print(*values, **print_kwargs):
		print(f"{prefix}{YELLOW}[WARNING {current_time()}]", *values, RESET, **print_kwargs)
	else:
		print(f"{LINE_UP}{prefix}{YELLOW}[WARNING {current_time()}] (x{nb_values})", *values, RESET, **print_kwargs)

def error(*values, exit: bool = True, prefix: str = "", **print_kwargs) -> None:
	""" Print an error message and optionally ask the user to continue or stop the program\n
	Args:
		values			(object):		Values to print (like the print function)
		exit			(bool):			Whether to ask the user to continue or stop the program, false to ignore the error automatically and continue
		print_kwargs	(dict):			Keyword arguments to pass to the print function
	"""
	if not is_same_print(*values, **print_kwargs):
		print(f"{prefix}{RED}[ERROR {current_time()}]", *values, RESET, **print_kwargs)
	else:
		print(f"{LINE_UP}{prefix}{RED}[ERROR {current_time()}] (x{nb_values})", *values, RESET, **print_kwargs)
	if exit:
		try:
			input("Press enter to ignore error and continue or 'CTRL+C' to stop the program... ")
		except KeyboardInterrupt:
			sys.exit(1)

def whatisit(*values, print_function: Callable = debug, prefix: str = "") -> None:
	""" Print the type of each value and the value itself\n
	Args:
		values			(object):		Values to print
		print_function	(Callable):	Function to use to print the values
		prefix			(str):		Prefix to add to the values
	"""
	if len(values) > 1:
		print_function("(What is it?)", prefix=prefix)
		for value in values:
			print_function(f"{type(value)}:\t{value}", prefix=prefix)
	elif len(values) == 1:
		print_function(f"(What is it?) {type(values[0])}:\t{values[0]}", prefix=prefix)


# Execution time decorator
def measure_time(print_func: Callable = debug, message: str = "", perf_counter: bool = True) -> Callable:
	""" Decorator that will measure the execution time of a function\n
	Args:
		print_func		(Callable):	Function to use to print the execution time
		message			(str):		Message to display with the execution time (e.g. "Execution time of Something"), defaults to "Execution time of {func.__name__}"
		perf_counter	(bool):		Whether to use time.perf_counter_ns or time.time_ns
	Returns:
		Callable:	Decorator to measure the time of the function.
	"""
	ns: Callable = time.perf_counter_ns if perf_counter else time.time_ns
	def decorator(func: Callable) -> Callable:

		# Set the message if not specified
		nonlocal message
		if not message:
			message = f"Execution time of {func.__name__}"

		@wraps(func)
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
class LOG_LEVELS:
	NONE = 0
	WARNING = 1
	WARNING_TRACEBACK = 2
	ERROR_TRACEBACK = 3
	RAISE_EXCEPTION = 4

def handle_error(exceptions: tuple[type[Exception], ...]|type[Exception] = (Exception,), message: str = "", error_log: int = LOG_LEVELS.ERROR_TRACEBACK) -> Callable:
	""" Decorator that handle an error with different log levels.\n
	Args:
		exceptions		(tuple[type[Exception]], ...):	Exceptions to handle
		message			(str):							Message to display with the error. (e.g. "Error during something")
		error_log		(int):							Log level for the errors (0: None, 1: Show as warning, 2: Show as warning with traceback, 3: Show as error with traceback, 4: Raise exception)
	"""
	# Convert the exceptions to a tuple if not already
	if not isinstance(exceptions, tuple):
		exceptions = (exceptions,)

	def decorator(func: Callable) -> Callable:
		if message != "":
			msg: str = f"{message}, "
		else:
			msg: str = message

		@wraps(func)
		def wrapper(*args, **kwargs) -> object:
			try:
				return func(*args, **kwargs)
			except exceptions as e:
				if error_log == LOG_LEVELS.WARNING:
					warning(f"{msg}Error during {func.__name__}: ({type(e).__name__}) {e}")
				elif error_log == LOG_LEVELS.WARNING_TRACEBACK:
					warning(f"{msg}Error during {func.__name__}:\n{traceback.format_exc()}")
				elif error_log == LOG_LEVELS.ERROR_TRACEBACK:
					error(f"{msg}Error during {func.__name__}:\n{traceback.format_exc()}", exit=True)
				else:
					raise e
		return wrapper
	return decorator


if __name__ == "__main__":
	info("Hello", "World")
	time.sleep(1)
	info("Hello", "World")
	time.sleep(1)
	info("Hello", "World")
	time.sleep(1)
	info("Hello", "World")
	time.sleep(1)
	info("Hello", "World")
	time.sleep(1)
	info("Hello", "World")

