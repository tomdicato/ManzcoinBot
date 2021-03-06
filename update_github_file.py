#Import required packages
from github import Github
import requests
import os 

gh_access_token=os.environ.get('MANZCOIN_GITHUB_TOKEN')

def updatefilefromgithub(gh_access_token, new_tweets, repo_name='ManzcoinBot', git_file = 'manz_tranz_list.csv', repo_owner='tomdicato', branch='main',message="more tests"):

    g = Github(gh_access_token)
    repo_owner=str(repo_owner)
    repo_name = str(repo_name)
    branch = str(branch)
    git_file=str(git_file)
    message=str(message)

    repo = g.get_user().get_repo(repo_name)

    contents = repo.get_contents(git_file)

    url = f"https://raw.githubusercontent.com/{ repo_owner }/{ repo_name }/{ branch }/{ git_file }"

    download = requests.get(url)

    open('manz_tranznew.csv', 'wb').write(download.content)

    new_tweets[['transaction_id','timestamp']].to_csv('manz_tranznew.csv', mode='a', index=False, header=False)

    with open('manz_tranznew.csv') as f:
        s = f.read()

    repo = g.get_user().get_repo(repo_name)
    contents = repo.get_contents('manz_tranz_list.csv')    

    repo.update_file(contents.path, message=message, content=s, sha=contents.sha, branch=branch)