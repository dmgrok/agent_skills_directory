#!/usr/bin/env python3
"""
Lightweight script to test a single provider before adding to aggregate.py
"""

import sys
import json
import os
from typing import Dict, Any
import requests
import yaml
from datetime import datetime

def fetch_url(url: str, headers: Dict[str, str] = None) -> Any:
    """Fetch URL with retry logic"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                print(f"❌ Failed to fetch {url}: {e}", file=sys.stderr)
                return None
            print(f"⚠️  Retry {attempt + 1}/{max_retries} for {url}", file=sys.stderr)
    return None

def test_provider(provider_config: Dict[str, Any]) -> bool:
    """Test a single provider configuration"""
    provider_id = list(provider_config.keys())[0]
    config = provider_config[provider_id]
    
    print(f"\n{'='*60}")
    print(f"Testing Provider: {config['name']} ({provider_id})")
    print(f"{'='*60}\n")
    
    # Set up headers for GitHub API
    github_token = os.environ.get('GITHUB_TOKEN')
    headers = {'Authorization': f'token {github_token}'} if github_token else {}
    
    # 1. Test API tree URL
    print(f"📡 Testing API tree URL...")
    tree_response = fetch_url(config['api_tree_url'], headers)
    if not tree_response:
        print(f"❌ Failed to fetch tree from {config['api_tree_url']}")
        return False
    
    try:
        tree_data = tree_response.json()
        if 'tree' not in tree_data:
            print(f"❌ Invalid tree response (missing 'tree' key)")
            return False
        print(f"✅ Tree API accessible ({len(tree_data['tree'])} items)")
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse tree JSON: {e}")
        return False
    
    # 2. Find SKILL.md files
    skill_paths = []
    prefix = config.get('skills_path_prefix', 'skills/')
    
    for item in tree_data['tree']:
        path = item.get('path', '')
        if prefix:
            if path.startswith(prefix) and path.endswith('/SKILL.md'):
                skill_paths.append(path)
        else:
            # Root level SKILL.md
            if path == 'SKILL.md':
                skill_paths.append(path)
    
    print(f"\n📁 Found {len(skill_paths)} SKILL.md file(s)")
    if len(skill_paths) == 0:
        print(f"⚠️  No SKILL.md files found (looking for prefix: '{prefix}')")
        return False
    
    # 3. Test fetching and parsing a few skills
    skills_tested = 0
    skills_valid = 0
    max_test = min(3, len(skill_paths))  # Test up to 3 skills
    
    print(f"\n🔍 Testing {max_test} skill(s):\n")
    
    for skill_path in skill_paths[:max_test]:
        skills_tested += 1
        skill_url = f"{config['raw_base']}/{skill_path}"
        print(f"  {skills_tested}. {skill_path}")
        
        response = fetch_url(skill_url, headers)
        if not response:
            print(f"     ❌ Failed to fetch")
            continue
        
        try:
            content = response.text
            
            # Check for YAML frontmatter
            if not content.startswith('---'):
                print(f"     ❌ Missing YAML frontmatter")
                continue
            
            # Extract frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                print(f"     ❌ Invalid frontmatter format")
                continue
            
            frontmatter = yaml.safe_load(parts[1])
            
            # Validate required fields
            required_fields = ['name', 'description']
            missing_fields = [f for f in required_fields if f not in frontmatter]
            
            if missing_fields:
                print(f"     ❌ Missing fields: {', '.join(missing_fields)}")
                continue
            
            print(f"     ✅ Valid - '{frontmatter['name']}'")
            skills_valid += 1
            
        except yaml.YAMLError as e:
            print(f"     ❌ YAML parse error: {e}")
            continue
        except Exception as e:
            print(f"     ❌ Error: {e}")
            continue
    
    # 4. Summary
    print(f"\n{'='*60}")
    print(f"📊 Test Results:")
    print(f"   Total SKILL.md files: {len(skill_paths)}")
    print(f"   Skills tested: {skills_tested}")
    print(f"   Valid skills: {skills_valid}")
    print(f"   Success rate: {skills_valid}/{skills_tested}")
    print(f"{'='*60}\n")
    
    if skills_valid == 0:
        print("❌ No valid skills found - provider test FAILED")
        return False
    
    if skills_valid < skills_tested:
        print(f"⚠️  Some skills failed validation ({skills_tested - skills_valid} failed)")
        print("⚠️  Provider test PASSED with warnings")
        return True
    
    print("✅ All tested skills are valid - provider test PASSED")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_provider.py <provider_config_json>")
        print("\nExample:")
        print('  python test_provider.py \'{"aiqualitylab": {"name": "AI Quality Lab", ...}}\'')
        sys.exit(1)
    
    try:
        provider_config = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    
    success = test_provider(provider_config)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
