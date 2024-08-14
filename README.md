![Github Commiters Spy](assets/images/gh_committers_spy.gif](https://res.cloudinary.com/dtr6hzxnx/image/upload/v1723639841/blog/GithubCommittersSpy_-_tiagotavares.io_cbx4rt.png)
# Github Committers Spy

This script enumerates active committers in specified GitHub repositories over a given number of days. It fetches the data using the GitHub API and outputs the results to CSV files.

The objective behind this project was to facilitate the survey of the real number of users who collaborate in the Github repositories of important company projects, and thus be able to price SAST and SCA licenses with greater accuracy.

- [Github Committers Spy](#github-committers-spy)
  - [Special Thanks to supporters and contributors](#special-thanks-to-supporters-and-contributors)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [Notes](#notes)
  - [References](#references)
  - [Support](#support)

## Special thanks to supporters and contributors
- Michelle Mesquita - https://github.com/michelleamesquita
- Murillo Rocha - https://github.com/6drocha
- Tiago "Kid" Machado - https://github.com/gar0t0


## Features

- Fetch active committers from specified GitHub repositories.
- Retrieve commit data from the main branch within a specified number of days.
- Output results to CSV files, including detailed commit counts per user.

## Requirements

- Python 3.x
- `requests` library
- `pyyaml` library
- `termcolor` library
- `emoji` library

## Installation

1. Clone the repository or download the script files.
2. Install the required Python libraries:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Create a `config.yaml` file with the following content and replace `your_github_token` with your GitHub personal access token:
    ```yaml
    github_token: "your_github_token"
    ```

2. Create a `repositories.txt` file and add the repositories you want to analyze, one per line, in the format `owner/repo` or `https://github.com/owner/repo`.

## Usage

Run the script with the desired number of days to check for active committers using the `-d` flag:

```sh
python gh_committers_spy.py -d 90
````

Receiving the number of collaborators in default branch in the last 90 days.

![alt text](assets/images/gh_committers_spy.gif)

## Notes
- Ensure you have a valid GitHub personal access token with appropriate permissions to access the repositories.
- The script checks commits on the default branch of each repository.
- If a repository URL is provided, it will be converted to the format owner/repo.


## References
- [GitHub REST API v3](https://docs.github.com/en/rest)
- [Requests: HTTP for Humans](https://requests.readthedocs.io/en/latest/)
- [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Checkmarx One Cloud Licence Types and Restrictions](https://checkmarx.com/legal/cxone-cloud-license-types-and-restrictions/v2022-07/) 
- [Veracode - Understanding the license consumption reports ](https://docs.veracode.com/r/c_license_consumption)

## Support

☕ If this tool helped you, how about inviting me for a coffee?? 😄

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/tiagotavares)

