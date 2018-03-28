import requests

def is_url_valid(url):
    response = requests.get(url)
    return_code = response.status_code
    if return_code == 200:
        return True
    else:
        return False
