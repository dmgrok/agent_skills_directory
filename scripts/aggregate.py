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
import zlib
import argparse
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
import urllib.request
import urllib.error
import subprocess
import shutil
from urllib.parse import urlsplit

# Load environment variables from .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, skip

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
    # Community providers discovered from awesome-llm-skills README
    "obra-superpowers": {
        "name": "Obra Superpowers",
        "repo": "https://github.com/obra/superpowers",
        "api_tree_url": "https://api.github.com/repos/obra/superpowers/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/obra/superpowers/main",
        "skills_path_prefix": "skills/",
    },
    "tapestry": {
        "name": "Tapestry Skills",
        "repo": "https://github.com/michalparkola/tapestry-skills-for-claude-code",
        "api_tree_url": "https://api.github.com/repos/michalparkola/tapestry-skills-for-claude-code/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/michalparkola/tapestry-skills-for-claude-code/main",
        "skills_path_prefix": "",
    },
    "sanjay-ai-skills": {
        "name": "Sanjay AI Skills",
        "repo": "https://github.com/sanjay3290/ai-skills",
        "api_tree_url": "https://api.github.com/repos/sanjay3290/ai-skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/sanjay3290/ai-skills/main",
        "skills_path_prefix": "skills/",
    },
    "aws-skills": {
        "name": "AWS Skills",
        "repo": "https://github.com/zxkane/aws-skills",
        "api_tree_url": "https://api.github.com/repos/zxkane/aws-skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/zxkane/aws-skills/main",
        "skills_path_prefix": "plugins/",
    },
    # Claude Skills Marketplace - split by plugin category
    "claude-marketplace-engineering": {
        "name": "Claude Marketplace (Engineering)",
        "repo": "https://github.com/mhattingpete/claude-skills-marketplace",
        "api_tree_url": "https://api.github.com/repos/mhattingpete/claude-skills-marketplace/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main",
        "skills_path_prefix": "engineering-workflow-plugin/skills/",
    },
    "claude-marketplace-visual": {
        "name": "Claude Marketplace (Visual)",
        "repo": "https://github.com/mhattingpete/claude-skills-marketplace",
        "api_tree_url": "https://api.github.com/repos/mhattingpete/claude-skills-marketplace/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main",
        "skills_path_prefix": "visual-documentation-plugin/skills/",
    },
    "claude-marketplace-code": {
        "name": "Claude Marketplace (Code Ops)",
        "repo": "https://github.com/mhattingpete/claude-skills-marketplace",
        "api_tree_url": "https://api.github.com/repos/mhattingpete/claude-skills-marketplace/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main",
        "skills_path_prefix": "code-operations-plugin/skills/",
    },
    "claude-marketplace-productivity": {
        "name": "Claude Marketplace (Productivity)",
        "repo": "https://github.com/mhattingpete/claude-skills-marketplace",
        "api_tree_url": "https://api.github.com/repos/mhattingpete/claude-skills-marketplace/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main",
        "skills_path_prefix": "productivity-skills-plugin/skills/",
    },
    # Single-skill community repos
    "epub-skill": {
        "name": "EPUB Converter",
        "repo": "https://github.com/smerchek/claude-epub-skill",
        "api_tree_url": "https://api.github.com/repos/smerchek/claude-epub-skill/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/smerchek/claude-epub-skill/main",
        "skills_path_prefix": "",
    },
    "d3js-skill": {
        "name": "D3.js Visualization",
        "repo": "https://github.com/chrisvoncsefalvay/claude-d3js-skill",
        "api_tree_url": "https://api.github.com/repos/chrisvoncsefalvay/claude-d3js-skill/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/chrisvoncsefalvay/claude-d3js-skill/main",
        "skills_path_prefix": "",
    },
    "ffuf-skill": {
        "name": "FFUF Web Fuzzing",
        "repo": "https://github.com/jthack/ffuf_claude_skill",
        "api_tree_url": "https://api.github.com/repos/jthack/ffuf_claude_skill/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/jthack/ffuf_claude_skill/main",
        "skills_path_prefix": "",
    },
    "ios-simulator-skill": {
        "name": "iOS Simulator",
        "repo": "https://github.com/conorluddy/ios-simulator-skill",
        "api_tree_url": "https://api.github.com/repos/conorluddy/ios-simulator-skill/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/conorluddy/ios-simulator-skill/main",
        "skills_path_prefix": "ios-simulator-skill/",
    },
    "move-quality-skill": {
        "name": "Move Code Quality",
        "repo": "https://github.com/1NickPappas/move-code-quality-skill",
        "api_tree_url": "https://api.github.com/repos/1NickPappas/move-code-quality-skill/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/1NickPappas/move-code-quality-skill/main",
        "skills_path_prefix": "",
    },
    "playwright-skill": {
        "name": "Playwright Automation",
        "repo": "https://github.com/lackeyjb/playwright-skill",
        "api_tree_url": "https://api.github.com/repos/lackeyjb/playwright-skill/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/lackeyjb/playwright-skill/main",
        "skills_path_prefix": "skills/",
    },
    "pypict-skill": {
        "name": "PICT Test Cases",
        "repo": "https://github.com/omkamal/pypict-claude-skill",
        "api_tree_url": "https://api.github.com/repos/omkamal/pypict-claude-skill/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/omkamal/pypict-claude-skill/main",
        "skills_path_prefix": "",
    },
    "csv-summarizer-skill": {
        "name": "CSV Data Summarizer",
        "repo": "https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill",
        "api_tree_url": "https://api.github.com/repos/coffeefuelbump/csv-data-summarizer-claude-skill/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/coffeefuelbump/csv-data-summarizer-claude-skill/main",
        "skills_path_prefix": "",
    },
    "family-history-skill": {
        "name": "Family History Research",
        "repo": "https://github.com/emaynard/claude-family-history-research-skill",
        "api_tree_url": "https://api.github.com/repos/emaynard/claude-family-history-research-skill/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/emaynard/claude-family-history-research-skill/main",
        "skills_path_prefix": "",
    },
    "notebooklm-skill": {
        "name": "NotebookLM Integration",
        "repo": "https://github.com/PleasePrompto/notebooklm-skill",
        "api_tree_url": "https://api.github.com/repos/PleasePrompto/notebooklm-skill/git/trees/master?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/PleasePrompto/notebooklm-skill/master",
        "skills_path_prefix": "",
    },
    "aiqualitylab": {
        "name": "AI Quality Lab",
        "repo": "https://github.com/aiqualitylab/agent-skills",
        "api_tree_url": "https://api.github.com/repos/aiqualitylab/agent-skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/aiqualitylab/agent-skills/main",
        "skills_path_prefix": "skills/",
    },
    "stripe": {
        "name": "Stripe",
        "repo": "https://github.com/stripe/ai",
        "api_tree_url": "https://api.github.com/repos/stripe/ai/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/stripe/ai/main",
        "skills_path_prefix": "skills/",
    },
    "cloudflare": {
        "name": "Cloudflare",
        "repo": "https://github.com/cloudflare/skills",
        "api_tree_url": "https://api.github.com/repos/cloudflare/skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/cloudflare/skills/main",
        "skills_path_prefix": "skills/",
    },
    "trailofbits": {
        "name": "Trail of Bits Security",
        "repo": "https://github.com/trailofbits/skills",
        "api_tree_url": "https://api.github.com/repos/trailofbits/skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/trailofbits/skills/main",
        "skills_path_prefix": "skills/",
    },
    "expo": {
        "name": "Expo",
        "repo": "https://github.com/expo/skills",
        "api_tree_url": "https://api.github.com/repos/expo/skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/expo/skills/main",
        "skills_path_prefix": "skills/",
    },
    "getsentry": {
        "name": "Sentry",
        "repo": "https://github.com/getsentry/skills",
        "api_tree_url": "https://api.github.com/repos/getsentry/skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/getsentry/skills/main",
        "skills_path_prefix": "skills/",
    },
    "supabase": {
        "name": "Supabase",
        "repo": "https://github.com/supabase/agent-skills",
        "api_tree_url": "https://api.github.com/repos/supabase/agent-skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/supabase/agent-skills/main",
        "skills_path_prefix": "skills/",
    },
    "google-labs-stitch": {
        "name": "Google Labs Stitch",
        "repo": "https://github.com/google-labs-code/stitch-skills",
        "api_tree_url": "https://api.github.com/repos/google-labs-code/stitch-skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/google-labs-code/stitch-skills/main",
        "skills_path_prefix": "skills/",
    },
    "composiohq": {
        "name": "ComposioHQ",
        "repo": "https://github.com/ComposioHQ/awesome-claude-skills",
        "api_tree_url": "https://api.github.com/repos/ComposioHQ/awesome-claude-skills/git/trees/master?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/ComposioHQ/awesome-claude-skills/master",
        "skills_path_prefix": "",
    },
    "better-auth": {
        "name": "Better Auth",
        "repo": "https://github.com/better-auth/skills",
        "api_tree_url": "https://api.github.com/repos/better-auth/skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/better-auth/skills/main",
        "skills_path_prefix": "skills/",
    },
    "tinybird": {
        "name": "Tinybird",
        "repo": "https://github.com/tinybirdco/tinybird-agent-skills",
        "api_tree_url": "https://api.github.com/repos/tinybirdco/tinybird-agent-skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/tinybirdco/tinybird-agent-skills/main",
        "skills_path_prefix": "skills/",
    },
    "neondatabase": {
        "name": "Neon Database",
        "repo": "https://github.com/neondatabase/agent-skills",
        "api_tree_url": "https://api.github.com/repos/neondatabase/agent-skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/neondatabase/agent-skills/main",
        "skills_path_prefix": "skills/",
    },
    "fal-ai": {
        "name": "fal.ai",
        "repo": "https://github.com/fal-ai-community/skills",
        "api_tree_url": "https://api.github.com/repos/fal-ai-community/skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/fal-ai-community/skills/main",
        "skills_path_prefix": "skills/",
    },
    "remotion": {
        "name": "Remotion",
        "repo": "https://github.com/remotion-dev/skills",
        "api_tree_url": "https://api.github.com/repos/remotion-dev/skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/remotion-dev/skills/main",
        "skills_path_prefix": "skills/",
    },
    "nginity": {
        "name": "nginity Enterprise",
        "repo": "https://github.com/alirezarezvani/claude-skills",
        "api_tree_url": "https://api.github.com/repos/alirezarezvani/claude-skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/alirezarezvani/claude-skills/main",
        "skills_path_prefix": "skills/",
    },
    "voltagent": {
        "name": "VoltAgent Catalog",
        "repo": "https://github.com/VoltAgent/awesome-agent-skills",
        "api_tree_url": "https://api.github.com/repos/VoltAgent/awesome-agent-skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/VoltAgent/awesome-agent-skills/main",
        "skills_path_prefix": "",
    },
    "heilcheng": {
        "name": "heilcheng Catalog",
        "repo": "https://github.com/heilcheng/awesome-agent-skills",
        "api_tree_url": "https://api.github.com/repos/heilcheng/awesome-agent-skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/heilcheng/awesome-agent-skills/main",
        "skills_path_prefix": "",
    },
    "travisvn": {
        "name": "travisvn Collection",
        "repo": "https://github.com/travisvn/awesome-claude-skills",
        "api_tree_url": "https://api.github.com/repos/travisvn/awesome-claude-skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/travisvn/awesome-claude-skills/main",
        "skills_path_prefix": "",
    },
    # New community providers from GitHub search
    "obsidian-plugin": {
        "name": "Obsidian Plugin Development",
        "repo": "https://github.com/gapmiss/obsidian-plugin-skill",
        "api_tree_url": "https://api.github.com/repos/gapmiss/obsidian-plugin-skill/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/gapmiss/obsidian-plugin-skill/main",
        "skills_path_prefix": ".claude/skills/",
    },
    "stream-coding": {
        "name": "Stream Coding Methodology",
        "repo": "https://github.com/frmoretto/stream-coding",
        "api_tree_url": "https://api.github.com/repos/frmoretto/stream-coding/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/frmoretto/stream-coding/main",
        "skills_path_prefix": "skills/",
    },
    "ipsw-skill": {
        "name": "IPSW iOS Firmware",
        "repo": "https://github.com/blacktop/ipsw-skill",
        "api_tree_url": "https://api.github.com/repos/blacktop/ipsw-skill/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/blacktop/ipsw-skill/main",
        "skills_path_prefix": "skill/",
    },
    "visionos-agents": {
        "name": "visionOS Development",
        "repo": "https://github.com/tomkrikorian/visionOSAgents",
        "api_tree_url": "https://api.github.com/repos/tomkrikorian/visionOSAgents/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/tomkrikorian/visionOSAgents/main",
        "skills_path_prefix": "skills/",
    },
    "skills-to-agents": {
        "name": "Skills to Agents Converter",
        "repo": "https://github.com/dave1010/skills-to-agents",
        "api_tree_url": "https://api.github.com/repos/dave1010/skills-to-agents/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/dave1010/skills-to-agents/main",
        "skills_path_prefix": "",
    },
}

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DEFAULT_HEADERS = {"User-Agent": "AgentSkillsDirectory/1.0"}
if GITHUB_TOKEN:
    # Use GitHub token when available to avoid rate limits
    DEFAULT_HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    DEFAULT_HEADERS["Accept"] = "application/vnd.github+json"

