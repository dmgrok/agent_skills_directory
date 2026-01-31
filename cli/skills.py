#!/usr/bin/env python3
"""
skills - The package manager for AI agent skills

Usage:
    skills search <query>           Search for skills
    skills info <skill-id>          Show skill details
    skills suggest [path]           Get AI recommendations for your project
    skills install <skill-id>       Install a skill
    skills uninstall <skill-id>     Remove a skill
    skills list                     List installed skills
    skills init                     Create a new skill.json
    skills publish                  Publish skill to registry
    skills update                   Update installed skills
    skills run <skill-id>           Run a skill
    skills config                   Manage configuration
    skills cache clean              Clear the cache
    skills --version                Show version
    skills --help                   Show help

Installation Targets:
    --global, -g        Install to ~/.skills/ (default, shared across projects)
    --project, -p       Install to current project's skills directory
    --agent AGENT       Target agent: auto, claude, copilot, codex (default: auto)

Agent-Specific Paths:
    Claude:  .claude/skills/     (project) or ~/.claude/skills/ (personal)
    Copilot: .github/skills/     (project) or ~/.copilot/skills/ (personal)
    Codex:   .codex/skills/      (project) or ~/.codex/skills/ (personal)
    Cursor:  .cursor/skills/     (project) or ~/.cursor/skills/ (personal)

Examples:
    skills search "web scraping"
    skills install anthropic/web-researcher
    skills install anthropic/web-researcher@1.2.0
    skills install github/pdf -p --agent claude     # Install to .claude/skills/
    skills install github/pdf -p --agent copilot   # Install to .github/skills/
    skills install github/pdf -g                   # Install to ~/.skills/
    skills info openai/code-interpreter
    skills list --json
"""

__version__ = "0.1.0"
__author__ = "Agent Skills Directory"

import argparse
import json
import os
import sys
import shutil
import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# =============================================================================
# Agent Profiles - Installation paths for different AI agents/IDEs
# =============================================================================

AGENT_PROFILES = {
    "claude": {
        "name": "Claude",
        "project_paths": [".claude/skills", ".github/skills"],
        "personal_path": Path.home() / ".claude" / "skills",
        "instructions_file": "CLAUDE.md",
        "env_var": "CLAUDE_CODE",
        "markers": [".claude", "CLAUDE.md"],
    },
    "copilot": {
        "name": "GitHub Copilot",
        "project_paths": [".github/skills", ".claude/skills"],
        "personal_path": Path.home() / ".copilot" / "skills",
        "instructions_file": ".github/copilot-instructions.md",
        "env_var": "GITHUB_COPILOT",
        "markers": [".github/copilot-instructions.md", ".vscode"],
    },
    "codex": {
        "name": "OpenAI Codex",
        "project_paths": [".codex/skills", ".github/skills"],
        "personal_path": Path.home() / ".codex" / "skills",
        "instructions_file": "AGENTS.md",
        "env_var": "CODEX_HOME",
        "markers": [".codex", "AGENTS.md"],
    },
    "cursor": {
        "name": "Cursor",
        "project_paths": [".cursor/skills", ".cursorrules"],
        "personal_path": Path.home() / ".cursor" / "skills",
        "instructions_file": ".cursorrules",
        "env_var": "CURSOR_HOME",
        "markers": [".cursor", ".cursorrules"],
    },
    "generic": {
        "name": "Generic",
        "project_paths": [".github/skills", ".claude/skills"],
        "personal_path": Path.home() / ".skills" / "installed",
        "instructions_file": None,
        "env_var": None,
        "markers": [],
    },
}

# =============================================================================
# Constants
# =============================================================================

SKILLS_HOME = Path.home() / ".skills"
SKILLS_CONFIG = SKILLS_HOME / "config.json"
SKILLS_INSTALLED = SKILLS_HOME / "installed"
SKILLS_CACHE = SKILLS_HOME / "cache"
SKILLS_LOCK = SKILLS_HOME / "skills-lock.json"

CATALOG_URL = "https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.json"
CATALOG_CACHE_TTL = 3600  # 1 hour

# ANSI colors
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    
    @classmethod
    def disable(cls):
        for attr in dir(cls):
            if not attr.startswith('_') and attr != 'disable':
                setattr(cls, attr, "")

# Disable colors if not a TTY
if not sys.stdout.isatty():
    Colors.disable()


def print_error(msg: str):
    print(f"{Colors.RED}error:{Colors.RESET} {msg}", file=sys.stderr)


def print_success(msg: str):
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")


def print_info(msg: str):
    print(f"{Colors.CYAN}→{Colors.RESET} {msg}")


def print_warning(msg: str):
    print(f"{Colors.YELLOW}warning:{Colors.RESET} {msg}")


def ensure_dirs():
    """Create skills home directory structure."""
    SKILLS_HOME.mkdir(exist_ok=True)
    SKILLS_INSTALLED.mkdir(exist_ok=True)
    SKILLS_CACHE.mkdir(exist_ok=True)
    
    if not SKILLS_CONFIG.exists():
        default_config = {
            "registry": CATALOG_URL,
            "cache_ttl": CATALOG_CACHE_TTL,
            "auto_update": True,
            "telemetry": False,
            "default_agent": "auto",
            "default_scope": "global"  # global or project
        }
        SKILLS_CONFIG.write_text(json.dumps(default_config, indent=2))


def load_config() -> Dict[str, Any]:
    """Load skills configuration."""
    ensure_dirs()
    return json.loads(SKILLS_CONFIG.read_text())


def save_config(config: Dict[str, Any]):
    """Save skills configuration."""
    SKILLS_CONFIG.write_text(json.dumps(config, indent=2))


def fetch_url(url: str, timeout: int = 30) -> str:
    """Fetch URL content with error handling."""
    req = Request(url, headers={"User-Agent": f"skills-cli/{__version__}"})
    try:
        with urlopen(req, timeout=timeout) as response:
            return response.read().decode("utf-8")
    except HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.reason}")
    except URLError as e:
        raise RuntimeError(f"Network error: {e.reason}")


def get_cache_path(url: str) -> Path:
    """Get cache file path for a URL."""
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return SKILLS_CACHE / f"{url_hash}.json"


def fetch_catalog(force_refresh: bool = False) -> Dict[str, Any]:
    """Fetch catalog with caching."""
    config = load_config()
    cache_path = get_cache_path(config["registry"])
    
    # Check cache
    if not force_refresh and cache_path.exists():
        cache_age = datetime.now().timestamp() - cache_path.stat().st_mtime
        if cache_age < config["cache_ttl"]:
            return json.loads(cache_path.read_text())
    
    # Fetch fresh catalog
    print_info("Fetching catalog...")
    try:
        content = fetch_url(config["registry"])
        catalog = json.loads(content)
        cache_path.write_text(content)
        return catalog
    except Exception as e:
        if cache_path.exists():
            print_warning(f"Using cached catalog: {e}")
            return json.loads(cache_path.read_text())
        raise


# =============================================================================
# Agent Detection
# =============================================================================

def detect_agent(project_path: Path = None) -> str:
    """Detect which AI agent is being used based on environment and project structure."""
    project_path = project_path or Path.cwd()
    
    # 1. Check environment variables
    for agent_id, profile in AGENT_PROFILES.items():
        if agent_id == "generic":
            continue
        env_var = profile.get("env_var")
        if env_var and os.environ.get(env_var):
            return agent_id
    
    # 2. Check for agent-specific markers in project
    for agent_id, profile in AGENT_PROFILES.items():
        if agent_id == "generic":
            continue
        for marker in profile.get("markers", []):
            if (project_path / marker).exists():
                return agent_id
    
    # 3. Check for agent-specific personal directories
    for agent_id, profile in AGENT_PROFILES.items():
        if agent_id == "generic":
            continue
        personal_path = profile.get("personal_path")
        if personal_path and personal_path.exists():
            return agent_id
    
    # 4. Default to generic
    return "generic"


def get_install_path(skill_id: str, agent: str = "auto", project: bool = False, project_path: Path = None) -> Path:
    """
    Determine the installation path for a skill.
    
    Args:
        skill_id: The skill ID (provider/name)
        agent: Target agent (auto, claude, copilot, codex, cursor, generic)
        project: If True, install to project; if False, install globally
        project_path: Project directory (defaults to cwd)
    
    Returns:
        Path to install the skill
    """
    project_path = project_path or Path.cwd()
    provider, name = skill_id.split("/")
    
    # Auto-detect agent if needed
    if agent == "auto":
        agent = detect_agent(project_path)
    
    profile = AGENT_PROFILES.get(agent, AGENT_PROFILES["generic"])
    
    if project:
        # Install to project's skills directory
        skills_dir = project_path / profile["project_paths"][0]
    else:
        # Install to personal/global directory
        skills_dir = profile.get("personal_path", SKILLS_INSTALLED)
    
    return skills_dir / name


def get_all_install_locations(project_path: Path = None) -> List[Tuple[str, Path]]:
    """Get all possible skill installation locations (for listing installed skills)."""
    project_path = project_path or Path.cwd()
    locations = []
    
    # Global location
    if SKILLS_INSTALLED.exists():
        locations.append(("global", SKILLS_INSTALLED))
    
    # Agent-specific personal locations
    for agent_id, profile in AGENT_PROFILES.items():
        personal_path = profile.get("personal_path")
        if personal_path and personal_path.exists() and personal_path != SKILLS_INSTALLED:
            locations.append((f"personal ({agent_id})", personal_path))
    
    # Project locations
    for agent_id, profile in AGENT_PROFILES.items():
        for proj_path in profile.get("project_paths", []):
            full_path = project_path / proj_path
            if full_path.exists():
                locations.append((f"project ({agent_id})", full_path))
    
    return locations


# =============================================================================
# Version handling and dependency resolution
# =============================================================================

def parse_version(version: str) -> Tuple[int, int, int, str]:
    """Parse semver string into tuple (major, minor, patch, prerelease)."""
    # Handle ^, ~, >=, etc prefixes
    version = re.sub(r'^[\^~>=<]+', '', version.strip())
    
    match = re.match(r'^(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:-(.+))?$', version)
    if not match:
        return (0, 0, 0, "")
    
    major = int(match.group(1))
    minor = int(match.group(2)) if match.group(2) else 0
    patch = int(match.group(3)) if match.group(3) else 0
    prerelease = match.group(4) or ""
    
    return (major, minor, patch, prerelease)


def compare_versions(v1: str, v2: str) -> int:
    """Compare two semver versions. Returns -1 if v1 < v2, 0 if equal, 1 if v1 > v2."""
    p1 = parse_version(v1)
    p2 = parse_version(v2)
    
    # Compare major, minor, patch
    for i in range(3):
        if p1[i] < p2[i]:
            return -1
        if p1[i] > p2[i]:
            return 1
    
    # Handle prerelease (no prerelease > prerelease)
    if not p1[3] and p2[3]:
        return 1
    if p1[3] and not p2[3]:
        return -1
    if p1[3] < p2[3]:
        return -1
    if p1[3] > p2[3]:
        return 1
    
    return 0


def version_satisfies(version: str, constraint: str) -> bool:
    """Check if version satisfies a constraint (^1.0.0, ~1.0.0, >=1.0.0, etc)."""
    constraint = constraint.strip()
    
    if not constraint or constraint == "*":
        return True
    
    # Exact version
    if constraint[0].isdigit():
        return compare_versions(version, constraint) == 0
    
    # Caret range (^1.2.3): >=1.2.3 <2.0.0
    if constraint.startswith("^"):
        base = parse_version(constraint[1:])
        ver = parse_version(version)
        
        if ver[0] != base[0]:  # Major must match
            return False
        if ver[0] == 0:  # 0.x.y - minor must match
            return ver[1] == base[1] and ver[2] >= base[2]
        return compare_versions(version, constraint[1:]) >= 0
    
    # Tilde range (~1.2.3): >=1.2.3 <1.3.0
    if constraint.startswith("~"):
        base = parse_version(constraint[1:])
        ver = parse_version(version)
        
        return ver[0] == base[0] and ver[1] == base[1] and ver[2] >= base[2]
    
    # Greater/less than
    if constraint.startswith(">="):
        return compare_versions(version, constraint[2:]) >= 0
    if constraint.startswith("<="):
        return compare_versions(version, constraint[2:]) <= 0
    if constraint.startswith(">"):
        return compare_versions(version, constraint[1:]) > 0
    if constraint.startswith("<"):
        return compare_versions(version, constraint[1:]) < 0
    
    return False


