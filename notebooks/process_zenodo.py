import urllib2

def check_zenodo_licence_exists(url):
    response = urllib2.urlopen(url)
    content = response.read()
    if 'license' in content:
        return True
    return False
