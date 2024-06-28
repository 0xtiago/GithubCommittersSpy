import requests
import yaml
import csv
import argparse
from datetime import datetime, timedelta
from urllib.parse import urlparse
from termcolor import colored
import emoji


def display_ascii_art():
    title = "GH Committers Spy - by 0xtiago"
    
    ascii_art = r"""
    
 _____ _   _   _____                           _ _                  _____             
|  __ \ | | | /  __ \                         (_) |                /  ___|            
| |  \/ |_| | | /  \/ ___  _ __ ___  _ __ ___  _| |_ ___ _ __ ___  \ `--. _ __  _   _ 
| | __|  _  | | |    / _ \| '_ ` _ \| '_ ` _ \| | __/ _ \ '__/ __|  `--. \ '_ \| | | |
| |_\ \ | | | | \__/\ (_) | | | | | | | | | | | | ||  __/ |  \__ \ /\__/ / |_) | |_| |
 \____|_| |_/  \____/\___/|_| |_| |_|_| |_| |_|_|\__\___|_|  |___/ \____/| .__/ \__, |
                                                                         | |     __/ |
                                                                         |_|    |___/ 

    """

    colored_title = colored(title, 'cyan', attrs=['bold'])
    colored_art = colored(ascii_art, 'yellow')

    print(colored_title)
    print(colored_art)


config_file = 'config.yaml' #Configuration file
repos_file = 'repositories.txt' # Repositories to be analysed
output_file = 'results.csv' # Results of each reposutory
committers_file = 'committers.csv' # List of unique committers username and total number of commits

# Function to read configuration from YAML file
def read_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

#Read configuration from YAML file
config = read_config(config_file)
GITHUB_TOKEN = config['github_token']

# Headers for authentication in the GitHub API
headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }

# Function to read the repository adresses from the repository file.
def read_repos_from_file(file_path):
    with open(file_path, 'r') as file:
        repos = [convert_repo_url(line.strip()) for line in file if line.strip()]
    return repos


# Function to convert full repository URLs to "owner/repo" format
def convert_repo_url(repo):
    repo = remove_git_extension(repo)
    if repo.startswith("https://"):
        parsed_url = urlparse(repo)
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) >= 2:
            return f'{path_parts[0]}/{path_parts[1]}'
    return repo

# Remove .git extension from URLs, if they exist
def remove_git_extension(repo):
    if repo.endswith('.git'):
        return repo[:-4]
    return repo

# Function to get the default branch name of a repository
def get_default_branch(repo):
    url = f'https://api.github.com/repos/{repo}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repo_info = response.json()
        return repo_info.get('default_branch', 'main')
    return 'main'

# Function to get active contributors in the last X (-d) days on the main branch
def get_active_collaborators(repo, days):
    default_branch = get_default_branch(repo)
    since_date = (datetime.now() - timedelta(days=days)).isoformat() + 'Z'
    url = f'https://api.github.com/repos/{repo}/commits?sha={default_branch}&since={since_date}'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        error_message = f'Error accessing the repository {repo}: {response.status_code}'
        print(error_message)
        return {}, error_message
    
    commits = response.json()
    active_collaborators = {}
    
    for commit in commits:
        author = commit['author']
        if author is not None:
            author_name = author['login']
            if author_name in active_collaborators:
                active_collaborators[author_name] += 1
            else:
                active_collaborators[author_name] = 1
    
    return active_collaborators, 'Success'

# Function to write results to the CSV file
def write_results_to_csv(results, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Repository', 'Active Committers', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

# Function to write commits per user to a CSV file
def write_committers_to_csv(committers, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Number of Commits']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user, commits in committers.items():
            writer.writerow({'User': user, 'Number of Commits': commits})

# Main function
def main():
    display_ascii_art()
    parser = argparse.ArgumentParser(description='Verifies unique active contributors to GitHub repositories.')
    parser.add_argument('-d', '--days', type=int, required=True, help='Number of days to check employee activity.')
    args = parser.parse_args()
    
    days = args.days


    # Read repository list from file
    repos = read_repos_from_file(repos_file)
    total_repos = len(repos)

    # List to store results
    results = []

    # Dictionary to store commits per user
    all_committers = {}

    # Loop through the repositories and get the number of active contributors
    for i, repo in enumerate(repos, start=1):
        committers, status = get_active_collaborators(repo, days)
        num_active_collaborators = len(committers)
        results.append({
            'Repository': repo,
            'Active Committers': num_active_collaborators,
            'Status': status
        })

        # Display the number of active committers in the console
        print(f'{i}/{total_repos} Repository: {repo}, Active Committers: {num_active_collaborators}, Status: {status}')

        # Update committer dictionary
        for user, commits in committers.items():
            if user in all_committers:
                all_committers[user] += commits
            else:
                all_committers[user] = commits

    # Write results to CSV file
    write_results_to_csv(results, output_file)
    write_committers_to_csv(all_committers, committers_file)

    print(f'Results written to file {output_file}')
    print(f'Committers written to the file {committers_file}')
    # print(f'Total unique committers: {len(all_committers)}')
    colored_committers = colored(len(all_committers), 'green', attrs=['bold'])
    print(f'Total unique committers: {colored_committers}')

    print()
    colored_buymeacoffee = colored("https://buymeacoffee.com/tiagotavares", 'yellow', attrs=['bold'])
    print(f"{emoji.emojize(':handshake:')} If this tool helped you, how about inviting me for a coffee?? {colored_buymeacoffee} {emoji.emojize(':grinning_face:')}.")

if __name__ == '__main__':
    main()
