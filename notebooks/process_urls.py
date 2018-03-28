import requests

def is_url_valid(url):
    response = requests.get(url)
    return_code = response.status_code
    if return_code == 200:
        return True
    else:
        return False

from github import Github

# g = Github(token)
# repo = g.get_repo(https://github.com/andreww/MSAT)

def check_github_licence_exists(repo):
    possible_filenames = ['LICENCE', 'COPYING','LICENSE']
    for content in repo.get_contents('/'):
        name = content.name
        for poss_name in possible_filenames:
            if poss_name in name.upper():
                return True
    return False


def validate_github(url,token):  
    git_url_path = (url.split('github.com/'))[1]    
    g = Github(token)                 
    repo = g.get_repo(git_url_path)
    check_github_licence_exists(repo)
    return 0
