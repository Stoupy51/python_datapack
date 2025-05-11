
# Imports
import stouputils as stp

from ._writers import write_advancement, write_function
from .write import write_file, write_versioned_function


# Deprecated functions
@stp.deprecated(message="This function has been renamed to write_to_versioned_function(), please update your code")
def write_to_versioned_file(*args, **kwargs):
	return write_versioned_function(*args, **kwargs)

@stp.deprecated(message="This function has been renamed to write_file(), please update your code")
def write_to_file(*args, **kwargs):
	return write_file(*args, **kwargs)

@stp.deprecated(message="This function has been renamed to write_function(), please update your code")
def write_to_function(*args, **kwargs):
	return write_function(*args, **kwargs)

@stp.deprecated(message="This function has been renamed to write_advancement(), please update your code")
def write_to_advancement(*args, **kwargs):
	return write_advancement(*args, **kwargs)

