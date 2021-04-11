from pandas import read_csv    

def read_csv_from_github(repo_name='ManzcoinBot', git_file = 'manz_tranz_list.csv', repo_owner='tomdicato', branch='main'):

    repo_owner=str(repo_owner)
    repo_name = str(repo_name)
    branch = str(branch)
    git_file=str(git_file)    

    url = f"https://raw.githubusercontent.com/{ repo_owner }/{ repo_name }/{ branch }/{ git_file }"

    manz_tranz_existing=read_csv(url)

    return(manz_tranz_existing)

# read_csv_from_github(repo_name='ManzcoinBot', git_file = 'manz_tranz_list.csv', repo_owner='tomdicato', branch='main')