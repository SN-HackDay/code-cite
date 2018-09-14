import requests

def check_zenodo_licence_exists(url):
    response = requests.get(url)
    content = response.text
    if 'license' in content:
        return True
    return False
