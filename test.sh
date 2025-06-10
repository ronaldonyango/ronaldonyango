# Install dependencies locally
pip install -r requirements.txt

# Set up Kaggle API token (get from https://www.kaggle.com/settings)
export KAGGLE_API_TOKEN="2de8425e0d512dc8e0a62aad37a8183e"

# Test the stats script
python scripts/update_kaggle_stats.py

# Verify outputs (should print dataset stats)
echo $stats

# Test README update (create a test README first)
cp README.md TEST_README.md
STATS='{"global-suicide-rates-views":1234,"global-suicide-rates-downloads":567}' python scripts/update_readme.py
diff README.md TEST_README.md