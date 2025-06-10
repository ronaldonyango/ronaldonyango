"""
Kaggle Dataset Statistics Fetcher and README Updater
Uses persistent HTML comment placeholders that never get replaced permanently.
"""

import os
import json
import requests
import base64
import re
import sys
from slugify import slugify
from typing import Dict, List, Any, Optional


class KaggleStatsFetcher:
    """Handles fetching statistics from Kaggle datasets."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Kaggle-Stats-Bot/2.0 (GitHub Actions)'
        })
        
        # Dataset configuration
        self.datasets = [
            {
                "owner": "ronaldonyango", 
                "dataset": "global-suicide-rates-1990-to-2022", 
                "name": "Global Suicide Rates"
            },
        ]
    
    def setup_authentication(self) -> bool:
        """Setup authentication headers for Kaggle API."""
        username = "ronaldonyango"
        key = "2de8425e0d512dc8e0a62aad37a8183e"
        
        if not username or not key:
            print("❌ Missing KAGGLE_USERNAME or KAGGLE_KEY environment variables")
            return False
        
        # Create basic auth header
        credentials = base64.b64encode(f"{username}:{key}".encode()).decode()
        self.session.headers['Authorization'] = f"Basic {credentials}"
        
        print(f"✅ Authentication configured for user: {username}")
        return True
    
    def fetch_dataset_stats_api(self, owner: str, dataset: str) -> Optional[Dict[str, int]]:
        """Fetch dataset statistics using official Kaggle API."""
        endpoints = [
            f"https://www.kaggle.com/api/v1/datasets/view/{owner}/{dataset}",
            f"https://www.kaggle.com/api/v1/datasets/list?user={owner}",
        ]
        
        for endpoint in endpoints:
            try:
                print(f"   Trying API endpoint: {endpoint}")
                response = self.session.get(endpoint, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'list' in endpoint:
                        # Find specific dataset in user's list
                        target_ref = f"{owner}/{dataset}"
                        for ds in data:
                            if ds.get('ref') == target_ref:
                                return {
                                    'views': ds.get('totalViews', 0),
                                    'downloads': ds.get('totalDownloads', 0)
                                }
                    else:
                        # Direct dataset endpoint
                        return {
                            'views': data.get('totalViews', data.get('viewCount', 0)),
                            'downloads': data.get('totalDownloads', data.get('downloadCount', 0))
                        }
                
                else:
                    print(f"   API returned {response.status_code}: {response.text[:100]}...")
                    
            except Exception as e:
                print(f"   API error: {str(e)}")
                continue
        
        return None
    
    def fetch_dataset_stats_scraping(self, owner: str, dataset: str) -> Optional[Dict[str, int]]:
        """Fallback method using web scraping."""
        try:
            url = f"https://www.kaggle.com/datasets/{owner}/{dataset}"
            print(f"   Trying web scraping: {url}")
            
            # Use different headers for scraping
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code != 200:
                print(f"   Scraping failed: {response.status_code}")
                return None
            
            html = response.text
            
            # Enhanced regex patterns for finding stats
            patterns = {
                'views': [
                    r'"viewCount["\']?\s*:\s*(\d+)',
                    r'"totalViews["\']?\s*:\s*(\d+)',
                    r'viewCount["\']?\s*:\s*(\d+)',
                    r'(\d+)\s*(?:total\s+)?views?',
                    r'Viewed\s+(\d+)\s+times',
                ],
                'downloads': [
                    r'"downloadCount["\']?\s*:\s*(\d+)',
                    r'"totalDownloads["\']?\s*:\s*(\d+)',
                    r'downloadCount["\']?\s*:\s*(\d+)',
                    r'(\d+)\s*(?:total\s+)?downloads?',
                    r'Downloaded\s+(\d+)\s+times',
                ]
            }
            
            stats = {'views': 0, 'downloads': 0}
            
            for stat_type, pattern_list in patterns.items():
                for pattern in pattern_list:
                    matches = re.findall(pattern, html, re.IGNORECASE)
                    if matches:
                        # Take the largest number found (likely the most accurate)
                        stats[stat_type] = max(int(match) for match in matches if match.isdigit())
                        break
            
            if stats['views'] > 0 or stats['downloads'] > 0:
                return stats
            
        except Exception as e:
            print(f"   Scraping error: {str(e)}")
        
        return None
    
    def fetch_all_stats(self) -> Dict[str, Any]:
        """Fetch statistics for all configured datasets."""
        print("🔍 Starting Kaggle stats collection...")
        
        if not self.setup_authentication():
            print("⚠️  Proceeding without authentication (limited functionality)")
        
        all_stats = {}
        
        for dataset_config in self.datasets:
            name = dataset_config['name']
            owner = dataset_config['owner']
            dataset = dataset_config['dataset']
            name_key = slugify(name)
            
            print(f"\n📊 Fetching stats for: {name}")
            print(f"    Dataset: {owner}/{dataset}")
            
            # Try API first, then scraping
            stats = None
            
            if 'Authorization' in self.session.headers:
                stats = self.fetch_dataset_stats_api(owner, dataset)
            
            if not stats:
                print("   API failed, trying web scraping...")
                stats = self.fetch_dataset_stats_scraping(owner, dataset)
            
            if stats:
                all_stats[f"{name_key}-views"] = stats['views']
                all_stats[f"{name_key}-downloads"] = stats['downloads']
                print(f"✅ Success: {stats['views']:,} views, {stats['downloads']:,} downloads")
            else:
                all_stats[f"{name_key}-views"] = 0
                all_stats[f"{name_key}-downloads"] = 0
                print("❌ Failed to fetch stats")
        
        return all_stats


class ReadmeUpdater:
    """Handles updating README with persistent HTML comment placeholders."""
    
    def __init__(self, readme_path: str = 'README.md'):
        self.readme_path = readme_path
    
    def update_readme(self, stats: Dict[str, Any]) -> bool:
        """Update README file using persistent HTML comment placeholders."""
        if not os.path.exists(self.readme_path):
            print(f"❌ README file not found: {self.readme_path}")
            return False
        
        try:
            # Read current README
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            replacements_made = 0
            
            # Look for HTML comment placeholder patterns
            # Format: <!-- STATS:key -->value<!-- /STATS:key -->
            for key, value in stats.items():
                formatted_value = f"{value:,}"
                
                # Pattern to match: <!-- STATS:key -->old_value<!-- /STATS:key -->
                pattern = r'<!-- STATS:' + re.escape(key) + r' -->(\d{1,3}(?:,\d{3})*|\d+)<!-- /STATS:' + re.escape(key) + r' -->'
                replacement = f'<!-- STATS:{key} -->{formatted_value}<!-- /STATS:{key} -->'
                
                new_content = re.sub(pattern, replacement, content)
                if new_content != content:
                    content = new_content
                    replacements_made += 1
                    print(f"✅ Updated {key}: {formatted_value}")
            
            # If no persistent placeholders found, look for traditional placeholders and convert them
            if replacements_made == 0:
                print("🔍 No persistent placeholders found, looking for traditional placeholders...")
                
                for key, value in stats.items():
                    formatted_value = f"{value:,}"
                    
                    # Look for traditional {{ key }} placeholders
                    traditional_placeholder = f"{{{{ {key} }}}}"
                    
                    if traditional_placeholder in content:
                        # Replace with persistent format
                        persistent_replacement = f"<!-- STATS:{key} -->{formatted_value}<!-- /STATS:{key} -->"
                        content = content.replace(traditional_placeholder, persistent_replacement)
                        replacements_made += 1
                        print(f"✅ Converted traditional placeholder {key} to persistent format: {formatted_value}")
            
            if replacements_made == 0:
                print("⚠️  No placeholders found in README")
                print("💡 To use this script, your README should contain either:")
                print(f"   - Persistent: <!-- STATS:global-suicide-rates-views -->0<!-- /STATS:global-suicide-rates-views -->")
                print(f"   - Traditional: {{{{ global-suicide-rates-views }}}}")
                print("\n📝 Example README format:")
                print("```markdown")
                print("## Kaggle Datasets")
                print("### Global Suicide Rates (1990-2022)")
                print("[![Views](https://img.shields.io/badge/Views-<!-- STATS:global-suicide-rates-views -->0<!-- /STATS:global-suicide-rates-views -->-blue)]()")
                print("[![Downloads](https://img.shields.io/badge/Downloads-<!-- STATS:global-suicide-rates-downloads -->0<!-- /STATS:global-suicide-rates-downloads -->-brightgreen)]()")
                print("```")
                return False
            
            # Write updated README
            with open(self.readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ README updated successfully ({replacements_made} replacements)")
            return True
            
        except Exception as e:
            print(f"❌ Error updating README: {str(e)}")
            return False


def write_github_output(stats: Dict[str, Any]) -> None:
    """Write statistics to GitHub Actions output."""
    github_output = os.getenv('GITHUB_OUTPUT')
    
    if not github_output:
        print("ℹ️  GITHUB_OUTPUT environment variable not set")
        print(f"Stats: {json.dumps(stats, indent=2)}")
        return
    
    try:
        with open(github_output, 'a', encoding='utf-8') as f:
            stats_json = json.dumps(stats)
            f.write(f"stats={stats_json}\n")
        print("✅ Stats written to GitHub Actions output")
    except Exception as e:
        print(f"❌ Error writing to GitHub output: {str(e)}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("🚀 KAGGLE STATS UPDATER (PERSISTENT HTML COMMENTS)")
    print("=" * 60)
    
    stats_env = os.getenv('STATS')
    
    if stats_env is not None:
        print("📝 README UPDATE MODE")
        print("-" * 30)
        
        try:
            if stats_env.lower() in ['null', '']:
                stats = {}
            else:
                stats = json.loads(stats_env)
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing STATS JSON: {str(e)}")
            print(f"STATS content: '{stats_env}'")
            sys.exit(1)
        
        print("📊 Loaded stats:")
        for key, value in stats.items():
            print(f"   - {key}: {value:,}")
        
        updater = ReadmeUpdater()
        success = updater.update_readme(stats)
        
        if not success:
            print("❌ README update failed")
            sys.exit(1)
        else:
            print("✅ README update completed successfully")
    
    else:
        print("🔍 STATS FETCHING MODE")
        print("-" * 30)
        
        fetcher = KaggleStatsFetcher()
        stats = fetcher.fetch_all_stats()
        
        print(f"\n📈 Final Stats Summary:")
        print("-" * 30)
        for key, value in stats.items():
            print(f"   {key}: {value:,}" if isinstance(value, int) else f"   {key}: {value}")
        
        write_github_output(stats)
    
    print("=" * 60)


if __name__ == "__main__":
    main()
