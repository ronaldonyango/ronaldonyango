import os
import json
import re

def format_number(num):
    """Format number with comma separators for readability."""
    if isinstance(num, (int, float)) and num >= 1000:
        return f"{num:,}"
    return str(num)

def update_readme():
    """Update README with stats from environment variable."""
    print("📝 Starting README update...")
    
    # Handle the case where STATS might be null/empty
    stats_env = os.getenv('STATS', '{}')
    if not stats_env or stats_env.lower() in ['null', 'none', '']:
        print("⚠️  STATS environment variable is null or empty, using defaults")
        stats = {}
    else:
        try:
            stats = json.loads(stats_env)
            print(f"✅ Loaded stats: {json.dumps(stats, indent=2)}")
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing STATS JSON: {str(e)}")
            print(f"STATS content: '{stats_env}'")
            stats = {}
    
    # Read README
    readme_path = 'README.md'
    if not os.path.exists(readme_path):
        print(f"❌ {readme_path} not found")
        return
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update badge values based on your README structure
        # Pattern: ![Badge Name](https://img.shields.io/badge/Label-VALUE-color)
        
        # Global Suicide Rates Views
        views = stats.get('global-suicide-rates-views', 0)
        formatted_views = format_number(views)
        content = re.sub(
            r'(https://img\.shields\.io/badge/Views-)\d+(-blue)',
            f'\\g<1>{formatted_views}\\g<2>',
            content
        )
        
        # Global Suicide Rates Downloads  
        downloads = stats.get('global-suicide-rates-downloads', 0)
        formatted_downloads = format_number(downloads)
        content = re.sub(
            r'(https://img\.shields\.io/badge/Downloads-)\d+(-brightgreen)',
            f'\\g<1>{formatted_downloads}\\g<2>',
            content
        )
        
        # Check if any changes were made
        if content == original_content:
            print("ℹ️  No changes needed in README")
            return
        
        # Write updated README
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ README updated successfully")
        print(f"📊 Updated stats:")
        print(f"  • Views: {formatted_views}")
        print(f"  • Downloads: {formatted_downloads}")
        
    except Exception as e:
        print(f"❌ Error updating README: {str(e)}")
        raise

if __name__ == "__main__":
    update_readme()