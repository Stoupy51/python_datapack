
# Imports
from src.python_datapack.continuous_delivery import load_credentials, upload_to_github

# Get credentials
credentials: dict = load_credentials("~/python_datapack/credentials.yml")

# Upload to GitHub
from upgrade import current_version
github_config: dict = {
	"project_name": "python_datapack",
	"version": current_version,
	"build_folder": "",
}
changelog: str = upload_to_github(credentials, github_config)

