
# Imports
from typing import BinaryIO
from ..utils.print import *
from ..constants import MINECRAFT_VERSION
from .cd_utils import *

# Constants
MODRINTH_API_URL: str = "https://api.modrinth.com/v2"
PROJECT_ENDPOINT: str = f"{MODRINTH_API_URL}/project"
VERSION_ENDPOINT: str = f"{MODRINTH_API_URL}/version"

@measure_time(progress, "Uploading to modrinth took")
@handle_error(error_log=3)
def upload_to_modrinth(credentials: dict[str, str], modrinth_config: dict[str, str], changelog: str = "") -> None:
	""" Upload the project to Modrinth using the credentials and the configuration\n
	Args:
		credentials		(dict[str, str]): Credentials for the Modrinth API
		modrinth_config	(dict[str, str]): Configuration for the Modrinth project
		changelog		(str): Changelog text for the release
	"""
	# Get the API key
	if "modrinth_api_key" not in credentials:
		raise ValueError("The credentials file must contain a 'modrinth_api_key' key, which is a PAT (Personal Access Token) for the Modrinth API: https://modrinth.com/settings/pats")
	api_key: str = credentials["modrinth_api_key"]
	headers: dict[str, str] = {"Authorization": api_key}

	# Verify configuration
	if "project_name" not in modrinth_config:
		raise ValueError("The modrinth_config file must contain a 'project_name' key, which is the name of the project on Modrinth")
	if "version" not in modrinth_config:
		raise ValueError("The modrinth_config file must contain a 'version' key, which is the version of the project")
	if "slug" not in modrinth_config:
		raise ValueError("The modrinth_config file must contain a 'namespace' key, which is the namespace of the project")
	if "summary" not in modrinth_config:
		raise ValueError("The modrinth_config file must contain a 'summary' key, which is the summary of the project")
	if "description_markdown" not in modrinth_config:
		raise ValueError("The modrinth_config file must contain a 'description_markdown' key, which is the description of the project in Markdown format")
	if "version_type" not in modrinth_config:
		raise ValueError("The modrinth_config file must contain a 'version_type' key, which is the version type of the project (release, beta, alpha)")
	if "build_folder" not in modrinth_config:
		raise ValueError("The modrinth_config file must contain a 'build_folder' key, which is the folder containing the build of the project (datapack and resourcepack zip files)")
	project_name: str = modrinth_config["project_name"]
	version: str = modrinth_config["version"]
	slug: str = modrinth_config["slug"]
	summary: str = modrinth_config["summary"]
	description_markdown: str = modrinth_config["description_markdown"]
	version_type: str = modrinth_config["version_type"]
	build_folder: str = modrinth_config["build_folder"]

	# Search for the project on Modrinth to check if it exists
	search_response = requests.get(f"{PROJECT_ENDPOINT}/{slug}", headers=headers)
	handle_response(search_response, f"Project not found on Modrinth, with namespace {slug}, please create it manually on https://modrinth.com/")
	project: dict = search_response.json()

	# Update the description and the summary
	update_response = requests.patch(f"{PROJECT_ENDPOINT}/{slug}", headers=headers, json={"body": description_markdown.strip(), "description": summary.strip()})
	handle_response(update_response, "Failed to update project description")

	# Check if the current version already exists
	version_response = requests.get(f"{PROJECT_ENDPOINT}/{slug}/version/{version}", headers=headers)
	if version_response.status_code == 200:
		warning(f"Version {version} already exists on Modrinth, do you want to delete it? (y/N)")
		if input().lower() != "y":
			return
		version_id: str = version_response.json()["id"]
		delete_response = requests.delete(f"{VERSION_ENDPOINT}/{version_id}", headers=headers)
		handle_response(delete_response, "Failed to delete the version")
	elif version_response.status_code == 404:
		info(f"Version {version} not found on Modrinth, uploading...")
	else:
		handle_response(version_response, "Failed to check if the version already exists")

	# Get the file parts
	file_parts: list[str] = [
		f"{build_folder}/{project_name}_datapack_with_libs.zip",
		f"{build_folder}/{project_name}_resource_pack_with_libs.zip"
	]
	file_parts = [file_part for file_part in file_parts if os.path.exists(file_part)]
	if len(file_parts) == 0:
		raise ValueError(f"No file parts (datapack and resourcepack zip files) found in {build_folder}, please check the build_folder path in the modrinth_config file")

	# Upload the version
	files: dict[str, bytes] = {}
	for file_part in file_parts:
		with open(file_part, "rb") as file:
			files[os.path.basename(file_part)] = file.read()
		
	request_data: dict = {
		"name": f"{project_name} [v{version}]",
		"version_number": version,
		"changelog": changelog,
		"dependencies": modrinth_config.get("dependencies", []),
		"game_versions": [MINECRAFT_VERSION],
		"version_type": version_type,
		"loaders": ["datapack"],
		"featured": False,
		"status": "listed",
		"project_id": project["id"],
		"file_parts": [os.path.basename(file_part) for file_part in file_parts],
		"primary_file": os.path.basename(file_parts[0])
	}

	upload_response = requests.post(
		VERSION_ENDPOINT,
		headers=headers,
		data={
			"data": json.dumps(request_data)
		},
		files=files,
		timeout=10,
		stream=False
	)
	json_response: dict = upload_response.json()
	handle_response(upload_response, "Failed to upload the version")
	debug(json.dumps(json_response, indent='\t'))

	# Get the hashes of the resource pack (if any)
	if len(file_parts) > 1:
		resource_pack_hash: str = json_response["files"][1]["hashes"]["sha1"]
		version_id: str = json_response["id"]
		version_response = requests.patch(
			f"{VERSION_ENDPOINT}/{version_id}",
			headers=headers,
			json={"file_types": [{"algorithm": "sha1", "hash": resource_pack_hash, "file_type": "required-resource-pack"}]}
		)
		handle_response(version_response, "Failed to put the resource pack as required")

	info(f"Project {project_name} updated on Modrinth!")

