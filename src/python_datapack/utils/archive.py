
# Imports
from .io import *
from .print import *
from zipfile import ZipFile, ZIP_DEFLATED
import time

# Function that make an archive but with efficiency using FILES_TO_WRITE variable
def make_archive(source: str, destination: str, copy_destinations: list[str] = []) -> float:
	""" Make an archive but with efficiency using FILES_TO_WRITE variable
	Args:
		source				(str):					The source folder to archive
		destination			(str):					The destination file
		copy_destinations	(list[str], optional):	The destination folders to copy the archive to. Defaults to [].
	Returns:
		float: The time taken to archive the source folder
	"""
	start_time: float = time.perf_counter()

	# Fix copy_destinations type if needed
	if copy_destinations and isinstance(copy_destinations, str):
		copy_destinations: list[str] = [copy_destinations]

	# Get all files that are not in FILES_TO_WRITE
	not_known_files: list[str] = []
	for root, _, files in os.walk(source):
		for file in files:
			file_path: str = os.path.join(root, file).replace("\\", "/")
			if file_path not in FILES_TO_WRITE:
				not_known_files.append(file_path)

	# Create the archive
	destination = destination if ".zip" in destination else destination + ".zip"
	with ZipFile(destination, "w", compression = ZIP_DEFLATED, compresslevel = 9) as zip:
		
		# Write every not known files
		for file in not_known_files:
			base_path: str = file.replace(source, "").strip("/")
			zip.write(file, base_path)
		
		# Write every known files
		for file in FILES_TO_WRITE:
			base_path: str = file.replace(source, "").strip("/")
			zip.writestr(base_path, FILES_TO_WRITE[file])
		
	# Copy the archive to the destination(s)
	for dest_folder in copy_destinations:
		try:
			if dest_folder.endswith("/"):
				file_name = destination.split("/")[-1]
				shutil.copy(destination, f"{dest_folder}/{file_name}")
			else:	# Else, it's not a folder but a file path
				shutil.copy(destination, dest_folder)
		except Exception as e:
			warning(f"Unable to copy '{destination}' to '{dest_folder}', reason: {e}")
	
	# Return the time taken to archive the source folder
	return time.perf_counter() - start_time

