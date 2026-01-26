#!/usr/bin/env python3
"""
Analyze a potential new skills repository for compatibility with agent_skills_directory.
Usage: python scripts/analyze_repo.py <github_repo_url>
Example: python scripts/analyze_repo.py https://github.com/Prat011/awesome-llm-skills
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from collections import defaultdict

# Load existing catalog for duplicate detection
CATALOG_PATH = os.path.join(os.path.dirname(__file__), "..", "catalog.json")

def fetch_json(url: str, token: str | None = None) -> dict:
    """Fetch JSON from URL with optional auth."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason} for {url}")
        return {}

def fetch_text(url: str, token: str | None = None) -> str:
    """Fetch raw text from URL."""
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
        return ""

def parse_yaml_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from SKILL.md content."""
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    yaml_block = parts[1].strip()
    # Simple YAML parsing (key: value)
    result = {}
    for line in yaml_block.split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip().strip('"').strip("'")
    return result

def analyze_repo(repo_url: str):
    """Analyze a GitHub repository for skills compatibility."""
    token = os.getenv("GITHUB_TOKEN")
    
    # Parse repo URL
    match = re.match(r"https://github\.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        print(f"❌ Invalid GitHub URL: {repo_url}")
        return
    
    owner, repo = match.groups()
    repo = repo.rstrip(".git")
    
    print(f"\n{'='*60}")
    print(f"📊 ANALYZING: {owner}/{repo}")
    print(f"{'='*60}\n")
    
    # Fetch repo tree
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    tree_data = fetch_json(api_url, token)
    
    if not tree_data or "tree" not in tree_data:
        # Try 'master' branch
        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1"
        tree_data = fetch_json(api_url, token)
    
    if not tree_data or "tree" not in tree_data:
        print("❌ Could not fetch repository tree. Check if repo exists and is public.")
        return
    
    tree = tree_data["tree"]
    
    # Find SKILL.md files
    skill_files = []
    all_paths = [item["path"] for item in tree]
    
    for item in tree:
        path = item["path"]
        if path.endswith("SKILL.md"):
            skill_files.append(path)
    
    print(f"📁 Repository Structure Analysis")
    print(f"   Total files/dirs: {len(tree)}")
    print(f"   SKILL.md files found: {len(skill_files)}")
    
    # Detect skills directory pattern
    skills_prefixes = set()
    for sf in skill_files:
        parts = sf.rsplit("/", 1)
        if len(parts) > 1:
            prefix = parts[0].rsplit("/", 1)
            if len(prefix) > 1:
                skills_prefixes.add(prefix[0] + "/")
            else:
                skills_prefixes.add("")
    
    print(f"   Skills path prefixes: {skills_prefixes or 'root level'}")
    
    if not skill_files:
        print("\n⚠️  No SKILL.md files found!")
        print("   Looking for alternative patterns...")
        
        # Check for other markdown files that might be skills
        md_files = [p for p in all_paths if p.endswith(".md") and p != "README.md"]
        print(f"   Other .md files: {len(md_files)}")
        if md_files[:10]:
            for f in md_files[:10]:
                print(f"      - {f}")
        return
    
    # Load existing catalog for duplicate detection
    existing_skills = {}
    existing_descriptions = {}
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH) as f:
            catalog = json.load(f)
            for skill in catalog.get("skills", []):
                name = skill.get("name", "").lower()
                existing_skills[name] = skill.get("id")
                desc = skill.get("description", "").lower()[:100]
                existing_descriptions[desc] = skill.get("id")
    
    print(f"\n📋 Existing catalog: {len(existing_skills)} skills loaded for comparison")
    
    # Analyze each SKILL.md
    print(f"\n{'='*60}")
    print("📝 SKILL.md ANALYSIS")
    print(f"{'='*60}\n")
    
    raw_base = f"https://raw.githubusercontent.com/{owner}/{repo}/main"
    
    quality_scores = []
    duplicates = []
    unique_skills = []
    parse_errors = []
    
    for skill_path in skill_files:
        skill_url = f"{raw_base}/{skill_path}"
        content = fetch_text(skill_url, token)
        
        if not content:
            # Try master branch
            skill_url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{skill_path}"
            content = fetch_text(skill_url, token)
        
        skill_name = skill_path.rsplit("/", 2)[-2] if "/" in skill_path else skill_path
        
        if not content:
            parse_errors.append((skill_name, "Could not fetch content"))
            continue
        
        # Parse frontmatter
        frontmatter = parse_yaml_frontmatter(content)
        
        # Quality scoring
        score = 0
        issues = []
        
        # Required fields
        if frontmatter.get("name"):
            score += 25
        else:
            issues.append("missing 'name'")
        
        if frontmatter.get("description"):
            score += 25
            desc_len = len(frontmatter.get("description", ""))
            if desc_len > 50:
                score += 10
            if desc_len > 100:
                score += 10
        else:
            issues.append("missing 'description'")
        
        if frontmatter.get("license"):
            score += 15
        else:
            issues.append("missing 'license'")
        
        # Bonus fields
        if frontmatter.get("version"):
            score += 5
        if frontmatter.get("tags"):
            score += 5
        if frontmatter.get("author"):
            score += 5
        
        # Check for body content
        body_start = content.find("---", 3)
        if body_start > 0:
            body = content[body_start+3:].strip()
            if len(body) > 200:
                score += 10
        
        quality_scores.append((skill_name, score, issues, frontmatter))
        
        # Duplicate detection
        name_lower = frontmatter.get("name", skill_name).lower()
        if name_lower in existing_skills:
            duplicates.append((skill_name, existing_skills[name_lower], "exact name match"))
        else:
            unique_skills.append(skill_name)
    
    # Print results
    print("✅ VALID SKILLS:")
    for name, score, issues, fm in sorted(quality_scores, key=lambda x: -x[1]):
        status = "✓" if score >= 50 else "⚠️"
        print(f"   {status} {name}: {score}/100", end="")
        if issues:
            print(f" (issues: {', '.join(issues)})", end="")
        print()
    
    if parse_errors:
        print(f"\n❌ PARSE ERRORS ({len(parse_errors)}):")
        for name, error in parse_errors:
            print(f"   - {name}: {error}")
    
    print(f"\n{'='*60}")
    print("🔄 DUPLICATE ANALYSIS")
    print(f"{'='*60}\n")
    
    if duplicates:
        print(f"⚠️  POTENTIAL DUPLICATES ({len(duplicates)}):")
        for new_skill, existing_id, reason in duplicates:
            print(f"   - '{new_skill}' matches '{existing_id}' ({reason})")
    else:
        print("✅ No exact duplicates found")
    
    print(f"\n🆕 UNIQUE SKILLS ({len(unique_skills)}):")
    for skill in unique_skills[:20]:
        print(f"   + {skill}")
    if len(unique_skills) > 20:
        print(f"   ... and {len(unique_skills) - 20} more")
    
    # Summary
    avg_quality = sum(s[1] for s in quality_scores) / len(quality_scores) if quality_scores else 0
    
    print(f"\n{'='*60}")
    print("📊 SUMMARY")
    print(f"{'='*60}\n")
    print(f"   Total SKILL.md files:    {len(skill_files)}")
    print(f"   Successfully parsed:     {len(quality_scores)}")
    print(f"   Parse errors:            {len(parse_errors)}")
    print(f"   Average quality score:   {avg_quality:.1f}/100")
    print(f"   Potential duplicates:    {len(duplicates)}")
    print(f"   Unique new skills:       {len(unique_skills)}")
    
    # Recommendation
    print(f"\n{'='*60}")
    print("💡 RECOMMENDATION")
    print(f"{'='*60}\n")
    
    if len(skill_files) == 0:
        print("   ❌ NOT COMPATIBLE - No SKILL.md files found")
        print("   This repo doesn't follow the expected structure.")
    elif avg_quality < 30:
        print("   ⚠️  LOW QUALITY - Average score below 30")
        print("   Most skills are missing required frontmatter fields.")
    elif len(unique_skills) == 0:
        print("   ⚠️  NO NEW VALUE - All skills are duplicates")
        print("   This repo doesn't add unique skills to the catalog.")
    elif avg_quality >= 50 and len(unique_skills) >= 3:
        print("   ✅ RECOMMENDED TO ADD")
        print(f"   Would add {len(unique_skills)} unique skills with good quality.")
        
        # Generate provider config
        prefix = list(skills_prefixes)[0] if skills_prefixes else "skills/"
        print(f"\n   Add to PROVIDERS in scripts/aggregate.py:")
        print(f'''
    "{owner.lower()}": {{
        "name": "{owner}",
        "repo": "{repo_url}",
        "api_tree_url": "https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/{owner}/{repo}/main",
        "skills_path_prefix": "{prefix}",
    }},''')
    else:
        print(f"   ⚠️  MARGINAL - Consider if {len(unique_skills)} new skills justify adding")
        print(f"   Quality score: {avg_quality:.1f}/100")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/analyze_repo.py <github_repo_url>")
        print("Example: python scripts/analyze_repo.py https://github.com/Prat011/awesome-llm-skills")
        sys.exit(1)
    
    analyze_repo(sys.argv[1])
