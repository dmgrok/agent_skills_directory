#!/usr/bin/env python3
"""
Agent Skills Directory Aggregator

Fetches skills from multiple provider repositories and creates
a unified catalog in JSON format.
"""

import json
import re
import sys
import time
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
import urllib.request
import urllib.error
import subprocess
import shutil
from urllib.parse import urlsplit

try:
    import toon_format  # type: ignore[import-untyped]
    HAS_TOON = True
except ImportError:
    HAS_TOON = False

import yaml  # type: ignore[import-untyped]


# Provider configurations
PROVIDERS = {
    "anthropics": {
        "name": "Anthropic",
        "repo": "https://github.com/anthropics/skills",
        "api_tree_url": "https://api.github.com/repos/anthropics/skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/anthropics/skills/main",
        "skills_path_prefix": "skills/",
    },
    "openai": {
        "name": "OpenAI",
        "repo": "https://github.com/openai/skills",
        "api_tree_url": "https://api.github.com/repos/openai/skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/openai/skills/main",
        "skills_path_prefix": "skills/",
    },
    "github": {
        "name": "GitHub",
        "repo": "https://github.com/github/awesome-copilot",
        "api_tree_url": "https://api.github.com/repos/github/awesome-copilot/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/github/awesome-copilot/main",
        "skills_path_prefix": "skills/",
    },
    "vercel": {
        "name": "Vercel",
        "repo": "https://github.com/vercel-labs/agent-skills",
        "api_tree_url": "https://api.github.com/repos/vercel-labs/agent-skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/vercel-labs/agent-skills/main",
        "skills_path_prefix": "skills/",
    },
    "huggingface": {
        "name": "HuggingFace",
        "repo": "https://github.com/huggingface/skills",
        "api_tree_url": "https://api.github.com/repos/huggingface/skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/huggingface/skills/main",
        "skills_path_prefix": "skills/",
    },
    "skillcreatorai": {
        "name": "SkillCreator.ai",
        "repo": "https://github.com/skillcreatorai/Ai-Agent-Skills",
        "api_tree_url": "https://api.github.com/repos/skillcreatorai/Ai-Agent-Skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main",
        "skills_path_prefix": "skills/",
    },
}

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DEFAULT_HEADERS = {"User-Agent": "AgentSkillsDirectory/1.0"}
if GITHUB_TOKEN:
    # Use GitHub token when available to avoid rate limits
    DEFAULT_HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    DEFAULT_HEADERS["Accept"] = "application/vnd.github+json"

# Category mappings based on keywords in name/description
CATEGORY_KEYWORDS = {
    "documents": ["pdf", "docx", "xlsx", "pptx", "document", "spreadsheet", "presentation"],
    "development": ["git", "gh-", "code", "test", "ci", "debug", "lint", "review", "mcp"],
    "creative": ["art", "design", "canvas", "music", "brand", "visual", "image"],
    "enterprise": ["communication", "meeting", "email", "slack", "notion", "knowledge"],
    "integrations": ["notion", "github", "slack", "api"],
    "data": ["data", "analysis", "extract", "transform", "csv", "json"],
}


@dataclass
class SkillSource:
    repo: str
    path: str
    skill_md_url: str
    commit_sha: Optional[str] = None


@dataclass
class Skill:
    id: str
    name: str
    description: str
    provider: str
    category: str
    license: Optional[str]
    compatibility: Optional[str]
    last_updated_at: Optional[str]
    metadata: dict
    source: SkillSource
    has_scripts: bool
    has_references: bool
    has_assets: bool
    tags: list[str]


