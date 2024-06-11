
# Imports
from .io import *
from .print import *
from ..dependencies.main import OFFICIAL_LIBS, OFFICIAL_LIBS_PATH
from smithed.weld.toolchain.cli import weld
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

# Weld datapack
@silent
def weld_datapack(config: dict, dest_path: str) -> None:
	""" Merge the datapack and libs into one file using Weld
	Args:
		dest_path (str): The path to the destination file
	"""
	# Get all paths to merge
	datapacks_to_merge = [
		f"{config['build_folder']}/{config['datapack_name']}_datapack.zip",
		config['libs_folder'] + "/datapack/*",
	]

	# Add the used official libs
	for lib in OFFICIAL_LIBS.values():
		if lib["is_used"]:
			name: str = lib["name"]
			path: str = f"{OFFICIAL_LIBS_PATH}/datapack/{name}.zip"
			if os.path.exists(path):
				datapacks_to_merge.append(path)

	# Weld all datapacks
	output_dir = os.path.dirname(dest_path)
	output = os.path.basename(dest_path.replace(".zip", ".temp.zip"))
	weld(datapacks_to_merge, Path(output_dir), Path(output), log = "error")

	# Make the new zip file with fixes pack.mcmeta and pack.png
	with ZipFile(dest_path.replace(".zip",".temp.zip"), "r") as temp_zip:
		with ZipFile(dest_path, "w", compression = ZIP_DEFLATED) as zip:
			for file in temp_zip.namelist():
				if file not in ["pack.mcmeta", "pack.png"]:
					zip.writestr(file, temp_zip.read(file))
			zip.write(f"{config['build_datapack']}/pack.mcmeta", "pack.mcmeta")
			if os.path.exists(f"{config['build_datapack']}/pack.png"):
				zip.write(f"{config['build_datapack']}/pack.png", "pack.png")
	
	# Remove temp file
	os.remove(dest_path.replace(".zip",".temp.zip"))

# Weld resource pack
@silent
def weld_resource_pack(config: dict, dest_path: str) -> None:
	""" Merge the resource pack and libs into one file using Weld
	Args:
		dest_path (str): The path to the destination file
	"""
	# Get all paths to merge
	resource_packs_to_merge = [
		f"{config['build_folder']}/{config['datapack_name']}_resource_pack.zip",
		config['libs_folder'] + "/resource_pack/*",
	]

	# Add the used official libs
	for lib in OFFICIAL_LIBS.values():
		if lib["is_used"]:
			name: str = lib["name"]
			path: str = f"{OFFICIAL_LIBS_PATH}/resource_pack/{name}.zip"
			if os.path.exists(path):
				resource_packs_to_merge.append(path)
	
	# Weld all resource packs
	output_dir = os.path.dirname(dest_path)
	output = os.path.basename(dest_path.replace(".zip", ".temp.zip"))
	weld(resource_packs_to_merge, Path(output_dir), Path(output), log = "error")

	# Make the new zip file with fixes pack.mcmeta and pack.png
	with ZipFile(dest_path.replace(".zip",".temp.zip"), "r") as temp_zip:
		with ZipFile(dest_path, "w", compression = ZIP_DEFLATED) as zip:
			for file in temp_zip.namelist():
				if file not in ["pack.mcmeta", "pack.png"]:
					zip.writestr(file, temp_zip.read(file))
			zip.write(f"{config['build_resource_pack']}/pack.mcmeta", "pack.mcmeta")
			if os.path.exists(f"{config['build_resource_pack']}/pack.png"):
				zip.write(f"{config['build_resource_pack']}/pack.png", "pack.png")
	
	# Remove temp file
	os.remove(dest_path.replace(".zip",".temp.zip"))

