
# Imports
import os
import pyperclip
import stouputils as stp

# Constants
MARKDOWN_TO_BBCODE_URL: list[str] = ["https://ricolovefeng.github.io/"]

# Configuration
def validate_config(pmc_config: dict[str, str]) -> tuple[str, str]:
	""" Validate PlanetMinecraft configuration

	Args:
		pmc_config (dict[str, str]): Configuration for the PlanetMinecraft project
	Returns:
		str: Project url on PlanetMinecraft
	"""
	required_keys = ["project_url", "version"]
	error_messages = {
		"project_url": "url of the project on PlanetMinecraft",
		"version": "version of the project",
	}
	
	for key in required_keys:
		if key not in pmc_config:
			raise ValueError(f"The pmc_config dictionary must contain a '{key}' key, which is the {error_messages[key]}")
	
	return (
		pmc_config["project_url"],
		pmc_config["version"]
	)

def upload_version(project_url: str, version: str, changelog: str) -> None:
	""" Upload new version by opening the project url with the browser

	Args:
		project_url		(str):	Url of the project on PlanetMinecraft to open
		version			(str):	Version number
		changelog		(str):	Changelog text
	"""
	# Open the project url in the browser
	os.system(f"start {project_url}")

	# Copy the changelog text to the clipboard
	pyperclip.copy(changelog)
	stp.info("Changelog text copied to the clipboard!")

	# Wait for the user to know if the upload is successful
	stp.progress("Press Enter if you have uploaded the new version")
	input()


@stp.measure_time(stp.progress, "Uploading to PlanetMinecraft took")
@stp.handle_error()
def upload_to_pmc(pmc_config: dict, changelog: str = "") -> None:
	""" Upload the project to PlanetMinecraft using the configuration

	Disclaimer:
		There is no API for PlanetMinecraft, so everything is done manually.
	Args:
		pmc_config		(dict):		Configuration for the PlanetMinecraft project
		changelog		(str):		Changelog text for the release
	"""
	project_url, version = validate_config(pmc_config)
	stp.suggestion(f"We suggest you updating your project description by using one of the following url (to convert markdown to bbcode): {MARKDOWN_TO_BBCODE_URL}")
	upload_version(project_url, version, changelog)