def fetch_url(url: str, retries: int = 3) -> Optional[str]:
    """Fetch content from URL with retry logic."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode("utf-8")
        except (urllib.error.URLError, OSError) as e:
            if attempt < retries - 1:
                wait = 2 ** attempt  # Exponential backoff
                print(f"  Retry {attempt + 1}/{retries} for {url} (waiting {wait}s)", file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"  Warning: Failed to fetch {url}: {e}", file=sys.stderr)
                return None
    return None


def parse_skill_md(content: str) -> Optional[dict]:
    """Parse SKILL.md content and extract frontmatter + body."""
    # Match YAML frontmatter between --- markers
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None
    
    try:
        frontmatter = yaml.safe_load(match.group(1))
        body = match.group(2)
        return {
            "frontmatter": frontmatter or {},
            "body": body
        }
    except yaml.YAMLError as e:
        print(f"  Warning: Failed to parse YAML: {e}", file=sys.stderr)
        return None


def extract_tags(name: str, description: str) -> list:
    """Extract searchable tags from skill name and description."""
    text = f"{name} {description}".lower()
    
    # Common keywords to extract
    keywords = [
        "pdf", "docx", "xlsx", "pptx", "csv", "json", "yaml",
        "github", "git", "pr", "ci", "cd", "test", "lint",
        "notion", "slack", "api", "mcp", "cli",
        "design", "art", "music", "brand", "visual",
        "document", "extract", "merge", "convert", "analysis",
        "meeting", "email", "knowledge", "wiki", "faq",
    ]
    
    tags = []
    for kw in keywords:
        if kw in text:
            tags.append(kw)
    
    # Add words from name
    name_words = name.replace("-", " ").split()
    for word in name_words:
        if word not in tags and len(word) > 2:
            tags.append(word)
    
    return tags[:10]  # Limit to 10 tags


def extract_owner_repo(repo_url: str) -> Optional[tuple[str, str]]:
    """Return (owner, repo) tuple from a GitHub repo URL."""
    parsed = urlsplit(repo_url)
    parts = parsed.path.strip("/").split("/")
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None


def fetch_last_updated_at(owner: str, repo: str, file_path: str) -> Optional[str]:
    """Fetch the last commit date for a specific file."""
    commits_url = (
        f"https://api.github.com/repos/{owner}/{repo}/commits"
        f"?path={file_path}&per_page=1&sha=main"
    )
    content = fetch_url(commits_url)
    if not content:
        return None

    try:
        commits = json.loads(content)
    except json.JSONDecodeError:
        print(f"  Warning: Failed to parse commits response for {file_path}", file=sys.stderr)
        return None

    if isinstance(commits, list) and commits:
        commit = commits[0].get("commit", {})
        author = commit.get("author", {}) or {}
        committer = commit.get("committer", {}) or {}
        return author.get("date") or committer.get("date")
    return None


def categorize_skill(name: str, description: str) -> str:
    """Determine category based on name and description."""
    text = f"{name} {description}".lower()
    
    scores: dict[str, int] = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[category] = score
    
    if scores:
        return max(scores, key=scores.__getitem__)
    return "other"


def fetch_provider_skills(provider_id: str, config: dict) -> list:
    """Fetch all skills from a provider repository."""
    print(f"Fetching skills from {config['name']}...")
    owner_repo = extract_owner_repo(config["repo"])
    
    # Get repository tree
    tree_content = fetch_url(config["api_tree_url"])
    if not tree_content:
        return []
    
    try:
        tree_data = json.loads(tree_content)
    except json.JSONDecodeError:
        print(f"  Error: Failed to parse tree JSON", file=sys.stderr)
        return []
    
    # Find all SKILL.md files
    skill_files = []
    all_paths = set()
    
    for item in tree_data.get("tree", []):
        path = item.get("path", "")
        all_paths.add(path)
        
        if path.startswith(config["skills_path_prefix"]) and path.endswith("/SKILL.md"):
            skill_files.append({
                "path": path,
                "sha": item.get("sha"),
                "dir": str(Path(path).parent)
            })
    
    print(f"  Found {len(skill_files)} skills")
    
    skills = []
    for sf in skill_files:
        skill_md_url = f"{config['raw_base']}/{sf['path']}"
        content = fetch_url(skill_md_url)
        
        if not content:
            continue
        
        parsed = parse_skill_md(content)
        if not parsed or "name" not in parsed["frontmatter"]:
            print(f"  Skipping {sf['path']}: missing required frontmatter", file=sys.stderr)
            continue
        
        fm = parsed["frontmatter"]
        name = fm.get("name", "")
        description = fm.get("description", "")
        
        # Check for optional directories
        skill_dir = sf["dir"]
        has_scripts = any(p.startswith(f"{skill_dir}/scripts/") for p in all_paths)
        has_references = any(p.startswith(f"{skill_dir}/references/") or p.startswith(f"{skill_dir}/reference/") for p in all_paths)
        has_assets = any(p.startswith(f"{skill_dir}/assets/") or p.startswith(f"{skill_dir}/templates/") for p in all_paths)

        last_updated_at = None
        if owner_repo:
            last_updated_at = fetch_last_updated_at(owner_repo[0], owner_repo[1], sf["path"])
        
        skill = Skill(
            id=f"{provider_id}/{name}",
            name=name,
            description=description,
            provider=provider_id,
            category=categorize_skill(name, description),
            license=fm.get("license"),
            compatibility=fm.get("compatibility"),
            last_updated_at=last_updated_at,
            metadata=fm.get("metadata", {}),
            source=SkillSource(
                repo=config["repo"],
                path=skill_dir,
                skill_md_url=skill_md_url,
                commit_sha=tree_data.get("sha")
            ),
            has_scripts=has_scripts,
            has_references=has_references,
            has_assets=has_assets,
            tags=extract_tags(name, description)
        )
        
        skills.append(skill)
        print(f"  ✓ {name}")
    
    return skills


def build_catalog() -> dict:
    """Build the complete skills catalog."""
    all_skills = []
    provider_stats = {}
    
    for provider_id, config in PROVIDERS.items():
        skills = fetch_provider_skills(provider_id, config)
        all_skills.extend(skills)
        provider_stats[provider_id] = {
            "name": config["name"],
            "repo": config["repo"],
            "skills_count": len(skills)
        }
    
    # Sort skills by provider then name
    all_skills.sort(key=lambda s: (s.provider, s.name))
    
    # Get unique categories
    categories = sorted(set(s.category for s in all_skills))
    
    # Build catalog
    now = datetime.now(timezone.utc)
    catalog = {
        "$schema": "https://raw.githubusercontent.com/dmgrok/agent_skills_directory/main/schema/catalog-schema.json",
        "version": now.strftime("%Y.%m.%d"),
        "generated_at": now.isoformat(),
        "total_skills": len(all_skills),
        "providers": provider_stats,
        "categories": categories,
        "skills": []
    }
    
    # Convert skills to dicts
    for skill in all_skills:
        skill_dict = asdict(skill)
        # Convert nested dataclass
        skill_dict["source"] = asdict(skill.source)
        catalog["skills"].append(skill_dict)
    
    return catalog


def write_toon_output(catalog: dict, output_dir: Path, catalog_json: Path, catalog_min_json: Path) -> None:
    """Write TOON format using python encoder if available, else fall back to npx CLI."""
    catalog_toon = output_dir / "catalog.toon"
    catalog_toon_min = output_dir / "catalog.min.toon"

    if HAS_TOON:
        try:
            toon_content = toon_format.encode(catalog)
            catalog_toon.write_text(toon_content, encoding="utf-8")
            catalog_toon_min.write_text(toon_content, encoding="utf-8")
            print(f"✓ Written: {catalog_toon} (python toon_format)")
            print(f"✓ Written: {catalog_toon_min} (python toon_format)")
            return
        except NotImplementedError:
            print("⚠ toon_format.encode not implemented; falling back to npx @toon-format/cli", file=sys.stderr)
        except Exception as e:
            print(f"⚠ toon_format.encode failed ({e}); falling back to npx @toon-format/cli", file=sys.stderr)

    npx_path = shutil.which("npx")
    if not npx_path:
        print("⚠ Skipped TOON output: npx not found and python encoder unavailable", file=sys.stderr)
        return

    try:
        subprocess.run(
            [npx_path, "@toon-format/cli", str(catalog_json), "-o", str(catalog_toon)],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [npx_path, "@toon-format/cli", str(catalog_min_json), "-o", str(catalog_toon_min)],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"✓ Written: {catalog_toon} (via npx @toon-format/cli)")
        print(f"✓ Written: {catalog_toon_min} (via npx @toon-format/cli)")
    except subprocess.CalledProcessError as e:
        error_out = e.stderr.strip() if e.stderr else str(e)
        print(f"⚠ Failed TOON output via npx @toon-format/cli: {error_out}", file=sys.stderr)


def main():
    print("=" * 50)
    print("Agent Skills Directory Aggregator")
    print("=" * 50)
    print()
    
    catalog = build_catalog()
    
    # Output paths
    output_dir = Path(__file__).parent.parent
    catalog_json = output_dir / "catalog.json"
    catalog_min_json = output_dir / "catalog.min.json"
    
    # Write pretty JSON
    with open(catalog_json, "w") as f:
        json.dump(catalog, f, indent=2)
    print(f"\n✓ Written: {catalog_json}")
    
    # Write minified JSON
    with open(catalog_min_json, "w") as f:
        json.dump(catalog, f, separators=(",", ":"))
    print(f"✓ Written: {catalog_min_json}")
    
    # Write TOON format (Token-Oriented Object Notation)
    write_toon_output(catalog, output_dir, catalog_json, catalog_min_json)
    
    # Summary
    print(f"\n{'=' * 50}")
    print(f"Total skills: {catalog['total_skills']}")
    for pid, pinfo in catalog["providers"].items():
        print(f"  {pinfo['name']}: {pinfo['skills_count']} skills")
    print(f"Categories: {', '.join(catalog['categories'])}")
    print("=" * 50)


if __name__ == "__main__":
    main()
