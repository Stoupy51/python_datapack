
# Imports
from .io import *
from .print import *
from zipfile import ZipFile, ZIP_DEFLATED, ZipInfo
import time

# Function that makes an archive with consistency (same zip file each time)
def make_archive(source: str, destination: str, copy_destinations: list[str] = []) -> float:
	"""Make an archive with consistency using FILES_TO_WRITE variable"""
	start_time: float = time.perf_counter()

	# Fix copy_destinations type if needed
	if copy_destinations and isinstance(copy_destinations, str):
		copy_destinations = [copy_destinations]

	# Get all files that are not in FILES_TO_WRITE
	not_known_files: list[str] = []
	for root, _, files in os.walk(source):
		for file in files:
			file_path: str = clean_path(os.path.join(root, file))
			if file_path not in FILES_TO_WRITE:
				not_known_files.append(file_path)

	# Get the constant time for the archive
	constant_time: tuple[int, ...] = (2024, 1, 1, 0, 0, 0)	# default time: 2024-01-01 00:00:00
	for file in FILES_TO_WRITE:
		if file.endswith("pack.mcmeta"):

			# Get the pack folder (and the data and assets folders paths)
			pack_folder: str = os.path.dirname(file)
			data_folder: str = f"{pack_folder}/data"
			assets_folder: str = f"{pack_folder}/assets"

			# Get the time of the data or assets folder if it exists, else get the time of the pack.mcmeta file
			if os.path.exists(data_folder):
				time_float: float = os.path.getmtime(data_folder)
			elif os.path.exists(assets_folder):
				time_float: float = os.path.getmtime(assets_folder)
			else:
				time_float: float = os.path.getmtime(file)
			constant_time = time.localtime(time_float)[:6]
			break

	# Create the archive
	destination = destination if ".zip" in destination else destination + ".zip"
	with ZipFile(destination, "w", compression=ZIP_DEFLATED, compresslevel=9) as zip:

		# Write every not-known file with the fixed date/time
		for file in not_known_files:
			if source not in file:
				continue
			base_path: str = file.replace(source, "").strip("/")
			info = ZipInfo(base_path)
			info.compress_type = ZIP_DEFLATED
			info.date_time = constant_time
			with open(file, "rb") as f:
				zip.writestr(info, f.read())
		
		# Write every known file with the fixed date/time
		for file in FILES_TO_WRITE:
			if source not in file:
				continue
			base_path: str = file.replace(source, "").strip("/")
			info: ZipInfo = ZipInfo(base_path)
			info.compress_type = ZIP_DEFLATED
			info.date_time = constant_time
			zip.writestr(info, FILES_TO_WRITE[file])

	# Copy the archive to the destination(s)
	for dest_folder in copy_destinations:
		try:
			dest_folder = clean_path(dest_folder)
			if dest_folder.endswith("/"):
				file_name = destination.split("/")[-1]
				shutil.copy(clean_path(destination), f"{dest_folder}/{file_name}")
			else:	# Else, it's not a folder but a file path
				shutil.copy(clean_path(destination), dest_folder)
		except Exception as e:
			warning(f"Unable to copy '{clean_path(destination)}' to '{dest_folder}', reason: {e}")
	
	# Return the time taken to archive the source folder
	return time.perf_counter() - start_time

