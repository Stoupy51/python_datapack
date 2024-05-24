
import os
from multiprocessing import Pool

# Easy multiprocessing functions
def parallelized_thread(function: callable, args: dict|tuple|list):
	""" Function runned for each thread
	Args:
		function	(callable):	The function to call
		args		(dict):		The args to pass to the function
	Returns:
		Any: The return of the function
	"""
	if isinstance(args, dict):
		return function(**args)
	elif isinstance(args, (tuple, list)):
		return function(*args)
	else:
		return function(args)

def chunk_thread(args):
	return parallelized_thread(*args)

def parallelize(processes: list[tuple[callable, dict|tuple|list]], nb_workers: int = os.cpu_count()):
	""" Parallelize the function
	Args:
		processes	(list[tuple[callable, dict]):	A list of tuples containing the function and the args to pass to it
			ex: [(my_func, {"path": "uwu"}), (my_func, {"path": "uwu2})]
			ex: [(my_func, ("uwu")), (my_func, ("uwu2"))]
	Returns:
		list[Any]: The return of the function for each process
	"""
	with Pool(processes = min(nb_workers, len(processes))) as pool:
		return pool.map(chunk_thread, processes)