# Trusted sources - these are prioritized and used for enhanced similarity detection
TRUSTED_SOURCES = {"anthropics", "openai", "vercel", "github"}

# Provider priority for deduplication (lower = higher priority)
# Official sources preferred over community mirrors
PROVIDER_PRIORITY = {
    "anthropics": 1,
    "openai": 2,
    "github": 3,
    "vercel": 4,
    "huggingface": 5,
    "skillcreatorai": 10,  # Community mirror - lowest priority
}

# Category mappings based on keywords in name/description
CATEGORY_KEYWORDS = {
    "documents": ["pdf", "docx", "xlsx", "pptx", "document", "spreadsheet", "presentation"],
    "development": ["git", "gh-", "code", "test", "ci", "debug", "lint", "review", "mcp"],
    "creative": ["art", "design", "canvas", "music", "brand", "visual", "image"],
    "enterprise": ["communication", "meeting", "email", "slack", "notion", "knowledge"],
    "integrations": ["notion", "github", "slack", "api"],
    "data": ["data", "analysis", "extract", "transform", "csv", "json"],
}

# State file for incremental aggregation
STATE_FILE = Path(__file__).parent.parent / "aggregation_state.json"


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
    body: str = field(default="", repr=False)  # Full SKILL.md body for dedup comparison
    
    # Duplicate annotation fields
    duplicate_status: Optional[str] = field(default=None)  # "mirror" or "probable_duplicate"
    duplicate_annotation: Optional[str] = field(default=None)  # Human-readable annotation
    duplicate_of: Optional[str] = field(default=None)  # ID of the reference skill
    duplicate_similarity: Optional[float] = field(default=None)  # Similarity score
    
    # Maintenance KPIs
    days_since_update: Optional[int] = field(default=None)  # Days since last commit
    maintenance_status: Optional[str] = field(default=None)  # "active", "maintained", "stale", "abandoned"
    quality_score: Optional[int] = field(default=None)  # Composite quality score 0-100