def resolve_dependencies(
    skill_id: str,
    catalog: Dict,
    installed: Dict,
    resolved: Dict = None,
    depth: int = 0
) -> Tuple[Dict[str, Dict], List[str]]:
    """
    Resolve dependencies for a skill recursively.
    
    Returns:
        (resolved_deps, errors): Dict of skill_id -> {skill, version, depth}, list of errors
    """
    if resolved is None:
        resolved = {}
    
    errors = []
    max_depth = 10  # Prevent infinite loops
    
    if depth > max_depth:
        errors.append(f"Maximum dependency depth ({max_depth}) exceeded")
        return resolved, errors
    
    skill = find_skill(catalog, skill_id)
    if not skill:
        errors.append(f"Skill not found: {skill_id}")
        return resolved, errors
    
    # Get dependencies from skill manifest or catalog
    source = skill.get("source", {})
    manifest_url = source.get("skill_json_url")
    
    dependencies = {}
    
    # Try to fetch skill.json for dependencies
    if manifest_url:
        try:
            manifest_content = fetch_url(manifest_url)
            manifest = json.loads(manifest_content)
            dependencies = manifest.get("dependencies", {})
        except Exception:
            pass  # No manifest or fetch failed, no dependencies
    
    # Process each dependency
    for dep_id, version_constraint in dependencies.items():
        if dep_id in resolved:
            # Check version compatibility
            existing_version = resolved[dep_id].get("version", "0.0.0")
            if not version_satisfies(existing_version, version_constraint):
                errors.append(
                    f"Version conflict: {dep_id} requires {version_constraint}, "
                    f"but {existing_version} is already resolved"
                )
            continue
        
        dep_skill = find_skill(catalog, dep_id)
        if not dep_skill:
            errors.append(f"Dependency not found: {dep_id} (required by {skill_id})")
            continue
        
        dep_version = dep_skill.get("version", "0.0.0")
        
        # Check if version satisfies constraint
        if not version_satisfies(dep_version, version_constraint):
            errors.append(
                f"No compatible version for {dep_id}: requires {version_constraint}, "
                f"available: {dep_version}"
            )
            continue
        
        resolved[dep_id] = {
            "skill": dep_skill,
            "version": dep_version,
            "constraint": version_constraint,
            "required_by": skill_id,
            "depth": depth + 1
        }
        
        # Recursively resolve dependencies
        _, sub_errors = resolve_dependencies(dep_id, catalog, installed, resolved, depth + 1)
        errors.extend(sub_errors)
    
    return resolved, errors


def parse_skill_spec(spec: str) -> tuple[str, Optional[str]]:
    """Parse skill@version specification."""
    if "@" in spec and not spec.startswith("@"):
        parts = spec.rsplit("@", 1)
        return parts[0], parts[1]
    return spec, None


def find_skill(catalog: Dict, skill_id: str) -> Optional[Dict]:
    """Find a skill by ID."""
    for skill in catalog.get("skills", []):
        if skill["id"] == skill_id:
            return skill
    return None


def search_skills(catalog: Dict, query: str) -> List[Dict]:
    """Search skills by query."""
    query_lower = query.lower()
    results = []
    
    for skill in catalog.get("skills", []):
        score = 0
        name = skill.get("name", "").lower()
        desc = skill.get("description", "").lower()
        tags = [t.lower() for t in skill.get("tags", [])]
        
        # Exact name match
        if query_lower == name:
            score += 100
        # Name contains query
        elif query_lower in name:
            score += 50
        # Description contains query
        if query_lower in desc:
            score += 20
        # Tag match
        if query_lower in tags:
            score += 30
        
        # Word matching
        for word in query_lower.split():
            if word in name:
                score += 10
            if word in desc:
                score += 5
            if word in tags:
                score += 8
        
        if score > 0:
            results.append((score, skill))
    
    results.sort(key=lambda x: x[0], reverse=True)
    return [skill for _, skill in results]


def get_installed_skills(project_path: Path = None) -> Dict[str, Dict]:
    """Get dictionary of all installed skills across all locations."""
    installed = {}
    project_path = project_path or Path.cwd()
    
    def scan_skills_dir(base_path: Path, location_type: str):
        """Scan a skills directory for installed skills."""
        if not base_path.exists():
            return
        
        # Skills can be either:
        # 1. Nested: base_path/provider/skill-name/
        # 2. Flat: base_path/skill-name/
        
        for entry in base_path.iterdir():
            if not entry.is_dir():
                continue
            
            # Check if this is a provider directory (has subdirectories with SKILL.md)
            has_nested_skills = any(
                (entry / sub / "SKILL.md").exists() or (entry / sub / "skill.json").exists()
                for sub in entry.iterdir() if sub.is_dir()
            )
            
            if has_nested_skills:
                # Provider/skill structure
                provider = entry.name
                for skill_dir in entry.iterdir():
                    if not skill_dir.is_dir():
                        continue
                    add_skill_from_dir(skill_dir, f"{provider}/{skill_dir.name}", location_type)
            else:
                # Flat structure (skill directly in skills dir)
                add_skill_from_dir(entry, f"local/{entry.name}", location_type)
    
    def add_skill_from_dir(skill_dir: Path, skill_id: str, location_type: str):
        """Add a skill from a directory to the installed dict."""
        manifest_path = skill_dir / "skill.json"
        skill_md_path = skill_dir / "SKILL.md"
        
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text())
            except json.JSONDecodeError:
                manifest = {}
        elif skill_md_path.exists():
            # Extract basic info from SKILL.md
            manifest = {"name": skill_dir.name, "version": "0.0.0"}
        else:
            return
        
        installed[skill_id] = {
            "path": str(skill_dir),
            "manifest": manifest,
            "version": manifest.get("version", "0.0.0"),
            "location": location_type
        }
    
    # Scan all possible locations
    for location_type, path in get_all_install_locations(project_path):
        scan_skills_dir(path, location_type)
    
    return installed


def cmd_search(args):
    """Search for skills."""
    catalog = fetch_catalog()
    results = search_skills(catalog, args.query)
    
    # Track search for analytics
    track_search(args.query)
    
    if not results:
        print_warning(f"No skills found for '{args.query}'")
        return 1
    
    print(f"\n{Colors.BOLD}Found {len(results)} skill(s):{Colors.RESET}\n")
    
    installed = get_installed_skills()
    max_results = args.limit or 20
    
    for skill in results[:max_results]:
        skill_id = skill["id"]
        is_installed = skill_id in installed
        
        status = f"{Colors.GREEN}✓ installed{Colors.RESET}" if is_installed else ""
        
        # Add quality score badge
        quality_score = skill.get("quality_score")
        score_badge = ""
        if quality_score is not None:
            score_color = Colors.GREEN if quality_score >= 80 else Colors.YELLOW if quality_score >= 60 else Colors.RED
            score_badge = f" {score_color}⭐{quality_score}{Colors.RESET}"
        
        print(f"  {Colors.BOLD}{skill_id}{Colors.RESET}{score_badge} {status}")
        print(f"  {Colors.DIM}{skill.get('description', 'No description')[:80]}{Colors.RESET}")
        
        tags = skill.get("tags", [])[:5]
        if tags:
            tag_str = " ".join(f"{Colors.CYAN}#{t}{Colors.RESET}" for t in tags)
            print(f"  {tag_str}")
        print()
    
    if len(results) > max_results:
        print(f"  {Colors.DIM}... and {len(results) - max_results} more (use --limit to see more){Colors.RESET}\n")
    
    return 0


def cmd_info(args):
    """Show skill information."""
    skill_id, version = parse_skill_spec(args.skill_id)
    catalog = fetch_catalog()
    skill = find_skill(catalog, skill_id)
    
    if not skill:
        print_error(f"Skill not found: {skill_id}")
        return 1
    
    installed = get_installed_skills()
    is_installed = skill_id in installed
    
    print(f"\n{Colors.BOLD}{skill['name']}{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 40}{Colors.RESET}")
    print(f"  {Colors.CYAN}id:{Colors.RESET}          {skill['id']}")
    print(f"  {Colors.CYAN}provider:{Colors.RESET}    {skill['provider']}")
    print(f"  {Colors.CYAN}category:{Colors.RESET}    {skill['category']}")
    print(f"  {Colors.CYAN}description:{Colors.RESET} {skill.get('description', 'N/A')}")
    
    if skill.get("license"):
        print(f"  {Colors.CYAN}license:{Colors.RESET}     {skill['license']}")
    
    if skill.get("last_updated_at"):
        updated = skill["last_updated_at"][:10]
        print(f"  {Colors.CYAN}updated:{Colors.RESET}     {updated}")
        
        # Show maintenance status
        maint_status = skill.get("maintenance_status")
        days_since = skill.get("days_since_update")
        if maint_status:
            status_emoji = {"active": "🟢", "maintained": "🟡", "stale": "🟠", "abandoned": "🔴"}.get(maint_status, "⚪")
            status_label = maint_status.capitalize()
            if days_since is not None:
                print(f"  {Colors.CYAN}maintenance:{Colors.RESET}  {status_emoji} {status_label} ({days_since} days ago)")
            else:
                print(f"  {Colors.CYAN}maintenance:{Colors.RESET}  {status_emoji} {status_label}")
    
    # Show quality score
    quality_score = skill.get("quality_score")
    if quality_score is not None:
        score_color = Colors.GREEN if quality_score >= 80 else Colors.YELLOW if quality_score >= 60 else Colors.RED
        print(f"  {Colors.CYAN}quality:{Colors.RESET}     {score_color}⭐ {quality_score}/100{Colors.RESET}")
    
    tags = skill.get("tags", [])
    if tags:
        tag_str = ", ".join(tags)
        print(f"  {Colors.CYAN}tags:{Colors.RESET}        {tag_str}")
    
    source = skill.get("source", {})
    if source.get("repo"):
        print(f"  {Colors.CYAN}repo:{Colors.RESET}        {source['repo']}")
    if source.get("skill_md_url"):
        print(f"  {Colors.CYAN}skill.md:{Colors.RESET}    {source['skill_md_url']}")
    
    print(f"\n  {Colors.CYAN}has_scripts:{Colors.RESET}    {'yes' if skill.get('has_scripts') else 'no'}")
    print(f"  {Colors.CYAN}has_references:{Colors.RESET} {'yes' if skill.get('has_references') else 'no'}")
    print(f"  {Colors.CYAN}has_assets:{Colors.RESET}     {'yes' if skill.get('has_assets') else 'no'}")
    
    if is_installed:
        inst = installed[skill_id]
        print(f"\n  {Colors.GREEN}✓ Installed{Colors.RESET} (v{inst['version']} at {inst['path']})")
    else:
        print(f"\n  {Colors.DIM}Not installed locally{Colors.RESET}")
    
    # Suggest skills.sh for actual installation
    print(f"\n{Colors.BOLD}Installation Options:{Colors.RESET}")
    print(f"  {Colors.CYAN}1. Via skills.sh (recommended):{Colors.RESET}")
    print(f"     skills.sh install {skill['provider']}/{skill['name'].lower().replace(' ', '-')}")
    print(f"\n  {Colors.CYAN}2. Manual from source:{Colors.RESET}")
    if source.get("skill_md_url"):
        print(f"     curl -O {source['skill_md_url']}")
    print(f"\n  {Colors.DIM}💡 This directory provides quality metrics. Use skills.sh for package management.{Colors.RESET}")
    
    print()
    return 0


