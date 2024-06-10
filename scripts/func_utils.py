def get_prs_url(owner: str, name: str):
    return (f'https://api.github.com/repos/{owner}/{name}/pulls')