def calculate_quality_score(
    maintenance_status: Optional[str],
    has_scripts: bool,
    has_references: bool,
    has_assets: bool,
    provider: str
) -> int:
    """
    Calculate composite quality score (0-100) based on multiple factors.
    
    Scoring breakdown:
    - Maintenance status: 0-50 points
    - Documentation completeness: 0-30 points (scripts, references, assets)
    - Provider trust: 0-20 points (official sources get bonus)
    """
    score = 0
    
    # Maintenance score (50 points max)
    if maintenance_status == "active":
        score += 50
    elif maintenance_status == "maintained":
        score += 40
    elif maintenance_status == "stale":
        score += 20
    elif maintenance_status == "abandoned":
        score += 5
    else:
        score += 25  # Unknown status - neutral
    
    # Documentation completeness (30 points max)
    if has_scripts:
        score += 10
    if has_references:
        score += 10
    if has_assets:
        score += 10
    
    # Provider trust bonus (20 points max)
    # Official/trusted sources get higher scores
    trusted_providers = {
        "anthropics", "openai", "github", "vercel", "huggingface",
        "stripe", "cloudflare", "supabase", "sentry", "expo",
        "better-auth", "tinybird", "neondatabase", "fal-ai", "remotion"
    }
    if provider in trusted_providers:
        score += 20
    else:
        score += 10  # Community providers still get partial credit
    
    return min(score, 100)  # Cap at 100