def install_single_skill(
    skill: Dict,
    catalog: Dict,
    version: Optional[str] = None,
    agent: str = "auto",
    project: bool = False,
    force: bool = False
) -> Tuple[bool, Path]:
    """
    Install a single skill (helper for cmd_install).
    Returns (success, install_path).
    """
    skill_id = skill["id"]
    installed = get_installed_skills()
    
    if skill_id in installed and not force:
        return True, Path(installed[skill_id]["path"])
    
    install_path = get_install_path(skill_id, agent=agent, project=project)
    install_path.mkdir(parents=True, exist_ok=True)
    
    detected_agent = detect_agent() if agent == "auto" else agent
    location_desc = f"project ({detected_agent})" if project else "global"
    
    # Fetch SKILL.md
    source = skill.get("source", {})
    skill_md_url = source.get("skill_md_url")
    
    if skill_md_url:
        try:
            skill_md_content = fetch_url(skill_md_url)
            (install_path / "SKILL.md").write_text(skill_md_content)
        except Exception as e:
            print_warning(f"Could not fetch SKILL.md for {skill_id}: {e}")
    
    # Create skill.json manifest
    manifest = {
        "name": skill["name"],
        "version": version or skill.get("version", "0.0.0"),
        "description": skill.get("description", ""),
        "license": skill.get("license"),
        "keywords": skill.get("tags", []),
        "repository": source.get("repo"),
        "runtime": "universal",
        "installed_at": datetime.now().isoformat(),
        "installed_to": location_desc,
        "agent": detected_agent,
        "source": {
            "catalog_version": catalog.get("version"),
            "provider": skill["provider"],
            "original_path": source.get("path")
        }
    }
    
    (install_path / "skill.json").write_text(json.dumps(manifest, indent=2))
    
    return True, install_path


def cmd_install(args):
    """Install a skill with dependency resolution."""
    ensure_dirs()
    
    skill_id, version = parse_skill_spec(args.skill_id)
    catalog = fetch_catalog()
    skill = find_skill(catalog, skill_id)
    
    if not skill:
        print_error(f"Skill not found: {skill_id}")
        return 1
    
    installed = get_installed_skills()
    if skill_id in installed and not args.force:
        existing = installed[skill_id]
        print_warning(f"Skill already installed: {skill_id}")
        print_info(f"  Location: {existing['path']}")
        print_info(f"  Use --force to reinstall")
        return 0
    
    # Determine installation settings
    project_mode = getattr(args, 'project', False)
    agent = getattr(args, 'agent', 'auto')
    skip_deps = getattr(args, 'no_deps', False)
    
    detected_agent = detect_agent() if agent == "auto" else agent
    location_desc = f"project ({detected_agent})" if project_mode else "global"
    
    # Resolve dependencies
    deps_to_install = {}
    if not skip_deps:
        print_info(f"Resolving dependencies for {skill_id}...")
        deps_to_install, dep_errors = resolve_dependencies(skill_id, catalog, installed)
        
        if dep_errors:
            for err in dep_errors:
                print_warning(err)
            if not args.force:
                print_error("Dependency resolution failed. Use --force to install anyway.")
                return 1
    
    # Show what will be installed
    total_skills = 1 + len(deps_to_install)
    if deps_to_install:
        print(f"\n{Colors.BOLD}Will install {total_skills} skill(s):{Colors.RESET}")
        print(f"  {Colors.CYAN}•{Colors.RESET} {skill_id} {Colors.DIM}(requested){Colors.RESET}")
        for dep_id, dep_info in sorted(deps_to_install.items(), key=lambda x: x[1]["depth"]):
            indent = "  " * dep_info["depth"]
            print(f"  {indent}{Colors.CYAN}•{Colors.RESET} {dep_id} {Colors.DIM}(dependency){Colors.RESET}")
        print()
    
    # Install dependencies first (deepest first)
    sorted_deps = sorted(deps_to_install.items(), key=lambda x: -x[1]["depth"])
    for dep_id, dep_info in sorted_deps:
        if dep_id in installed:
            print_info(f"Dependency already installed: {dep_id}")
            continue
        
        print_info(f"Installing dependency {dep_id}...")
        success, dep_path = install_single_skill(
            dep_info["skill"], catalog,
            version=dep_info.get("version"),
            agent=agent, project=project_mode, force=args.force
        )
        if success:
            print_success(f"Installed {dep_id} → {dep_path}")
    
    # Install main skill
    print_info(f"Installing {skill_id} [{location_desc}]...")
    success, install_path = install_single_skill(
        skill, catalog, version=version,
        agent=agent, project=project_mode, force=args.force
    )
    
    if success:
        print_success(f"Installed {skill_id} → {install_path}")
        track_install(skill_id)  # Track analytics
    
    # Show agent-specific guidance
    profile = AGENT_PROFILES.get(detected_agent, AGENT_PROFILES["generic"])
    if project_mode and profile.get("instructions_file"):
        print_info(f"Tip: Reference this skill in your {profile['instructions_file']}")
    
    return 0


def cmd_uninstall(args):
    """Uninstall a skill."""
    skill_id, _ = parse_skill_spec(args.skill_id)
    installed = get_installed_skills()
    
    if skill_id not in installed:
        print_error(f"Skill not installed: {skill_id}")
        return 1
    
    install_path = Path(installed[skill_id]["path"])
    
    if not args.yes:
        response = input(f"Remove {skill_id} from {install_path}? [y/N] ")
        if response.lower() != "y":
            print_info("Aborted")
            return 0
    
    shutil.rmtree(install_path)
    
    # Clean up empty provider directory
    provider_dir = install_path.parent
    if provider_dir.exists() and not any(provider_dir.iterdir()):
        provider_dir.rmdir()
    
    print_success(f"Uninstalled {skill_id}")
    return 0


def cmd_list(args):
    """List installed skills."""
    installed = get_installed_skills()
    
    if not installed:
        print_info("No skills installed")
        print_info(f"Run 'skills search <query>' to find skills")
        return 0
    
    if args.json:
        print(json.dumps(installed, indent=2))
        return 0
    
    print(f"\n{Colors.BOLD}Installed skills ({len(installed)}):{Colors.RESET}\n")
    
    # Group by location
    by_location = {}
    for skill_id, info in installed.items():
        location = info.get("location", "unknown")
        if location not in by_location:
            by_location[location] = []
        by_location[location].append((skill_id, info))
    
    for location, skills in sorted(by_location.items()):
        print(f"  {Colors.CYAN}[{location}]{Colors.RESET}")
        for skill_id, info in sorted(skills):
            version = info.get("version", "?")
            desc = info.get("manifest", {}).get("description", "")[:45]
            print(f"    {Colors.BOLD}{skill_id}{Colors.RESET}@{version}")
            if desc:
                print(f"    {Colors.DIM}{desc}{Colors.RESET}")
        print()
    
    return 0


def cmd_init(args):
    """Initialize a new skill.json."""
    target_dir = Path(args.path or ".").resolve()
    manifest_path = target_dir / "skill.json"
    
    if manifest_path.exists() and not args.force:
        print_error(f"skill.json already exists at {manifest_path}")
        print_info("Use --force to overwrite")
        return 1
    
    # Interactive prompts
    print(f"{Colors.BOLD}Creating skill.json{Colors.RESET}\n")
    
    name = input(f"skill name ({target_dir.name}): ").strip() or target_dir.name
    name = re.sub(r"[^a-z0-9-]", "-", name.lower())
    
    version = input("version (1.0.0): ").strip() or "1.0.0"
    description = input("description: ").strip()
    author = input("author: ").strip()
    license_id = input("license (MIT): ").strip() or "MIT"
    runtime = input("runtime (universal): ").strip() or "universal"
    keywords = input("keywords (comma-separated): ").strip()
    
    manifest = {
        "name": name,
        "version": version,
        "description": description,
        "author": author or None,
        "license": license_id,
        "runtime": runtime,
        "keywords": [k.strip() for k in keywords.split(",") if k.strip()] if keywords else [],
        "entry": "SKILL.md",
        "dependencies": {},
        "capabilities": [],
        "inputs": [],
        "outputs": []
    }
    
    # Remove None values
    manifest = {k: v for k, v in manifest.items() if v is not None}
    
    target_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2))
    
    # Create SKILL.md template if it doesn't exist
    skill_md_path = target_dir / "SKILL.md"
    if not skill_md_path.exists():
        skill_md_content = f"""---
name: {name}
description: {description}
version: {version}
license: {license_id}
---

# {name}

{description}

## Usage

Describe how to use this skill.

## Examples

```
Example usage here
```

## Configuration

Any configuration options.
"""
        skill_md_path.write_text(skill_md_content)
        print_success(f"Created {skill_md_path}")
    
    print_success(f"Created {manifest_path}")
    return 0


def cmd_update(args):
    """Update installed skills."""
    installed = get_installed_skills()
    
    if not installed:
        print_info("No skills installed")
        return 0
    
    catalog = fetch_catalog(force_refresh=True)
    updates_available = []
    
    for skill_id, info in installed.items():
        skill = find_skill(catalog, skill_id)
        if skill:
            # Check if skill has been updated
            last_updated = skill.get("last_updated_at")
            installed_at = info.get("manifest", {}).get("installed_at")
            
            if last_updated and installed_at and last_updated > installed_at:
                updates_available.append(skill_id)
    
    if not updates_available:
        print_success("All skills are up to date")
        return 0
    
    print(f"\n{Colors.BOLD}Updates available:{Colors.RESET}\n")
    for skill_id in updates_available:
        print(f"  {skill_id}")
    
    if not args.yes:
        response = input(f"\nUpdate {len(updates_available)} skill(s)? [y/N] ")
        if response.lower() != "y":
            print_info("Aborted")
            return 0
    
    for skill_id in updates_available:
        # Simulate args for install
        class InstallArgs:
            skill_id = skill_id
            force = True
        cmd_install(InstallArgs())
    
    return 0


def cmd_config(args):
    """Manage configuration."""
    config = load_config()
    
    if args.action == "list":
        print(json.dumps(config, indent=2))
    elif args.action == "get":
        if args.key in config:
            print(config[args.key])
        else:
            print_error(f"Unknown config key: {args.key}")
            return 1
    elif args.action == "set":
        # Try to parse as JSON, fall back to string
        try:
            value = json.loads(args.value)
        except json.JSONDecodeError:
            value = args.value
        config[args.key] = value
        save_config(config)
        print_success(f"Set {args.key} = {value}")
    
    return 0


def cmd_cache(args):
    """Manage cache."""
    if args.action == "clean":
        if SKILLS_CACHE.exists():
            shutil.rmtree(SKILLS_CACHE)
            SKILLS_CACHE.mkdir()
        print_success("Cache cleared")
    elif args.action == "list":
        if not SKILLS_CACHE.exists():
            print_info("Cache is empty")
            return 0
        total_size = 0
        for f in SKILLS_CACHE.iterdir():
            size = f.stat().st_size
            total_size += size
            print(f"  {f.name} ({size} bytes)")
        print(f"\n  Total: {total_size / 1024:.1f} KB")
    return 0


def cmd_run(args):
    """Run a skill (placeholder for future implementation)."""
    skill_id, _ = parse_skill_spec(args.skill_id)
    installed = get_installed_skills()
    
    if skill_id not in installed:
        print_error(f"Skill not installed: {skill_id}")
        print_info(f"Run: skills install {skill_id}")
        return 1
    
    install_path = Path(installed[skill_id]["path"])
    manifest = installed[skill_id].get("manifest", {})
    
    entry = manifest.get("entry", "SKILL.md")
    entry_path = install_path / entry
    
    if not entry_path.exists():
        print_error(f"Entry point not found: {entry_path}")
        return 1
    
    print_info(f"Skill location: {install_path}")
    print_info(f"Entry point: {entry}")
    print()
    print(f"{Colors.YELLOW}Note: Skill execution requires an AI agent runtime.{Colors.RESET}")
    print(f"Load this skill in your MCP server, LangChain, or other agent framework.")
    print(f"\nSKILL.md content preview:")
    print(f"{Colors.DIM}{'─' * 40}{Colors.RESET}")
    
    content = entry_path.read_text()
    preview = content[:500]
    if len(content) > 500:
        preview += "\n..."
    print(preview)
    
    return 0


