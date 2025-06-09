import re
import json
import os

def update_readme():
    # Load stats from GitHub Actions outputs
    stats = json.loads(os.getenv('STATS', '{}'))
    
    with open('README.md', 'r') as f:
        content = f.read()
    
    # Update each dataset's badges
    for stat_key in stats:
        if stat_key.endswith('-views'):
            name = stat_key.replace('-views', '')
            pattern = rf'\[!\[{name} Views\]\(https:\/\/img\.shields\.io\/badge\/Views-\d+-blue\)\]'
            replacement = f'[![{name} Views](https://img.shields.io/badge/Views-{stats[stat_key]}-blue)]'
            content = re.sub(pattern, replacement, content)
        
        elif stat_key.endswith('-downloads'):
            name = stat_key.replace('-downloads', '')
            pattern = rf'\[!\[{name} Downloads\]\(https:\/\/img\.shields\.io\/badge\/Downloads-\d+-brightgreen\)\]'
            replacement = f'[![{name} Downloads](https://img.shields.io/badge/Downloads-{stats[stat_key]}-brightgreen)]'
            content = re.sub(pattern, replacement, content)
    
    # Write updated content
    with open('README.md', 'w') as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()