def calculate_maintenance_status(last_updated_at: Optional[str]) -> tuple[Optional[int], Optional[str]]:
    """
    Calculate maintenance KPIs based on last update date.
    
    Returns:
        (days_since_update, maintenance_status)
        
    Status definitions:
        - active: Updated within 30 days
        - maintained: Updated within 6 months
        - stale: Updated within 1 year
        - abandoned: No update in over 1 year
    """
    if not last_updated_at:
        return None, None
    
    try:
        last_update = datetime.fromisoformat(last_updated_at.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        days_since = (now - last_update).days
        
        if days_since < 30:
            status = "active"
        elif days_since < 180:  # 6 months
            status = "maintained"
        elif days_since < 365:  # 1 year
            status = "stale"
        else:
            status = "abandoned"
        
        return days_since, status
    except (ValueError, AttributeError):
        return None, None


def compute_content_hash(text: str) -> str:
    """Compute a normalized hash of content for similarity detection."""
    # Normalize: lowercase, remove extra whitespace, strip
    normalized = re.sub(r'\s+', ' ', text.lower().strip())
    # Use zlib crc32 as a fast hash
    return format(zlib.crc32(normalized.encode('utf-8')) & 0xffffffff, '08x')


def compute_similarity(text1: str, text2: str) -> float:
    """
    Compute similarity ratio between two texts using compression.
    Higher ratio means more similar content (1.0 = identical).
    """
    if not text1 or not text2:
        return 0.0
    
    # Normalize texts
    t1 = re.sub(r'\s+', ' ', text1.lower().strip())
    t2 = re.sub(r'\s+', ' ', text2.lower().strip())
    
    # Compression-based similarity (Normalized Compression Distance)
    c1 = len(zlib.compress(t1.encode('utf-8')))
    c2 = len(zlib.compress(t2.encode('utf-8')))
    c12 = len(zlib.compress((t1 + t2).encode('utf-8')))
    
    # NCD formula: (C(xy) - min(C(x), C(y))) / max(C(x), C(y))
    # We return 1 - NCD so higher = more similar
    ncd = (c12 - min(c1, c2)) / max(c1, c2)
    return max(0.0, 1.0 - ncd)


def compute_enhanced_similarity(skill1, skill2) -> float:
    """
    Enhanced similarity that considers metadata and handles skills with different detail levels.
    Gives higher weight to name/description similarity for trusted sources.
    """
    # Start with body similarity
    body_sim = compute_similarity(skill1.body, skill2.body)
    
    # Check if both skills have same name (case-insensitive)
    same_name = skill1.name.lower() == skill2.name.lower()
    
    # Check metadata similarity
    desc_sim = 0.0
    if skill1.description and skill2.description:
        desc_sim = compute_similarity(skill1.description, skill2.description)
    
    # If names match and either is from a trusted source, boost similarity
    if same_name:
        skill1_trusted = skill1.provider in TRUSTED_SOURCES
        skill2_trusted = skill2.provider in TRUSTED_SOURCES
        
        if skill1_trusted or skill2_trusted:
            # For trusted sources with matching names, heavily weight metadata
            # This catches cases where one has extensive docs and other is concise
            metadata_sim = desc_sim * 0.7 + body_sim * 0.3
            # Boost by a base amount for same name from trusted source
            return min(1.0, metadata_sim + 0.3)
    
    # Default: primarily body similarity with some description weight
    return body_sim * 0.8 + desc_sim * 0.2


def deduplicate_skills(skills: list, similarity_threshold: float = 0.8) -> tuple[list, list, dict]:
    """
    Annotate duplicate skills instead of removing them.
    Mark skills as "mirror" (complete duplicate) or "probable duplicate" based on similarity.
    
    Deduplication strategy:
    1. Group skills by name
    2. For groups with multiple skills, check content similarity
    3. If similarity > threshold, annotate as duplicate (keep in catalog with metadata)
    4. Distinguish between "mirror" (>95% similar) and "probable duplicate" (80-95%)
    5. Track all similar skills for cross-referencing
    
    Args:
        skills: List of Skill objects
        similarity_threshold: Similarity threshold above which skills are annotated as duplicates (default 0.8)
    
    Returns:
        Tuple of (all skills with annotations, list of duplicate metadata, similar_skills_map)
        similar_skills_map: Dict mapping skill id to list of similar skill ids with scores
    """
    from collections import defaultdict
    
    # Group by skill name
    by_name: dict[str, list] = defaultdict(list)
    for skill in skills:
        by_name[skill.name].append(skill)
    
    all_skills = []  # Keep all skills, annotated
    duplicate_metadata = []  # Track duplicate info for reference
    similar_skills_map: dict[str, list] = {}  # Maps skill_id to similar skills
    
    for name, group in by_name.items():
        if len(group) == 1:
            all_skills.append(group[0])
            continue
        
        # Sort by provider priority (lower = better)
        group.sort(key=lambda s: PROVIDER_PRIORITY.get(s.provider, 99))
        
        # The best (first) skill in the group is the reference
        best = group[0]
        all_skills.append(best)
        kept_in_group = [best]
        
        for other in group[1:]:
            similarity = compute_enhanced_similarity(best, other)
            
            if similarity > similarity_threshold:
                # High similarity - annotate as duplicate but keep it
                if similarity >= 0.95:
                    # Complete mirror
                    other.duplicate_status = "mirror"
                    other.duplicate_annotation = f"Complete mirror of {best.id}"
                else:
                    # Probable duplicate
                    other.duplicate_status = "probable_duplicate"
                    other.duplicate_annotation = f"Probable duplicate of {best.id} ({round(similarity * 100)}% similar)"
                
                other.duplicate_of = best.id
                other.duplicate_similarity = round(similarity, 2)
                
                # Track for the duplicates summary
                duplicate_metadata.append({
                    "skill": other,
                    "reference": best.id,
                    "status": other.duplicate_status,
                    "similarity": round(similarity, 2)
                })
            
            # Keep all skills, even duplicates
            all_skills.append(other)
            kept_in_group.append(other)
        
        # For all kept skills in this group, record their similar counterparts
        if len(kept_in_group) > 1:
            for i, skill_a in enumerate(kept_in_group):
                similar_list = []
                for j, skill_b in enumerate(kept_in_group):
                    if i != j:
                        sim = compute_enhanced_similarity(skill_a, skill_b)
                        similar_list.append({
                            "id": skill_b.id,
                            "provider": skill_b.provider,
                            "similarity": round(sim, 2)
                        })
                if similar_list:
                    similar_skills_map[skill_a.id] = similar_list
    
    return all_skills, duplicate_metadata, similar_skills_map


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


def fetch_repo_stars(owner: str, repo: str) -> Optional[int]:
    """Fetch the star count for a GitHub repository."""
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    content = fetch_url(api_url)
    if not content:
        return None

    try:
        repo_data = json.loads(content)
        return repo_data.get("stargazers_count")
    except json.JSONDecodeError:
        return None


def fetch_repo_description(owner: str, repo: str) -> Optional[str]:
    """Fetch the description for a GitHub repository."""
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    content = fetch_url(api_url)
    if not content:
        return None

    try:
        repo_data = json.loads(content)
        return repo_data.get("description")
    except json.JSONDecodeError:
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
        
        # Match SKILL.md files under the skills_path_prefix
        # Handle both "skills/name/SKILL.md" and root-level "SKILL.md" (when prefix is "")
        prefix = config["skills_path_prefix"]
        if path.startswith(prefix) and (path.endswith("/SKILL.md") or path == "SKILL.md"):
            skill_files.append({
                "path": path,
                "sha": item.get("sha"),
                "dir": str(Path(path).parent) if "/" in path else ""
            })
    
    print(f"  Found {len(skill_files)} skills")
    
    skills = []
    for sf in skill_files:
        skill_md_url = f"{config['raw_base']}/{sf['path']}"
        content = fetch_url(skill_md_url)
        
        if not content:
            continue
        
        parsed = parse_skill_md(content)
        if not parsed:
            print(f"  Skipping {sf['path']}: failed to parse", file=sys.stderr)
            continue
        
        fm = parsed["frontmatter"]
        
        # Get name from frontmatter or derive from directory path
        name = fm.get("name", "")
        if not name:
            # Derive name from directory path (e.g., "skills/stripe-best-practices/SKILL.md" -> "stripe-best-practices")
            if sf["dir"]:
                name = Path(sf["dir"]).name
            else:
                # For root-level SKILL.md files, use the repo name
                name = Path(config["repo"]).name
        
        if not name:
            print(f"  Skipping {sf['path']}: unable to determine name", file=sys.stderr)
            continue
        
        description = fm.get("description", "")
        
        # Check for optional directories
        skill_dir = sf["dir"]
        has_scripts = any(p.startswith(f"{skill_dir}/scripts/") for p in all_paths)
        has_references = any(p.startswith(f"{skill_dir}/references/") or p.startswith(f"{skill_dir}/reference/") for p in all_paths)
        has_assets = any(p.startswith(f"{skill_dir}/assets/") or p.startswith(f"{skill_dir}/templates/") for p in all_paths)

        last_updated_at = None
        if owner_repo:
            last_updated_at = fetch_last_updated_at(owner_repo[0], owner_repo[1], sf["path"])
        
        # Calculate maintenance KPIs
        days_since_update, maintenance_status = calculate_maintenance_status(last_updated_at)
        
        # Calculate quality score
        quality_score = calculate_quality_score(
            maintenance_status,
            has_scripts,
            has_references,
            has_assets,
            provider_id
        )
        
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
            tags=extract_tags(name, description),
            body=parsed["body"],  # Store body for dedup comparison
            days_since_update=days_since_update,
            maintenance_status=maintenance_status,
            quality_score=quality_score
        )
        
        skills.append(skill)
        status_emoji = {"active": "🟢", "maintained": "🟡", "stale": "🟠", "abandoned": "🔴"}.get(maintenance_status, "⚪")
        print(f"  ✓ {name} {status_emoji} (score: {quality_score})")
    
    return skills