def cmd_detect(args):
    """Show detected agent and skill paths."""
    project_path = Path.cwd()
    detected = detect_agent(project_path)
    profile = AGENT_PROFILES.get(detected, AGENT_PROFILES["generic"])
    
    print(f"\n{Colors.BOLD}Agent Detection{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 40}{Colors.RESET}")
    print(f"  {Colors.CYAN}Detected agent:{Colors.RESET}  {profile['name']} ({detected})")
    print(f"  {Colors.CYAN}Project path:{Colors.RESET}    {project_path}")
    
    print(f"\n{Colors.BOLD}Installation Paths{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 40}{Colors.RESET}")
    
    # Project paths
    print(f"\n  {Colors.CYAN}Project paths (--project):{Colors.RESET}")
    for proj_path in profile.get("project_paths", []):
        full_path = project_path / proj_path
        exists = "✓" if full_path.exists() else " "
        print(f"    {Colors.GREEN if full_path.exists() else Colors.DIM}{exists} {full_path}{Colors.RESET}")
    
    # Personal/global path
    personal = profile.get("personal_path", SKILLS_INSTALLED)
    exists = "✓" if personal.exists() else " "
    print(f"\n  {Colors.CYAN}Personal path (--global):{Colors.RESET}")
    print(f"    {Colors.GREEN if personal.exists() else Colors.DIM}{exists} {personal}{Colors.RESET}")
    
    # Instructions file
    if profile.get("instructions_file"):
        inst_file = project_path / profile["instructions_file"]
        exists = "✓" if inst_file.exists() else " "
        print(f"\n  {Colors.CYAN}Instructions file:{Colors.RESET}")
        print(f"    {Colors.GREEN if inst_file.exists() else Colors.DIM}{exists} {inst_file}{Colors.RESET}")
    
    # Show all agents
    print(f"\n{Colors.BOLD}All Supported Agents{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 40}{Colors.RESET}")
    for agent_id, agent_profile in AGENT_PROFILES.items():
        if agent_id == "generic":
            continue
        marker = "→ " if agent_id == detected else "  "
        print(f"  {marker}{Colors.BOLD}{agent_profile['name']}{Colors.RESET} ({agent_id})")
        print(f"      Project: {agent_profile['project_paths'][0]}")
        print(f"      Personal: {agent_profile['personal_path']}")
    
    print()
    return 0


# =============================================================================
# GitHub API helpers for publishing
# =============================================================================

def get_github_token() -> Optional[str]:
    """Get GitHub token from environment or config."""
    # Check environment variables (common CI/CD and local dev patterns)
    for env_var in ["GITHUB_TOKEN", "GH_TOKEN", "GITHUB_PAT"]:
        token = os.environ.get(env_var)
        if token:
            return token
    
    # Check config
    config = load_config()
    token = config.get("github_token")
    if token:
        return token
    
    # Check gh CLI config (macOS/Linux)
    gh_config = Path.home() / ".config" / "gh" / "hosts.yml"
    if gh_config.exists():
        try:
            import yaml
            hosts = yaml.safe_load(gh_config.read_text())
            if hosts and "github.com" in hosts:
                return hosts["github.com"].get("oauth_token")
        except Exception:
            pass
    
    return None


def github_api_request(endpoint: str, method: str = "GET", data: dict = None, token: str = None) -> dict:
    """Make a GitHub API request."""
    url = f"https://api.github.com{endpoint}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": f"skills-cli/{__version__}",
    }
    if token:
        headers["Authorization"] = f"token {token}"
    
    body = None
    if data:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    
    req = Request(url, data=body, headers=headers, method=method)
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_data = json.loads(error_body)
            message = error_data.get("message", str(e))
        except json.JSONDecodeError:
            message = error_body or str(e)
        raise RuntimeError(f"GitHub API error ({e.code}): {message}")


def get_github_user(token: str) -> dict:
    """Get authenticated GitHub user info."""
    return github_api_request("/user", token=token)


def validate_skill_for_publish(skill_dir: Path) -> Tuple[dict, List[str]]:
    """
    Validate a skill directory for publishing.
    Returns (manifest, errors) - empty errors list means valid.
    """
    errors = []
    manifest = {}
    
    # Check skill.json exists
    manifest_path = skill_dir / "skill.json"
    if not manifest_path.exists():
        errors.append("skill.json not found. Run 'skills init' first.")
        return manifest, errors
    
    try:
        manifest = json.loads(manifest_path.read_text())
    except json.JSONDecodeError as e:
        errors.append(f"Invalid skill.json: {e}")
        return manifest, errors
    
    # Required fields
    required_fields = ["name", "version", "description"]
    for field in required_fields:
        if not manifest.get(field):
            errors.append(f"Missing required field in skill.json: {field}")
    
    # Validate name format (lowercase, alphanumeric, hyphens)
    name = manifest.get("name", "")
    if name and not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$", name):
        errors.append(f"Invalid skill name '{name}'. Use lowercase letters, numbers, and hyphens only.")
    
    # Validate version (semver-like)
    version = manifest.get("version", "")
    if version and not re.match(r"^\d+\.\d+\.\d+(-[\w.]+)?$", version):
        errors.append(f"Invalid version '{version}'. Use semver format (e.g., 1.0.0)")
    
    # Check SKILL.md exists
    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.exists():
        errors.append("SKILL.md not found. Create a SKILL.md with your skill instructions.")
    else:
        content = skill_md_path.read_text()
        if len(content.strip()) < 50:
            errors.append("SKILL.md is too short. Add meaningful instructions.")
    
    return manifest, errors


def cmd_validate(args):
    """Validate a skill for publishing."""
    from cli.validate import validate_skill_directory, format_validation_result
    
    skill_dir = Path(args.path or ".").resolve()
    
    print(f"\n{Colors.BOLD}Validating Skill{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 40}{Colors.RESET}")
    print(f"  Directory: {skill_dir}")
    
    # Optionally fetch catalog for duplicate checking
    catalog = None
    if not args.skip_catalog:
        try:
            print_info("Fetching catalog for duplicate check...")
            catalog = fetch_catalog()
        except Exception:
            print_warning("Could not fetch catalog, skipping duplicate check")
    
    result = validate_skill_directory(skill_dir, catalog)
    print(format_validation_result(result, verbose=args.verbose))
    
    return 0 if result.is_valid else 1


def cmd_publish(args):
    """Publish a skill to the registry via PR-based submission."""
    from cli.validate import validate_skill_directory, format_validation_result
    
    skill_dir = Path(args.path or ".").resolve()
    
    print(f"\n{Colors.BOLD}Publishing Skill{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 40}{Colors.RESET}")
    
    # Step 1: Comprehensive validation
    print_info("Running validation checks...")
    
    # Fetch catalog for duplicate checking
    catalog = None
    try:
        catalog = fetch_catalog()
    except Exception as e:
        print_warning(f"Could not fetch catalog: {e}")
    
    validation = validate_skill_directory(skill_dir, catalog)
    
    if not validation.is_valid:
        print_error("Validation failed:")
        print(format_validation_result(validation, verbose=True))
        return 1
    
    if validation.warnings:
        print_warning(f"{len(validation.warnings)} warning(s):")
        for warn in validation.warnings:
            print(f"  {Colors.YELLOW}•{Colors.RESET} {warn}")
        print()
        if not args.force:
            response = input("Continue with warnings? [y/N] ")
            if response.lower() != "y":
                print_info("Aborted. Fix warnings and try again.")
                return 0
    
    # Load manifest
    manifest = json.loads((skill_dir / "skill.json").read_text())
    skill_name = manifest["name"]
    skill_version = manifest["version"]
    
    print_success(f"Valid skill: {skill_name}@{skill_version}")
    
    # Step 2: GitHub authentication
    token = get_github_token()
    if not token:
        print_error("GitHub authentication required")
        print()
        print(f"  Run: {Colors.CYAN}skills login{Colors.RESET}")
        return 1
    
    try:
        user = get_github_user(token)
        username = user["login"]
        print_success(f"Authenticated as: {username}")
    except Exception as e:
        print_error(f"Authentication failed: {e}")
        return 1
    
    # Skill ID = github-username/skill-name (unique by GitHub identity)
    skill_id = f"{username}/{skill_name}"
    repo_name = f"skill-{skill_name}"
    
    print_info(f"Skill ID: {Colors.BOLD}{skill_id}{Colors.RESET}")
    
    # Dry run mode
    if args.dry_run:
        print()
        print(f"{Colors.YELLOW}Dry run - would perform:{Colors.RESET}")
        print(f"  1. Create/update repo: github.com/{username}/{repo_name}")
        print(f"  2. Push skill.json, SKILL.md")
        print(f"  3. Create release: v{skill_version}")
        if args.submit:
            print(f"  4. Submit PR/issue to dmgrok/agent_skills_directory")
        return 0
    
    # Step 3: Ensure repository exists
    repo_url = f"https://github.com/{username}/{repo_name}"
    repo_exists = False
    
    try:
        github_api_request(f"/repos/{username}/{repo_name}", token=token)
        repo_exists = True
        print_info(f"Repository: {repo_url}")
    except RuntimeError as e:
        if "404" in str(e):
            repo_exists = False
        else:
            raise
    
    if not repo_exists:
        if not args.yes:
            response = input(f"\nCreate repository '{repo_name}'? [Y/n] ")
            if response.lower() == "n":
                print_info("Aborted.")
                return 0
        
        print_info(f"Creating repository: {repo_name}...")
        try:
            repo_data = github_api_request("/user/repos", method="POST", data={
                "name": repo_name,
                "description": manifest.get("description", f"Agent skill: {skill_name}")[:100],
                "homepage": "https://dmgrok.github.io/agent_skills_directory/",
                "has_issues": True,
                "has_wiki": False,
                "auto_init": False,
            }, token=token)
            print_success(f"Created: {repo_data['html_url']}")
        except Exception as e:
            print_error(f"Failed to create repository: {e}")
            return 1
    
    # Step 4: Push files and create release
    result = cmd_publish_auto(skill_dir, manifest, token, username, repo_name)
    if result != 0:
        return result
    
    # Step 5: Submit to directory (--submit flag)
    if args.submit:
        return cmd_submit_to_directory(token, username, skill_name, repo_name, manifest)
    else:
        print()
        print(f"  {Colors.CYAN}To add to the official directory:{Colors.RESET}")
        print(f"    skills publish --submit")
    
    return 0


