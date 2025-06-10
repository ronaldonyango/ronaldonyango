import os
import json
import requests
from slugify import slugify

def get_kaggle_stats():
    """Fetch Kaggle dataset statistics and output for GitHub Actions."""
    datasets = [
        {"slug": "ronaldonyango/global-suicide-rates-1990-to-2022", "name": "Global Suicide Rates"},
        # Add more datasets here
    ]
    
    stats = {}
    
    # Check for Kaggle API token
    api_token = os.getenv('KAGGLE_API_TOKEN')
    if not api_token:
        print("Warning: KAGGLE_API_TOKEN not found. Using placeholder values.")
        for dataset in datasets:
            name_key = slugify(dataset['name'])
            stats[f"{name_key}-views"] = "N/A"
            stats[f"{name_key}-downloads"] = "N/A"
        write_github_output(stats)
        return stats
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    for dataset in datasets:
        name_key = slugify(dataset['name'])
        try:
            url = f"https://www.kaggle.com/api/v1/datasets/view/{dataset['slug']}"
            print(f"Fetching stats for: {dataset['name']}")
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            views = data.get('totalViews', 0)
            downloads = data.get('totalDownloads', 0)
            
            stats[f"{name_key}-views"] = views
            stats[f"{name_key}-downloads"] = downloads
            
            print(f"✓ {dataset['name']}: {views} views, {downloads} downloads")
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Network error for {dataset['name']}: {str(e)}")
            stats[f"{name_key}-views"] = "N/A"
            stats[f"{name_key}-downloads"] = "N/A"
        except json.JSONDecodeError as e:
            print(f"✗ JSON parsing error for {dataset['name']}: {str(e)}")
            stats[f"{name_key}-views"] = "N/A"
            stats[f"{name_key}-downloads"] = "N/A"
        except Exception as e:
            print(f"✗ Unexpected error for {dataset['name']}: {str(e)}")
            stats[f"{name_key}-views"] = "N/A"
            stats[f"{name_key}-downloads"] = "N/A"
    
    write_github_output(stats)
    return stats

def write_github_output(stats):
    """Write stats to GitHub Actions output."""
    github_output = os.getenv('GITHUB_OUTPUT')
    if not github_output:
        print("Warning: GITHUB_OUTPUT environment variable not set")
        print(f"Stats would be: {json.dumps(stats, indent=2)}")
        return
    
    try:
        with open(github_output, 'a', encoding='utf-8') as f:
            # Use proper GitHub Actions output format
            stats_json = json.dumps(stats)
            f.write(f"stats={stats_json}\n")
        print(f"✓ Stats written to GitHub Actions output")
    except Exception as e:
        print(f"✗ Error writing to GitHub output: {str(e)}")

def update_readme():
    """Update README with stats from environment variable."""
    # Handle the case where STATS might be null/empty
    stats_env = os.getenv('STATS', '{}')
    if not stats_env or stats_env.lower() == 'null':
        print("Warning: STATS environment variable is null or empty, using empty dict")
        stats = {}
    else:
        try:
            stats = json.loads(stats_env)
        except json.JSONDecodeError as e:
            print(f"Error parsing STATS JSON: {str(e)}")
            print(f"STATS content: '{stats_env}'")
            stats = {}
    
    print(f"Loaded stats: {json.dumps(stats, indent=2)}")
    
    # Read README template
    readme_path = 'README.md'
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found")
        return
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace placeholders with actual stats
        # Example replacements - adjust based on your README template
        for key, value in stats.items():
            placeholder = f"{{{{ {key} }}}}"
            content = content.replace(placeholder, str(value))
        
        # Write updated README
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ README updated successfully")
        
    except Exception as e:
        print(f"✗ Error updating README: {str(e)}")

if __name__ == "__main__":
    # Check if we're getting stats or updating README
    if os.getenv('STATS') is not None:
        print("=== Updating README ===")
        update_readme()
    else:
        print("=== Fetching Kaggle Stats ===")
        get_kaggle_stats()