def build_catalog() -> dict:
    """Build the complete skills catalog."""
    all_skills = []
    provider_stats = {}
    
    # Track unique repos to avoid duplicate API calls for stars
    repo_cache: dict[str, dict] = {}  # repo_url -> {stars, description}
    
    for provider_id, config in PROVIDERS.items():
        skills = fetch_provider_skills(provider_id, config)
        all_skills.extend(skills)
        
        # Fetch repo stats (stars, description) - cache by repo URL
        repo_url = config["repo"]
        if repo_url not in repo_cache:
            owner_repo = extract_owner_repo(repo_url)
            stars = None
            description = None
            if owner_repo:
                # Fetch repo info in one call
                api_url = f"https://api.github.com/repos/{owner_repo[0]}/{owner_repo[1]}"
                content = fetch_url(api_url)
                if content:
                    try:
                        repo_data = json.loads(content)
                        stars = repo_data.get("stargazers_count")
                        description = repo_data.get("description")
                    except json.JSONDecodeError:
                        pass
            repo_cache[repo_url] = {"stars": stars, "description": description}
        
        cached = repo_cache[repo_url]
        provider_stats[provider_id] = {
            "name": config["name"],
            "repo": config["repo"],
            "skills_count": len(skills),
            "stars": cached["stars"],
            "description": cached["description"]
        }
    
    # Deduplicate skills - annotate mirrors and probable duplicates
    print(f"\nAnnotating duplicate skills...")
    all_skills, duplicate_metadata, similar_skills_map = deduplicate_skills(all_skills)
    
    if duplicate_metadata:
        mirrors = [d for d in duplicate_metadata if d['status'] == 'mirror']
        probable = [d for d in duplicate_metadata if d['status'] == 'probable_duplicate']
        
        print(f"  Annotated {len(duplicate_metadata)} duplicate skills:")
        if mirrors:
            print(f"    {len(mirrors)} complete mirrors (≥95% similar):")
            for d in mirrors:
                print(f"      - {d['skill'].id} → {d['reference']} ({round(d['similarity'] * 100)}%)")
        if probable:
            print(f"    {len(probable)} probable duplicates (80-95% similar):")
            for d in probable:
                print(f"      - {d['skill'].id} → {d['reference']} ({round(d['similarity'] * 100)}%)")
    
    if similar_skills_map:
        # Count how many skills have similar counterparts (excluding duplicates)
        non_duplicate_similar = sum(1 for skill in all_skills 
                                   if skill.id in similar_skills_map and not skill.duplicate_status)
        print(f"  Found {non_duplicate_similar} skills with similar counterparts (kept as different implementations)")
    
    # Update provider stats - all skills are kept now
    for provider_id in provider_stats:
        count = sum(1 for s in all_skills if s.provider == provider_id)
        provider_stats[provider_id]["skills_count"] = count
    
    # Sort skills by provider then name
    all_skills.sort(key=lambda s: (s.provider, s.name))
    
    # Get unique categories
    categories = sorted(set(s.category for s in all_skills))
    
    # Calculate maintenance statistics
    maintenance_stats = {
        "active": len([s for s in all_skills if s.maintenance_status == "active"]),
        "maintained": len([s for s in all_skills if s.maintenance_status == "maintained"]),
        "stale": len([s for s in all_skills if s.maintenance_status == "stale"]),
        "abandoned": len([s for s in all_skills if s.maintenance_status == "abandoned"]),
        "unknown": len([s for s in all_skills if s.maintenance_status is None])
    }
    
    # Calculate percentages
    total_with_dates = len(all_skills) - maintenance_stats["unknown"]
    if total_with_dates > 0:
        maintenance_stats["active_percentage"] = round((maintenance_stats["active"] / total_with_dates) * 100, 1)
        maintenance_stats["maintained_percentage"] = round(((maintenance_stats["active"] + maintenance_stats["maintained"]) / total_with_dates) * 100, 1)
    else:
        maintenance_stats["active_percentage"] = 0
        maintenance_stats["maintained_percentage"] = 0
    
    # Build catalog
    now = datetime.now(timezone.utc)
    catalog = {
        "$schema": "https://raw.githubusercontent.com/dmgrok/agent_skills_directory/main/schema/catalog-schema.json",
        "version": now.strftime("%Y.%m.%d"),
        "generated_at": now.isoformat(),
        "total_skills": len(all_skills),
        "providers": provider_stats,
        "categories": categories,
        "skills": [],
        "duplicate_summary": {
            "total_annotated": len(duplicate_metadata),
            "mirrors": len([r for r in duplicate_metadata if r["status"] == "mirror"]),
            "probable_duplicates": len([r for r in duplicate_metadata if r["status"] == "probable_duplicate"])
        },
        "maintenance_summary": maintenance_stats
    }
    
    # Convert skills to dicts
    for skill in all_skills:
        skill_dict = asdict(skill)
        # Convert nested dataclass
        skill_dict["source"] = asdict(skill.source)
        # Remove body field (only used for dedup, not for output)
        skill_dict.pop("body", None)
        # Add similar skills if this skill has counterparts
        if skill.id in similar_skills_map:
            skill_dict["similar_skills"] = similar_skills_map[skill.id]
        catalog["skills"].append(skill_dict)
    
    return catalog