def cmd_submit_to_directory(token: str, username: str, skill_name: str, repo_name: str, manifest: dict) -> int:
    """Submit skill to the official directory via issue/PR."""
    
    print()
    print(f"{Colors.BOLD}Submitting to Official Directory{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 40}{Colors.RESET}")
    
    DIRECTORY_REPO = "dmgrok/agent_skills_directory"
    skill_id = f"{username}/{skill_name}"
    
    # Generate provider entry for aggregate.py
    provider_entry = f'''    "{username}": {{
        "name": "{username}",
        "repo": "https://github.com/{username}/{repo_name}",
        "api_tree_url": "https://api.github.com/repos/{username}/{repo_name}/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/{username}/{repo_name}/main",
        "skills_path_prefix": "",  # Root-level SKILL.md
    }},'''
    
    # Create submission issue with all details for review
    pr_title = f"[Skill Submission] {skill_id}"
    pr_body = f"""## New Skill Submission

### Skill Information
| Field | Value |
|-------|-------|
| **Skill ID** | `{skill_id}` |
| **Name** | {manifest.get('name')} |
| **Version** | {manifest.get('version')} |
| **Description** | {manifest.get('description', 'N/A')} |
| **Repository** | https://github.com/{username}/{repo_name} |
| **License** | {manifest.get('license', 'Not specified')} |
| **Runtime** | {manifest.get('runtime', 'universal')} |

### Automated Validation
- ✅ skill.json schema valid
- ✅ SKILL.md exists with content
- ✅ No duplicate skill name detected
- ✅ No secrets detected
- ✅ No malicious patterns detected

### Provider Entry
To add this skill, merge this entry into `PROVIDERS` in `scripts/aggregate.py`:

```python
{provider_entry}
```

### Keywords
`{', '.join(manifest.get('keywords', [])) or 'None specified'}`

### Capabilities
`{', '.join(manifest.get('capabilities', [])) or 'None specified'}`

---
*Submitted via `skills publish --submit` • [View CLI docs](https://dmgrok.github.io/agent_skills_directory/)*
"""
    
    print_info("Creating submission issue...")
    
    try:
        issue_data = github_api_request(
            f"/repos/{DIRECTORY_REPO}/issues",
            method="POST",
            data={
                "title": pr_title,
                "body": pr_body,
                "labels": ["skill-submission", "automated"]
            },
            token=token
        )
        
        print_success("Submission created!")
        print()
        print(f"  {Colors.BLUE}{issue_data['html_url']}{Colors.RESET}")
        print()
        print("  What happens next:")
        print("  1. Automated checks run on your submission")
        print("  2. Maintainers review the skill")
        print("  3. If approved, your skill appears in the next catalog update")
        print()
        print(f"  Track progress: {Colors.BLUE}{issue_data['html_url']}{Colors.RESET}")
        
    except Exception as e:
        print_warning(f"Could not create issue automatically: {e}")
        print()
        print("Please submit manually:")
        print(f"  1. Go to {Colors.BLUE}https://github.com/{DIRECTORY_REPO}/issues/new{Colors.RESET}")
        print(f"  2. Title: {pr_title}")
        print(f"  3. Include your repository URL and skill.json details")
        return 1
    
    return 0
    
    return 0


def cmd_publish_auto(skill_dir: Path, manifest: dict, token: str, username: str, repo_name: str) -> int:
    """Automated publishing: push files and create release."""
    import subprocess
    
    skill_version = manifest["version"]
    
    print()
    print(f"{Colors.BOLD}Auto-publishing...{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 40}{Colors.RESET}")
    
    # Check if git is available
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("Git is required for auto-publishing. Install git first.")
        return 1
    
    # Initialize git if needed
    git_dir = skill_dir / ".git"
    if not git_dir.exists():
        print_info("Initializing git repository...")
        subprocess.run(["git", "init"], cwd=skill_dir, capture_output=True, check=True)
    
    # Set remote
    remote_url = f"https://github.com/{username}/{repo_name}.git"
    result = subprocess.run(["git", "remote", "get-url", "origin"], cwd=skill_dir, capture_output=True)
    if result.returncode != 0:
        print_info(f"Adding remote origin: {remote_url}")
        subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=skill_dir, capture_output=True)
    else:
        current_remote = result.stdout.decode().strip()
        if current_remote != remote_url:
            print_info(f"Updating remote origin to: {remote_url}")
            subprocess.run(["git", "remote", "set-url", "origin", remote_url], cwd=skill_dir, capture_output=True)
    
    # Stage files
    print_info("Staging files...")
    files_to_add = ["skill.json", "SKILL.md"]
    for f in ["scripts", "assets", "references", "README.md", "LICENSE"]:
        if (skill_dir / f).exists():
            files_to_add.append(f)
    
    for f in files_to_add:
        if (skill_dir / f).exists():
            subprocess.run(["git", "add", f], cwd=skill_dir, capture_output=True)
    
    # Check if there are changes to commit
    result = subprocess.run(["git", "status", "--porcelain"], cwd=skill_dir, capture_output=True)
    if result.stdout.strip():
        print_info("Committing changes...")
        subprocess.run(
            ["git", "commit", "-m", f"Release v{skill_version}"],
            cwd=skill_dir,
            capture_output=True
        )
    else:
        print_info("No changes to commit")
    
    # Push to remote
    print_info("Pushing to GitHub...")
    # Configure git to use token for auth
    auth_remote = f"https://{token}@github.com/{username}/{repo_name}.git"
    result = subprocess.run(
        ["git", "push", auth_remote, "HEAD:main", "--force-with-lease"],
        cwd=skill_dir,
        capture_output=True
    )
    if result.returncode != 0:
        # Try without force
        result = subprocess.run(
            ["git", "push", auth_remote, "HEAD:main"],
            cwd=skill_dir,
            capture_output=True
        )
        if result.returncode != 0:
            print_error(f"Push failed: {result.stderr.decode()}")
            return 1
    print_success("Pushed to GitHub")
    
    # Create release via API
    print_info(f"Creating release v{skill_version}...")
    try:
        release_data = github_api_request(
            f"/repos/{username}/{repo_name}/releases",
            method="POST",
            data={
                "tag_name": f"v{skill_version}",
                "name": f"v{skill_version}",
                "body": f"Release of {manifest['name']} v{skill_version}\n\n{manifest.get('description', '')}",
                "draft": False,
                "prerelease": False,
            },
            token=token
        )
        print_success(f"Created release: {release_data['html_url']}")
    except RuntimeError as e:
        if "already_exists" in str(e):
            print_warning(f"Release v{skill_version} already exists")
        else:
            print_error(f"Failed to create release: {e}")
    
    # Final summary
    print()
    print(f"{Colors.GREEN}✓ Published {username}/{manifest['name']}@{skill_version}{Colors.RESET}")
    print()
    print(f"  Repository: {Colors.BLUE}https://github.com/{username}/{repo_name}{Colors.RESET}")
    print(f"  Skill ID:   {Colors.BOLD}{username}/{manifest['name']}{Colors.RESET}")
    print()
    print(f"  To add to the official directory, open a PR:")
    print(f"  {Colors.BLUE}https://github.com/dmgrok/agent_skills_directory{Colors.RESET}")
    
    return 0


def cmd_login(args):
    """Authenticate with GitHub."""
    print(f"\n{Colors.BOLD}GitHub Authentication{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 40}{Colors.RESET}")
    
    # Check existing auth
    existing_token = get_github_token()
    if existing_token and not args.force:
        try:
            user = get_github_user(existing_token)
            print_success(f"Already authenticated as: {user['login']}")
            print_info("Use --force to re-authenticate")
            return 0
        except Exception:
            pass  # Token invalid, continue to login
    
    print()
    print("Enter a GitHub Personal Access Token (PAT).")
    print(f"Create one at: {Colors.BLUE}https://github.com/settings/tokens/new{Colors.RESET}")
    print("Required scopes: repo (or public_repo for public repos only)")
    print()
    
    token = input("Token: ").strip()
    if not token:
        print_error("No token provided")
        return 1
    
    # Validate token
    try:
        user = get_github_user(token)
        username = user["login"]
    except Exception as e:
        print_error(f"Invalid token: {e}")
        return 1
    
    # Save to config
    config = load_config()
    config["github_token"] = token
    config["github_user"] = username
    save_config(config)
    
    print_success(f"Authenticated as: {username}")
    print_info("Token saved to ~/.skills/config.json")
    
    return 0


def cmd_whoami(args):
    """Show authenticated GitHub user."""
    token = get_github_token()
    if not token:
        print_error("Not authenticated. Run 'skills login' first.")
        return 1
    
    try:
        user = get_github_user(token)
        print(f"\n{Colors.BOLD}Authenticated as:{Colors.RESET}")
        print(f"  Username: {Colors.GREEN}{user['login']}{Colors.RESET}")
        if user.get("name"):
            print(f"  Name:     {user['name']}")
        if user.get("email"):
            print(f"  Email:    {user['email']}")
        print(f"  Profile:  {Colors.BLUE}{user['html_url']}{Colors.RESET}")
        print()
    except Exception as e:
        print_error(f"Authentication failed: {e}")
        return 1
    
    return 0


# =============================================================================
# Analytics and Stats
# =============================================================================

STATS_FILE = SKILLS_HOME / "stats.json"


def load_stats() -> Dict[str, Any]:
    """Load local analytics stats."""
    if STATS_FILE.exists():
        try:
            return json.loads(STATS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {"installs": {}, "searches": {}, "total_installs": 0}


def save_stats(stats: Dict[str, Any]):
    """Save local analytics stats."""
    ensure_dirs()
    STATS_FILE.write_text(json.dumps(stats, indent=2))


def track_install(skill_id: str):
    """Track a skill installation."""
    stats = load_stats()
    
    if skill_id not in stats["installs"]:
        stats["installs"][skill_id] = {"count": 0, "first": None, "last": None}
    
    stats["installs"][skill_id]["count"] += 1
    stats["installs"][skill_id]["last"] = datetime.now().isoformat()
    if not stats["installs"][skill_id]["first"]:
        stats["installs"][skill_id]["first"] = stats["installs"][skill_id]["last"]
    
    stats["total_installs"] = stats.get("total_installs", 0) + 1
    
    save_stats(stats)


def track_search(query: str):
    """Track a search query."""
    stats = load_stats()
    
    query_lower = query.lower()
    if query_lower not in stats["searches"]:
        stats["searches"][query_lower] = 0
    stats["searches"][query_lower] += 1
    
    save_stats(stats)


def cmd_stats(args):
    """Show analytics and statistics."""
    print(f"\n{Colors.BOLD}Skills Statistics{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 50}{Colors.RESET}")
    
    # Local stats
    stats = load_stats()
    installed = get_installed_skills()
    
    print(f"\n{Colors.CYAN}Local Statistics:{Colors.RESET}")
    print(f"  Installed skills:    {len(installed)}")
    print(f"  Total installs:      {stats.get('total_installs', 0)}")
    print(f"  Unique searches:     {len(stats.get('searches', {}))}")
    
    # Most installed locally
    if stats.get("installs"):
        print(f"\n{Colors.CYAN}Most Installed (local):{Colors.RESET}")
        sorted_installs = sorted(
            stats["installs"].items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )[:5]
        for skill_id, data in sorted_installs:
            print(f"  {skill_id}: {data['count']} install(s)")
    
    # Catalog stats
    try:
        catalog = fetch_catalog()
        
        print(f"\n{Colors.CYAN}Catalog Statistics:{Colors.RESET}")
        print(f"  Total skills:        {len(catalog.get('skills', []))}")
        print(f"  Providers:           {len(catalog.get('providers', {}))}")
        print(f"  Catalog version:     {catalog.get('version', 'unknown')}")
        
        # Category breakdown
        categories = {}
        for skill in catalog.get("skills", []):
            cat = skill.get("category", "other")
            categories[cat] = categories.get(cat, 0) + 1
        
        if categories:
            print(f"\n{Colors.CYAN}Skills by Category:{Colors.RESET}")
            for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
                bar = "█" * min(count, 30)
                print(f"  {cat:15} {count:3} {Colors.GREEN}{bar}{Colors.RESET}")
        
        # Provider stats with GitHub stars
        providers = catalog.get("providers", {})
        if providers and args.detailed:
            print(f"\n{Colors.CYAN}Top Providers by Stars:{Colors.RESET}")
            sorted_providers = sorted(
                providers.items(),
                key=lambda x: x[1].get("stars") or 0,
                reverse=True
            )[:10]
            for provider_id, info in sorted_providers:
                stars = info.get("stars") or 0
                skill_count = sum(1 for s in catalog.get("skills", []) if s.get("provider") == provider_id)
                print(f"  {provider_id:25} ⭐ {stars:,}  ({skill_count} skills)")
        
    except Exception as e:
        print_warning(f"Could not fetch catalog stats: {e}")
    
    # Recent activity
    if stats.get("installs"):
        recent = sorted(
            [(sid, data) for sid, data in stats["installs"].items() if data.get("last")],
            key=lambda x: x[1]["last"],
            reverse=True
        )[:5]
        
        if recent:
            print(f"\n{Colors.CYAN}Recent Installs:{Colors.RESET}")
            for skill_id, data in recent:
                last = data["last"][:10] if data.get("last") else "unknown"
                print(f"  {skill_id} ({last})")
    
    print()
    return 0


def analyze_project_structure(project_path: Path) -> Dict[str, Any]:
    """Analyze project structure to understand what technologies and frameworks are used."""
    analysis = {
        "languages": set(),
        "frameworks": set(),
        "tools": set(),
        "file_types": set(),
        "package_files": []
    }
    
    # Common patterns to identify technologies
    tech_patterns = {
        "python": ["*.py", "requirements.txt", "setup.py", "pyproject.toml", "Pipfile"],
        "javascript": ["*.js", "package.json", "*.ts", "*.jsx", "*.tsx"],
        "java": ["*.java", "pom.xml", "build.gradle"],
        "go": ["*.go", "go.mod"],
        "rust": ["*.rs", "Cargo.toml"],
        "ruby": ["*.rb", "Gemfile"],
        "php": ["*.php", "composer.json"],
        "c++": ["*.cpp", "*.hpp", "CMakeLists.txt"],
        "c": ["*.c", "*.h", "Makefile"],
    }
    
    framework_patterns = {
        "react": ["package.json"],
        "vue": ["package.json"],
        "angular": ["angular.json"],
        "django": ["manage.py", "settings.py"],
        "flask": ["app.py"],
        "fastapi": ["main.py"],
        "express": ["package.json"],
        "nextjs": ["next.config.js", "next.config.ts"],
        "gatsby": ["gatsby-config.js"],
    }
    
    try:
        # Walk project directory (limit depth to avoid very deep recursion)
        for root, dirs, files in os.walk(project_path):
            # Skip common ignored directories
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '.venv', 
                                                     '__pycache__', 'dist', 'build', '.next', 
                                                     'target', 'vendor'}]
            
            # Check relative depth
            rel_path = Path(root).relative_to(project_path)
            if len(rel_path.parts) > 3:
                continue
            
            for file in files:
                file_path = Path(root) / file
                suffix = file_path.suffix.lower()
                
                # Track file types
                if suffix:
                    analysis["file_types"].add(suffix)
                
                # Check language patterns
                for lang, patterns in tech_patterns.items():
                    for pattern in patterns:
                        if file_path.match(pattern):
                            analysis["languages"].add(lang)
                            if file in ["package.json", "requirements.txt", "Cargo.toml", "go.mod", "pom.xml"]:
                                analysis["package_files"].append(str(file_path))
                
                # Check framework patterns
                for framework, patterns in framework_patterns.items():
                    for pattern in patterns:
                        if file_path.match(pattern):
                            analysis["frameworks"].add(framework)
    
    except Exception as e:
        print_warning(f"Error analyzing project: {e}")
    
    # Convert sets to lists for JSON serialization
    analysis["languages"] = list(analysis["languages"])
    analysis["frameworks"] = list(analysis["frameworks"])
    analysis["tools"] = list(analysis["tools"])
    analysis["file_types"] = list(analysis["file_types"])
    
    return analysis


