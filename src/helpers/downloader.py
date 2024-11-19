import requests
from pathlib import Path


def download_to_local(url:str, out_path:Path, parent_mkdir:bool=True):
	if not isinstance(out_path, Path):
		raise ValueError(f"{out_path} must be valid pathlib Path object")
	if parent_mkdir:
		out_path.parent.mkdir(parents=True, exists_ok=True)
#Purpose of this: This function takes a url, downloads the file using the request library and saves it locally at a specified path ensuring the parent directory for the file exists before saving.
#For example if the url = "https://cdn.jsdelivr.net/npm/flowbite.min.css"
#and out_path = Path("staticfiles/vendors/flowbite.min.css")
# in this case the function will first check if the directory 'staticfiles/vendors' exists.
# if it does not exist it will create both.
# it then fetches the file from the url and saves it as 'flowbite.min.css' in the specified directory. It is not necessary that
#every file content will be stored in flowbite.min.css. It will save wherver the path is defined to save the html content

	try:
		#sends http get request to the url to fetch the file.
		response = requests.get(url)
		#it checks if the request is successful or not using the status code.
		response.raise_for_status()
		#writes the binary data to specified file path. It avoids issues newline conversions
		out_path.write_bytes(response.content)
		return True
	except requests.RequestException as e:
		print(f"Failed to download {url}:{e}")
		return False