def load_state() -> dict:
    """Load previous aggregation state for incremental mode."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠ Could not load state file: {e}", file=sys.stderr)
    return {"last_run": None, "provider_commits": {}, "skills_count": 0}


def save_state(catalog: dict, provider_commits: dict) -> None:
    """Save aggregation state for next incremental run."""
    state = {
        "last_run": datetime.now(timezone.utc).isoformat(),
        "provider_commits": provider_commits,
        "skills_count": catalog["total_skills"],
        "version": catalog["version"]
    }
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    print(f"✓ Saved state to {STATE_FILE}")


def get_provider_head_commit(provider_id: str, provider_config: dict) -> Optional[str]:
    """Get the latest commit SHA for a provider's repository."""
    # Extract owner/repo from API URL
    url_match = re.search(r'repos/([^/]+/[^/]+)/', provider_config["api_tree_url"])
    if not url_match:
        return None
    
    owner_repo = url_match.group(1)
    branch = "main" if "main" in provider_config["api_tree_url"] else "master"
    commits_url = f"https://api.github.com/repos/{owner_repo}/commits/{branch}"
    
    try:
        json_str = fetch_url(commits_url)
        if json_str:
            data = json.loads(json_str)
            if "sha" in data:
                return data["sha"]
    except Exception as e:
        print(f"⚠ Could not fetch HEAD commit for {provider_id}: {e}", file=sys.stderr)
    
    return None