def find_readme(project_path: Path) -> Optional[Path]:
    """Find README file in project directory."""
    readme_patterns = ["README.md", "README.MD", "readme.md", "README", "README.txt"]
    
    for pattern in readme_patterns:
        readme_path = project_path / pattern
        if readme_path.exists() and readme_path.is_file():
            return readme_path
    
    return None


def count_similar_skills(skill: Dict, all_skills: List[Dict]) -> int:
    """Count how many similar skills exist in the catalog."""
    skill_name = skill["name"].lower()
    skill_desc = skill.get("description", "").lower()
    skill_tags = set(t.lower() for t in skill.get("tags", []))
    skill_category = skill.get("category", "").lower()
    skill_id = skill["id"]
    
    similar_count = 0
    
    for other_skill in all_skills:
        if other_skill["id"] == skill_id:
            continue
        
        other_name = other_skill["name"].lower()
        other_desc = other_skill.get("description", "").lower()
        other_tags = set(t.lower() for t in other_skill.get("tags", []))
        other_category = other_skill.get("category", "").lower()
        
        similarity_score = 0
        
        # Same category
        if skill_category and skill_category == other_category:
            similarity_score += 1
        
        # Tag overlap
        tag_overlap = len(skill_tags & other_tags)
        if tag_overlap >= 2:
            similarity_score += 2
        elif tag_overlap >= 1:
            similarity_score += 1
        
        # Name similarity (common words)
        skill_words = set(skill_name.split())
        other_words = set(other_name.split())
        name_overlap = len(skill_words & other_words)
        if name_overlap >= 2:
            similarity_score += 2
        elif name_overlap >= 1:
            similarity_score += 1
        
        # Description keyword overlap
        skill_desc_words = set(extract_keywords(skill_desc))
        other_desc_words = set(extract_keywords(other_desc))
        desc_overlap = len(skill_desc_words & other_desc_words)
        if desc_overlap >= 3:
            similarity_score += 1
        
        # Consider similar if score >= 3
        if similarity_score >= 3:
            similar_count += 1
    
    return similar_count


def extract_keywords(text: str, min_length: int = 3) -> set:
    """Extract meaningful keywords from text."""
    # Remove markdown, code blocks, URLs
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', ' ', text)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Extract words
    words = re.findall(r'\b[a-z][a-z0-9_-]*\b', text.lower())
    
    # Common stop words to exclude
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
        'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each',
        'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
        'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'use',
        'using', 'used', 'make', 'made', 'get', 'set', 'put', 'new', 'also'
    }
    
    keywords = {w for w in words if len(w) >= min_length and w not in stop_words}
    return keywords


def prefilter_skills_by_relevance(
    skills: List[Dict],
    readme_content: str,
    analysis: Dict,
    top_n: int = 30
) -> List[Dict]:
    """
    Pre-filter catalog to top N most relevant skills before LLM analysis.
    This dramatically reduces the context size sent to LLM.
    """
    # Extract keywords from README
    readme_keywords = extract_keywords(readme_content) if readme_content else set()
    
    # Extract context from project structure
    languages = set(l.lower() for l in analysis.get("languages", []))
    frameworks = set(f.lower() for f in analysis.get("frameworks", []))
    file_exts = set(analysis.get("file_types", []))
    
    # Build combined context keywords
    context_keywords = readme_keywords | languages | frameworks
    
    # Score each skill
    scored_skills = []
    for skill in skills:
        score = 0
        skill_name = skill["name"].lower()
        skill_desc = skill.get("description", "").lower()
        skill_tags = [t.lower() for t in skill.get("tags", [])]
        skill_category = skill.get("category", "").lower()
        
        # Build skill searchable text
        skill_text = f"{skill_name} {skill_desc} {' '.join(skill_tags)} {skill_category}"
        skill_words = set(extract_keywords(skill_text))
        
        # Keyword overlap score (most important)
        overlap = context_keywords & skill_words
        score += len(overlap) * 10
        
        # Direct keyword matches get bonus
        for keyword in readme_keywords:
            if len(keyword) > 4 and keyword in skill_text:
                score += 20
        
        # Language exact matches
        for lang in languages:
            if lang in skill_tags or lang in skill_name:
                score += 15
        
        # Framework exact matches
        for framework in frameworks:
            if framework in skill_text:
                score += 15
        
        # Quality and maintenance bonus
        quality = skill.get("quality_score", 0)
        if quality >= 80:
            score += 5
        elif quality >= 60:
            score += 2
        
        maint = skill.get("maintenance_status", "")
        if maint == "active":
            score += 3
        elif maint == "maintained":
            score += 1
        
        # Category relevance
        if readme_content:
            if "api" in readme_keywords or "rest" in readme_keywords:
                if "api" in skill_text or "rest" in skill_text:
                    score += 5
            if "database" in readme_keywords or "db" in readme_keywords:
                if "database" in skill_text or "sql" in skill_text:
                    score += 5
            if "test" in readme_keywords or "testing" in readme_keywords:
                if "test" in skill_text:
                    score += 5
        
        if score > 0:
            scored_skills.append((score, skill))
    
    # Sort by score and return top N
    scored_skills.sort(key=lambda x: (-x[0], -x[1].get("quality_score", 0)))
    return [skill for score, skill in scored_skills[:top_n]]


