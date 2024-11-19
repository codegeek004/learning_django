import requests
from pathlib import Path

#Purpose of this: This function takes a url, downloads the file using the request library and saves it locally at a specified path ensuring the parent directory for the file exists before saving.
#For example if the url = "https://cdn.jsdelivr.net/npm/flowbite.min.css"
#and out_path = Path("staticfiles/vendors/flowbite.min.css")
# in this case the function will first check if the directory 'staticfiles/vendors' exists.
# if it does not exist it will create both.
# it then fetches the file from the url and saves it as 'flowbite.min.css' in the specified directory


def download_to_local(url:str, out_path:Path, parent_mkdir:bool=True):
	if not isinstance(out_path, Path):
		raise ValueError(f"{out_path} must be valid pathlib Path object")
	#This means that wherever the parent directory is existing will end up being exiting 
	if parent_mkdir:
		out_path.parent.mkdir(parents=True, exists_ok=True)