def check_provider_changed(provider_id: str, provider_config: dict, last_commit: Optional[str]) -> bool:
    """Check if provider has new commits since last aggregation."""
    if not last_commit:
        return True  # No previous state, fetch everything
    
    current_commit = get_provider_head_commit(provider_id, provider_config)
    if not current_commit:
        return True  # Can't determine, be safe and fetch
    
    return current_commit != last_commit


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
    global PROVIDERS  # Declare at top for potential modification in incremental mode
    
    parser = argparse.ArgumentParser(description="Aggregate skills from multiple providers")
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="Only fetch from providers with changes since last run (saves API requests)"
    )
    args = parser.parse_args()
    
    print("=" * 50)
    print("Agent Skills Directory Aggregator")
    if args.incremental:
        print("Mode: INCREMENTAL (checking for changes only)")
    else:
        print("Mode: FULL REFRESH")
    print("=" * 50)
    print()
    
    # Load previous state for incremental mode
    state = load_state() if args.incremental else None
    provider_commits = {}
    previous_catalog = None
    
    if args.incremental and state and state.get("last_run"):
        print(f"Last run: {state['last_run']}")
        print(f"Previous skills count: {state.get('skills_count', 0)}")
        print("\nChecking providers for changes...")
        
        # Load previous catalog to merge unchanged provider skills
        output_dir = Path(__file__).parent.parent
        catalog_json = output_dir / "catalog.json"
        if catalog_json.exists():
            with open(catalog_json, 'r') as f:
                previous_catalog = json.load(f)
        
        # Check which providers have changed
        changed_providers = []
        unchanged_providers = []
        
        for provider_id, provider_config in PROVIDERS.items():
            last_commit = state.get("provider_commits", {}).get(provider_id)
            current_commit = get_provider_head_commit(provider_id, provider_config)
            
            if current_commit:
                provider_commits[provider_id] = current_commit
            
            if check_provider_changed(provider_id, provider_config, last_commit):
                changed_providers.append(provider_id)
                print(f"  ✓ {provider_config['name']}: CHANGED")
            else:
                unchanged_providers.append(provider_id)
                print(f"  - {provider_config['name']}: unchanged")
        
        if not changed_providers:
            print("\n✓ No changes detected. Catalog is up to date.")
            return
        
        print(f"\n{len(changed_providers)}/{len(PROVIDERS)} providers have changes")
        print(f"This will save ~{len(unchanged_providers) * 2} GitHub API requests\n")
        
        # Temporarily filter PROVIDERS to only changed ones
        original_providers = PROVIDERS.copy()
        PROVIDERS = {pid: original_providers[pid] for pid in changed_providers}
    elif args.incremental:
        # First run with --incremental: do full refresh but don't fetch commits upfront (save API requests)
        print("First run with incremental mode - doing full refresh...")
        print("(Commit tracking will be enabled after this run)\n")
    
    catalog = build_catalog()
    
    # Merge with previous catalog if running in incremental mode with unchanged providers
    if previous_catalog and args.incremental:
        # Get list of providers we just fetched
        fetched_providers = set(PROVIDERS.keys())
        
        # Get original full provider list
        from importlib import reload
        import sys
        # Reload to get original PROVIDERS dict
        original_providers_list = set(pid for pid in provider_commits.keys())
        unchanged_providers = original_providers_list - fetched_providers
        
        if unchanged_providers:
            print(f"\nMerging skills from {len(unchanged_providers)} unchanged providers...")
            # Add skills from unchanged providers
            for skill_dict in previous_catalog.get("skills", []):
                if skill_dict.get("provider") in unchanged_providers:
                    catalog["skills"].append(skill_dict)
            
            # Update provider stats
            for provider_id in unchanged_providers:
                prev_provider = previous_catalog.get("providers", {}).get(provider_id)
                if prev_provider:
                    catalog["providers"][provider_id] = prev_provider
            
            # Recalculate totals
            catalog["total_skills"] = len(catalog["skills"])
            print(f"  Total skills after merge: {catalog['total_skills']}")
    
    # After building catalog, fetch commit SHAs for state tracking (if not already done in incremental mode)
    if not provider_commits:
        print("\nCollecting commit SHAs for state tracking...")
        for provider_id, provider_config in PROVIDERS.items():
            current_commit = get_provider_head_commit(provider_id, provider_config)
            if current_commit:
                provider_commits[provider_id] = current_commit
    
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
    
    # Save state for next incremental run
    save_state(catalog, provider_commits)
    
    # Summary
    print(f"\n{'=' * 50}")
    print(f"Total skills: {catalog['total_skills']}")
    for pid, pinfo in catalog["providers"].items():
        print(f"  {pinfo['name']}: {pinfo['skills_count']} skills")
    print(f"Categories: {', '.join(catalog['categories'])}")
    
    # Maintenance summary
    maint = catalog.get("maintenance_summary", {})
    if maint:
        print(f"\nMaintenance Status:")
        print(f"  🟢 Active (<30 days): {maint.get('active', 0)} ({maint.get('active_percentage', 0)}%)")
        print(f"  🟡 Maintained (<6 mo): {maint.get('maintained', 0)}")
        print(f"  🟠 Stale (<1 year): {maint.get('stale', 0)}")
        print(f"  🔴 Abandoned (>1 year): {maint.get('abandoned', 0)}")
        print(f"  Overall: {maint.get('maintained_percentage', 0)}% actively maintained")
    
    print("=" * 50)


if __name__ == "__main__":
    main()