def cmd_suggest(args):
    """Use LLM to suggest relevant skills based on project README and catalog."""
    project_path = Path(args.path or Path.cwd())
    
    if not project_path.exists():
        print_error(f"Project path does not exist: {project_path}")
        return 1
    
    print_info("Analyzing project...")
    
    # Find and read README
    readme_path = find_readme(project_path)
    readme_content = ""
    
    if readme_path:
        try:
            readme_content = readme_path.read_text(encoding='utf-8', errors='ignore')
            # Truncate if too long (keep first 8000 chars for context)
            if len(readme_content) > 8000:
                readme_content = readme_content[:8000] + "\n\n[... truncated for length ...]"
            print_info(f"Found README: {readme_path.name}")
        except Exception as e:
            print_warning(f"Could not read README: {e}")
    else:
        print_warning("No README found. Analysis will be limited.")
    
    # Analyze project structure
    analysis = analyze_project_structure(project_path)
    
    if args.verbose:
        print(f"\n{Colors.DIM}Project Analysis:{Colors.RESET}")
        print(f"  Languages: {', '.join(analysis['languages']) or 'None detected'}")
        print(f"  Frameworks: {', '.join(analysis['frameworks']) or 'None detected'}")
        print(f"  File types: {', '.join(list(analysis['file_types'])[:15])}")
        if readme_path:
            print(f"  README: {readme_path.name} ({len(readme_content)} chars)")
        print()
    
    # Fetch catalog
    try:
        catalog = fetch_catalog()
    except Exception as e:
        print_error(f"Failed to fetch catalog: {e}")
        return 1
    
    skills_list = catalog.get("skills", [])
    print_info(f"Analyzing against {len(skills_list)} skills from catalog...")
    
    # Pre-filter to most relevant skills (dramatically reduces LLM context)
    relevant_skills = prefilter_skills_by_relevance(skills_list, readme_content, analysis, top_n=30)
    
    if args.verbose:
        efficiency = (1 - len(relevant_skills) / len(skills_list)) * 100
        print(f"{Colors.DIM}Pre-filtered to {len(relevant_skills)} most relevant skills ({efficiency:.0f}% reduction){Colors.RESET}")
    
    # Prepare compact skills summary for LLM
    skills_summary = []
    for skill in relevant_skills:
        skills_summary.append({
            "id": skill["id"],
            "name": skill["name"],
            "description": skill.get("description", "")[:150],  # Truncate long descriptions
            "category": skill.get("category", ""),
            "tags": skill.get("tags", [])[:5],  # Limit tags
            "quality_score": skill.get("quality_score", 0),
            "maintenance_status": skill.get("maintenance_status", "unknown")
        })
    
    # Build prompt for LLM analysis
    prompt = f"""Analyze this software project and recommend the most relevant AI agent skills from the catalog.

PROJECT README:
{readme_content[:4000] if readme_content else 'No README available'}
{' [... truncated for length ...]' if len(readme_content) > 4000 else ''}

PROJECT STRUCTURE:
- Languages detected: {', '.join(analysis['languages']) or 'None'}
- Frameworks detected: {', '.join(analysis['frameworks']) or 'None'}
- File types: {', '.join(list(analysis['file_types'])[:20])}

RELEVANT SKILLS (pre-filtered from {len(skills_list)} total skills):
{json.dumps(skills_summary, indent=2)}

TASK:
Based on the README and project structure, recommend 5-10 skills from the list above.

CONSIDERATIONS:
1. README describes the project's purpose, features, and tech stack
2. Match skills to the project's actual needs and domain
3. Prefer high quality_score (80+) and maintenance_status "active"
4. Only recommend skills from the list above

RESPONSE FORMAT (JSON only):
{{
  "project_summary": "Brief 1-2 sentence description of what this project does",
  "recommendations": [
    {{
      "skill_id": "exact-provider/skill-name-from-list",
      "reason": "Why this skill is relevant (be specific to the project)",
      "confidence": "high|medium|low"
    }}
  ]
}}"""

    # Use enhanced heuristic search (fast, accurate, no LLM needed)
    project_summary = None
    recommendations = generate_enhanced_recommendations(
        relevant_skills, 
        readme_content, 
        analysis, 
        top_n=10
    )
    
    # Optional: Try LLM enhancement if --llm flag is set (future feature)
    if getattr(args, 'use_llm', False):
        try:
            print_info("Enhancing with LLM analysis via Perplexity...")
            
            result = mcp_perplexity_perplexity_reason(
                messages=[{"role": "user", "content": prompt}],
                strip_thinking=True
            )
            
            response_text = result.get("content", "")
            json_match = re.search(r'```json\s*({.*?})\s*```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)
            
            parsed = json.loads(response_text)
            llm_recommendations = parsed.get("recommendations", [])
            project_summary = parsed.get("project_summary")
            
            if llm_recommendations:
                recommendations = llm_recommendations
                print_success("LLM enhancement completed")
                
        except Exception as e:
            if args.verbose:
                print_warning(f"LLM enhancement skipped: {e}")
    
    # Display recommendations
    if not recommendations:
        print_warning("No skill recommendations found for this project.")
        return 0
    
    # Show project summary if available
    if project_summary:
        print(f"\n{Colors.BOLD}Project Summary:{Colors.RESET}")
        print(f"{Colors.DIM}{project_summary}{Colors.RESET}\n")
    
    print(f"{Colors.BOLD}Recommended Skills for Your Project:{Colors.RESET}\n")
    
    # Calculate similar skills for each recommendation
    similar_counts = {}
    for rec in recommendations:
        skill = find_skill(catalog, rec["skill_id"])
        if skill:
            similar_count = count_similar_skills(skill, skills_list)
            similar_counts[rec["skill_id"]] = similar_count
    
    for i, rec in enumerate(recommendations, 1):
        skill_id = rec["skill_id"]
        reason = rec["reason"]
        confidence = rec.get("confidence", "medium")
        
        # Get full skill details
        skill = find_skill(catalog, skill_id)
        if not skill:
            continue
        
        confidence_color = {
            "high": Colors.GREEN,
            "medium": Colors.YELLOW,
            "low": Colors.DIM
        }.get(confidence, Colors.RESET)
        
        # Quality and maintenance indicators
        quality_score = skill.get("quality_score", 0)
        if quality_score >= 80:
            quality_badge = f"{Colors.GREEN}⭐{quality_score}{Colors.RESET}"
            quality_label = f"{Colors.GREEN}High Quality{Colors.RESET}"
        elif quality_score >= 60:
            quality_badge = f"{Colors.YELLOW}⭐{quality_score}{Colors.RESET}"
            quality_label = f"{Colors.YELLOW}Good Quality{Colors.RESET}"
        else:
            quality_badge = f"{Colors.DIM}⭐{quality_score}{Colors.RESET}"
            quality_label = f"{Colors.DIM}Quality: {quality_score}{Colors.RESET}"
        
        maint_status = skill.get("maintenance_status", "unknown")
        maint_emoji = {"active": "🟢", "maintained": "🟡", "stale": "🟠", "abandoned": "🔴"}.get(maint_status, "⚪")
        maint_label = maint_status.capitalize()
        
        days_since = skill.get("days_since_update")
        if days_since is not None:
            if days_since < 30:
                days_label = f"{Colors.GREEN}{days_since}d ago{Colors.RESET}"
            elif days_since < 180:
                days_label = f"{Colors.YELLOW}{days_since}d ago{Colors.RESET}"
            else:
                days_label = f"{Colors.DIM}{days_since}d ago{Colors.RESET}"
        else:
            days_label = ""
        
        # Similar skills count
        similar_count = similar_counts.get(skill_id, 0)
        similar_label = f"{Colors.CYAN}{similar_count} similar{Colors.RESET}" if similar_count > 0 else ""
        
        # Header line
        print(f"  {Colors.BOLD}{i}. {skill_id}{Colors.RESET} {quality_badge} {confidence_color}({confidence}){Colors.RESET}")
        
        # Description
        print(f"     {Colors.DIM}{skill.get('description', 'No description')[:80]}{Colors.RESET}")
        
        # Metrics line
        metrics_parts = []
        metrics_parts.append(f"{maint_emoji} {maint_label}")
        if days_label:
            metrics_parts.append(f"Updated: {days_label}")
        metrics_parts.append(quality_label)
        if similar_label:
            metrics_parts.append(similar_label)
        print(f"     {Colors.DIM}│{Colors.RESET} {f' {Colors.DIM}•{Colors.RESET} '.join(metrics_parts)}")
        
        # Reason
        print(f"     {Colors.CYAN}→{Colors.RESET} {reason}")
        print()
    
    # Show installation command
    print(f"{Colors.DIM}To install a skill:{Colors.RESET}")
    print(f"  skillsdir install <skill-id>")
    print()
    
    return 0


def generate_enhanced_recommendations(
    skills: List[Dict],
    readme_content: str,
    analysis: Dict,
    top_n: int = 10
) -> List[Dict]:
    """
    Generate high-quality skill recommendations using enhanced heuristics.
    No LLM needed - uses sophisticated scoring algorithm.
    """
    readme_lower = readme_content.lower() if readme_content else ""
    readme_keywords = extract_keywords(readme_content) if readme_content else set()
    
    languages = set(l.lower() for l in analysis.get("languages", []))
    frameworks = set(f.lower() for f in analysis.get("frameworks", []))
    file_types = set(analysis.get("file_types", []))
    
    scored_skills = []
    
    for skill in skills:
        score = 0
        reasons = []
        
        skill_id = skill["id"]
        skill_name = skill["name"].lower()
        skill_desc = skill.get("description", "").lower()
        skill_tags = [t.lower() for t in skill.get("tags", [])]
        skill_category = skill.get("category", "").lower()
        
        # Primary matching: README keywords
        if readme_keywords:
            # Exact keyword matches in skill name (highest weight)
            name_words = set(skill_name.split())
            name_matches = readme_keywords & name_words
            if name_matches:
                score += 30
                reasons.append(f"name matches: {', '.join(list(name_matches)[:2])}")
            
            # Keyword matches in tags (high weight)
            tag_matches = readme_keywords & set(skill_tags)
            if tag_matches:
                score += 25
                reasons.append(f"tags match: {', '.join(list(tag_matches)[:2])}")
            
            # Keyword matches in description (medium weight)
            desc_words = set(extract_keywords(skill_desc))
            desc_matches = readme_keywords & desc_words
            if len(desc_matches) >= 2:
                score += 15
                reasons.append(f"{len(desc_matches)} keyword matches")
        
        # Language/framework matching
        for lang in languages:
            if lang in skill_tags:
                score += 20
                reasons.append(f"supports {lang}")
                break
            elif lang in skill_name or lang in skill_desc:
                score += 10
                reasons.append(f"mentions {lang}")
                break
        
        for framework in frameworks:
            if framework in skill_tags or framework in skill_name:
                score += 20
                reasons.append(f"supports {framework}")
                break
            elif framework in skill_desc:
                score += 10
                reasons.append(f"mentions {framework}")
                break
        
        # Domain-specific matching (from README context)
        if readme_lower:
            domain_keywords = {
                'api': ['api', 'rest', 'graphql', 'endpoint', 'swagger'],
                'database': ['database', 'sql', 'postgres', 'mysql', 'mongodb', 'redis'],
                'testing': ['test', 'testing', 'pytest', 'jest', 'cypress'],
                'devops': ['docker', 'kubernetes', 'deploy', 'ci/cd', 'github-actions'],
                'frontend': ['react', 'vue', 'angular', 'frontend', 'ui', 'component'],
                'backend': ['backend', 'server', 'express', 'fastapi', 'django'],
                'ml': ['machine-learning', 'ml', 'tensorflow', 'pytorch', 'model'],
                'docs': ['documentation', 'docs', 'readme', 'markdown']
            }
            
            for domain, keywords in domain_keywords.items():
                readme_has_domain = any(kw in readme_lower for kw in keywords)
                skill_in_domain = any(kw in skill_name or kw in skill_desc or kw in skill_tags for kw in keywords)
                
                if readme_has_domain and skill_in_domain:
                    score += 15
                    reasons.append(f"{domain} domain match")
                    break
        
        # Quality and maintenance scoring
        quality = skill.get("quality_score", 0)
        if quality >= 80:
            score += 10
            reasons.append("high quality")
        elif quality >= 60:
            score += 5
        
        maint = skill.get("maintenance_status", "")
        if maint == "active":
            score += 8
            reasons.append("actively maintained")
        elif maint == "maintained":
            score += 4
        
        # Category relevance bonuses
        if skill_category:
            if languages and skill_category == "development":
                score += 5
            if file_types and any(ext in ['.json', '.yaml', '.toml', '.xml'] for ext in file_types):
                if skill_category == "data":
                    score += 5
            if readme_lower and 'document' in readme_lower and skill_category == "documents":
                score += 5
        
        # Provider trust score (official providers get slight boost)
        provider = skill_id.split('/')[0]
        trusted_providers = {
            'anthropics', 'openai', 'github', 'vercel', 'cloudflare',
            'stripe', 'supabase', 'huggingface'
        }
        if provider in trusted_providers:
            score += 3
        
        if score > 0:
            # Determine confidence level
            if score >= 50:
                confidence = "high"
            elif score >= 30:
                confidence = "medium"
            else:
                confidence = "low"
            
            scored_skills.append({
                "score": score,
                "skill": skill,
                "reasons": reasons,
                "confidence": confidence
            })
    
    # Sort by score and quality
    scored_skills.sort(key=lambda x: (-x["score"], -x["skill"].get("quality_score", 0)))
    
    # Convert to recommendation format
    recommendations = []
    for item in scored_skills[:top_n]:
        reason = "; ".join(item["reasons"][:3]) if item["reasons"] else "General utility"
        recommendations.append({
            "skill_id": item["skill"]["id"],
            "reason": reason,
            "confidence": item["confidence"],
            "score": item["score"]  # Include for debugging
        })
    
    return recommendations


def generate_heuristic_suggestions(analysis: Dict, skills: List[Dict], readme_content: str = "") -> List[Dict]:
    """
    Legacy heuristic function - now redirects to enhanced version.
    Kept for backward compatibility.
    """
    return generate_enhanced_recommendations(skills, readme_content, analysis, top_n=10)


def cmd_export(args):
    """Export installed skills to various formats."""
    from cli.loader import load_skills_from_dir, Skill
    
    # Determine skills directory
    if args.skills_dir:
        skills_dir = Path(args.skills_dir)
    else:
        # Collect skills from all installed locations
        skills_dir = None
    
    # Load skills
    skills = []
    if skills_dir:
        skills = load_skills_from_dir(skills_dir)
    else:
        # Load from all installed locations
        for location_type, path in get_all_install_locations():
            skills.extend(load_skills_from_dir(path))
    
    if not skills:
        print_warning("No skills found to export")
        return 0
    
    print_info(f"Exporting {len(skills)} skill(s) as {args.format}...")
    
    # Generate output based on format
    output = ""
    
    if args.format == "mcp":
        resources = [s.to_mcp() for s in skills]
        output = json.dumps({"resources": resources}, indent=2)
    
    elif args.format == "langchain":
        tools = [s.to_langchain_tool() for s in skills]
        output = json.dumps({"tools": tools}, indent=2)
    
    elif args.format == "crewai":
        agents = [s.to_crewai_agent() for s in skills]
        output = json.dumps({"agents": agents}, indent=2)
    
    elif args.format == "autogen":
        agents = [s.to_autogen_agent() for s in skills]
        output = json.dumps({"agents": agents}, indent=2)
    
    elif args.format == "openai":
        assistants = [s.to_openai_assistant() for s in skills]
        output = json.dumps({"assistants": assistants}, indent=2)
    
    elif args.format == "anthropic":
        all_tools = []
        for s in skills:
            all_tools.extend(s.to_anthropic_tools())
        output = json.dumps({"tools": all_tools}, indent=2)
    
    elif args.format == "prompt":
        parts = ["# Loaded Skills", ""]
        for skill in skills:
            parts.append(skill.to_system_prompt())
            parts.append("")
            parts.append("---")
            parts.append("")
        output = "\n".join(parts)
    
    elif args.format == "copilot":
        parts = ["# Skills for GitHub Copilot", ""]
        parts.append("The following skills are available. Use them as reference for completing tasks.")
        parts.append("")
        for skill in skills:
            parts.append(f"## {skill.name}")
            parts.append("")
            if skill.description:
                parts.append(f"> {skill.description}")
                parts.append("")
            parts.append(skill.instructions)
            parts.append("")
        output = "\n".join(parts)
    
    elif args.format == "claude":
        parts = ["# Agent Skills", ""]
        parts.append("You have access to the following skills:")
        parts.append("")
        for skill in skills:
            parts.append(f"## {skill.name} (v{skill.version})")
            parts.append("")
            if skill.description:
                parts.append(f"*{skill.description}*")
                parts.append("")
            parts.append(skill.instructions)
            parts.append("")
        output = "\n".join(parts)
    
    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output)
        print_success(f"Exported to {output_path}")
    else:
        print(output)
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="skillsdir",
        description="Informed discoverability for AI agent skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Informed Discoverability - Find the RIGHT skills for your project:

  🎯 Quality scored (LGTM validation)
  📊 Maintenance tracked (🟢 Active vs 🔴 Abandoned)
  🛡️ Security validated (secrets + injection scanning)

Examples:
  skillsdir search "pdf extraction"    # Find skills with quality insights
  skillsdir info anthropic/pdf         # See: 🟢 Active, LGTM 87/100, ✓ Security
  
  # Make informed decision, then install via skills.sh:
  skills.sh install anthropic/pdf      # The actual package manager

Problem: skills.sh has 30K+ skills. Which ones should you use?
Solution: We provide quality metrics to make informed decisions.
"""
    )
    parser.add_argument("-v", "--version", action="version", version=f"skillsdir {__version__}")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # search
    p_search = subparsers.add_parser("search", help="Search for skills")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--limit", "-l", type=int, help="Max results to show")
    p_search.set_defaults(func=cmd_search)
    
    # info
    p_info = subparsers.add_parser("info", help="Show skill information")
    p_info.add_argument("skill_id", help="Skill ID (e.g., anthropic/web-researcher)")
    p_info.set_defaults(func=cmd_info)
    
    # suggest
    p_suggest = subparsers.add_parser("suggest", help="Get AI-powered skill recommendations for your project",
        description="""Analyze your project and get intelligent recommendations for relevant skills.

This command uses a sophisticated scoring algorithm to match your project with skills from
the catalog. No LLM required - works entirely locally with excellent results.

The algorithm considers:
- README content and keywords
- Project languages and frameworks  
- File types and structure
- Skill quality scores and maintenance status
- Domain-specific patterns (API, database, testing, etc.)

Examples:
  skillsdir suggest                    # Analyze current directory
  skillsdir suggest /path/to/project   # Analyze specific project
  skillsdir suggest --verbose          # Show detailed analysis
  skillsdir suggest --llm              # Enhance with LLM (requires MCP)
""")
    p_suggest.add_argument("path", nargs="?", help="Project directory (default: current directory)")
    p_suggest.add_argument("--verbose", "-v", action="store_true", help="Show detailed project analysis")
    p_suggest.add_argument("--llm", action="store_true", dest="use_llm", help="Enhance with LLM analysis (optional, requires Perplexity MCP)")
    p_suggest.set_defaults(func=cmd_suggest)
    
    # install
    p_install = subparsers.add_parser("install", help="Install a skill",
        description="""Install a skill to your project or globally.

By default, skills are installed globally to ~/.skills/installed/.
Use --project to install to your current project's skills directory.
Use --agent to specify which agent's path to use (auto-detected by default).

Examples:
  skills install anthropic/pdf                    # Global install
  skills install anthropic/pdf -p                 # Install to project (auto-detect agent)
  skills install anthropic/pdf -p --agent claude  # Install to .claude/skills/
  skills install anthropic/pdf -p --agent copilot # Install to .github/skills/
  skills install anthropic/pdf -p --agent codex   # Install to .codex/skills/
  skills install anthropic/pdf -p --agent cursor  # Install to .cursor/skills/
  skills install anthropic/pdf --no-deps          # Skip dependency installation
""")
    p_install.add_argument("skill_id", help="Skill ID (e.g., anthropic/web-researcher[@version])")
    p_install.add_argument("--force", "-f", action="store_true", help="Force reinstall")
    p_install.add_argument("--project", "-p", action="store_true", 
                          help="Install to project skills directory (e.g., .github/skills/, .claude/skills/)")
    p_install.add_argument("--global", "-g", dest="global_install", action="store_true",
                          help="Install globally to ~/.skills/ (default)")
    p_install.add_argument("--agent", choices=["auto", "claude", "copilot", "codex", "cursor", "generic"],
                          default="auto", help="Target agent (auto-detected by default)")
    p_install.add_argument("--no-deps", action="store_true", help="Skip dependency installation")
    p_install.set_defaults(func=cmd_install)
    
    # uninstall
    p_uninstall = subparsers.add_parser("uninstall", help="Uninstall a skill")
    p_uninstall.add_argument("skill_id", help="Skill ID")
    p_uninstall.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    p_uninstall.set_defaults(func=cmd_uninstall)
    
    # list
    p_list = subparsers.add_parser("list", help="List installed skills")
    p_list.add_argument("--json", action="store_true", help="Output as JSON")
    p_list.set_defaults(func=cmd_list)
    
    # init
    p_init = subparsers.add_parser("init", help="Create a new skill.json")
    p_init.add_argument("path", nargs="?", help="Directory path")
    p_init.add_argument("--force", "-f", action="store_true", help="Overwrite existing")
    p_init.set_defaults(func=cmd_init)
    
    # update
    p_update = subparsers.add_parser("update", help="Update installed skills")
    p_update.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    p_update.set_defaults(func=cmd_update)
    
    # config
    p_config = subparsers.add_parser("config", help="Manage configuration")
    p_config.add_argument("action", choices=["list", "get", "set"])
    p_config.add_argument("key", nargs="?", help="Config key")
    p_config.add_argument("value", nargs="?", help="Config value")
    p_config.set_defaults(func=cmd_config)
    
    # cache
    p_cache = subparsers.add_parser("cache", help="Manage cache")
    p_cache.add_argument("action", choices=["clean", "list"])
    p_cache.set_defaults(func=cmd_cache)
    
    # run
    p_run = subparsers.add_parser("run", help="Run a skill")
    p_run.add_argument("skill_id", help="Skill ID")
    p_run.set_defaults(func=cmd_run)
    
    # detect - show detected agent info
    p_detect = subparsers.add_parser("detect", help="Show detected agent and skill paths")
    p_detect.set_defaults(func=cmd_detect)
    
    # validate - validate a skill for publishing
    p_validate = subparsers.add_parser("validate", help="Validate a skill for publishing",
        description="""Validate a skill directory before publishing.

Checks performed:
- skill.json schema validation
- SKILL.md content validation
- No secrets or API keys in files
- No malicious patterns (rm -rf, curl|bash, etc.)
- Duplicate skill name detection (requires catalog)
- Placeholder text detection

Examples:
  skills validate                    # Validate current directory
  skills validate ./my-skill         # Validate specific directory
  skills validate --verbose          # Show detailed results
  skills validate --skip-catalog     # Skip duplicate checking
""")
    p_validate.add_argument("path", nargs="?", help="Skill directory (default: current)")
    p_validate.add_argument("--verbose", "-v", action="store_true", help="Show detailed validation results")
    p_validate.add_argument("--skip-catalog", action="store_true", help="Skip catalog fetch for duplicate checking")
    p_validate.set_defaults(func=cmd_validate)
    
    # publish - publish a skill to the registry
    p_publish = subparsers.add_parser("publish", help="Publish a skill to the registry",
        description="""Publish a skill to GitHub and optionally submit to the official directory.

This command will:
1. Run comprehensive validation (schema, secrets, malicious patterns)
2. Create a GitHub repository (skill-{name}) if needed
3. Push your skill files
4. Create a release with the version from skill.json
5. Optionally submit to dmgrok/agent_skills_directory (--submit)

Your skill ID will be: {github-username}/{skill-name}

The PR-based submission flow ensures:
- Community review before inclusion
- Automated quality checks
- No duplicate skill names
- Security scanning for secrets/malware

Examples:
  skills publish                 # Publish to your GitHub only
  skills publish --submit        # Also submit to official directory
  skills publish --dry-run       # Preview what would happen
  skills publish --force         # Continue despite warnings
""")
    p_publish.add_argument("path", nargs="?", help="Skill directory (default: current)")
    p_publish.add_argument("--dry-run", "-n", action="store_true", help="Preview without making changes")
    p_publish.add_argument("--yes", "-y", action="store_true", help="Auto-confirm prompts")
    p_publish.add_argument("--submit", "-s", action="store_true", help="Submit to official directory via issue")
    p_publish.add_argument("--force", "-f", action="store_true", help="Continue despite validation warnings")
    p_publish.set_defaults(func=cmd_publish)
    
    # login - authenticate with GitHub
    p_login = subparsers.add_parser("login", help="Authenticate with GitHub")
    p_login.add_argument("--force", "-f", action="store_true", help="Re-authenticate even if already logged in")
    p_login.set_defaults(func=cmd_login)
    
    # whoami - show authenticated user
    p_whoami = subparsers.add_parser("whoami", help="Show authenticated GitHub user")
    p_whoami.set_defaults(func=cmd_whoami)
    
    # export - export skills to various formats
    p_export = subparsers.add_parser("export", help="Export installed skills to various formats",
        description="""Export installed skills to different runtime formats.

Supported formats:
  mcp       - MCP (Model Context Protocol) resources JSON
  langchain - LangChain tool definitions
  crewai    - CrewAI agent configurations
  autogen   - AutoGen agent definitions
  openai    - OpenAI Assistant configurations
  anthropic - Anthropic tool definitions
  prompt    - Combined system prompt (most universal)
  copilot   - GitHub Copilot instructions file
  claude    - Claude CLAUDE.md format

Examples:
  skills export --format prompt          # Export as combined prompt
  skills export --format mcp -o skills.json
  skills export --format copilot -o .github/copilot-skills.md
""")
    p_export.add_argument("--format", "-f", required=True,
                         choices=["mcp", "langchain", "crewai", "autogen", "openai", "anthropic", "prompt", "copilot", "claude"],
                         help="Export format")
    p_export.add_argument("--output", "-o", help="Output file (default: stdout)")
    p_export.add_argument("--skills-dir", help="Skills directory (default: all installed)")
    p_export.set_defaults(func=cmd_export)
    
    # stats - show analytics
    p_stats = subparsers.add_parser("stats", help="Show analytics and statistics",
        description="""Display statistics about skills usage.

Shows:
- Local install counts and history
- Catalog statistics (skills, providers, categories)  
- Provider rankings by GitHub stars
- Recent activity

Examples:
  skills stats              # Basic stats
  skills stats --detailed   # Include provider rankings
""")
    p_stats.add_argument("--detailed", "-d", action="store_true", help="Show detailed provider stats")
    p_stats.set_defaults(func=cmd_stats)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\nAborted")
        return 130
    except Exception as e:
        print_error(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())
