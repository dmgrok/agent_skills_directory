# Agent Skills Directory

**Intelligent skill discovery for AI agents.** Find quality-validated skills that match your project with smart recommendations, maintenance tracking, and security scanning.

```bash
# Get intelligent recommendations for your project
skillsdir suggest

# Or search with quality insights
skillsdir search "pdf extraction"

# Browse the catalog
open https://dmgrok.github.io/agent_skills_directory/
```

[![Curated Skills](https://img.shields.io/badge/Skills-245+-success)](https://dmgrok.github.io/agent_skills_directory/)
[![Providers](https://img.shields.io/badge/Providers-41-blue)](https://dmgrok.github.io/agent_skills_directory/)
[![Quality Tracked](https://img.shields.io/badge/Quality-Tracked-yellow)](https://github.com/dmgrok/LGTM_agent_skills)
[![Maintenance Status](https://img.shields.io/badge/Maintenance-🟢🟡🟠🔴-green)](https://dmgrok.github.io/agent_skills_directory/)

---

## Why This Exists

**The Problem:** There are thousands of AI agent skills. Which ones work? Which are maintained? Which fit your project?

**The Solution:** We aggregate, validate, and score skills from 41+ official providers so you can make informed decisions.

### Key Features

- 🎯 **Smart Recommendations** - Analyzes your project and suggests relevant skills
- 📊 **Quality Scoring** - 0-100 points based on documentation, maintenance, and provider trust
- 🟢 **Maintenance Status** - Active, Maintained, Stale, or Abandoned with days-since-update
- 🔍 **Similar Skills** - See how many alternatives exist for each skill
- 🛡️ **Security Validated** - Scanned for secrets and prompt injection
- 🏢 **Official Sources** - Anthropic, OpenAI, GitHub, Vercel, Stripe, Cloudflare + 35 more
- 💯 **100% Local** - No LLM or external API required for recommendations

---

## 🚀 Contributing New Providers

Want to add your skills to the directory? It's fully automated!

1. **[Create a New Provider Issue](https://github.com/dmgrok/agent_skills_directory/issues/new?template=new-provider.yml)** with your repository details
2. Our automated validation system will:
   - ✅ Validate skills using [LGTM Agent Skills](https://github.com/dmgrok/LGTM_agent_skills)
   - 🔒 Scan for secrets with gitleaks
   - 🛡️ Check for prompt injection attacks with Lakera Guard
   - 🤖 Auto-create a PR if validation passes (70+ score required)
3. Once merged, your skills are automatically included in daily aggregation runs

**Requirements:**
- Skills in `SKILL.md` format with YAML frontmatter
- Valid license (MIT, Apache 2.0, etc.)
- No hardcoded secrets or malicious content
- Score 70+ on LGTM validation

**Example:** See [issue #11](https://github.com/dmgrok/agent_skills_directory/issues/11) for a sample submission.

---

## Skills Providers

This directory aggregates skills from **41 provider repositories** across the AI agent ecosystem:

### Major Providers

| Provider | Repository | Skills | Stars |
|----------|-----------|--------|-------|
| [Anthropic](https://github.com/anthropics/skills) | anthropics/skills | 16 | 54.7K ⭐ |
| [Obra Superpowers](https://github.com/obra/superpowers) | obra/superpowers | 14 | 37.3K ⭐ |
| [GitHub Copilot](https://github.com/github/awesome-copilot) | github/awesome-copilot | 26 | 19.1K ⭐ |
| [Vercel](https://github.com/vercel-labs/agent-skills) | vercel-labs/agent-skills | 5 | 16.9K ⭐ |
| [NotebookLM](https://github.com/PleasePrompto/notebooklm-skill) | notebooklm-skill | 1 | 2.8K ⭐ |
| [OpenAI Codex](https://github.com/openai/skills) | openai/skills | 12 | 2.1K ⭐ |
| [Playwright](https://github.com/lackeyjb/playwright-skill) | playwright-skill | 1 | 1.5K ⭐ |
| [HuggingFace](https://github.com/huggingface/skills) | huggingface/skills | 8 | 1.1K ⭐ |

### Enterprise & Official Providers

| Provider | Repository | Focus | Stars |
|----------|-----------|-------|-------|
| [VoltAgent](https://github.com/VoltAgent/awesome-agent-skills) | voltagent/awesome-agent-skills | Skills aggregator (172+ skills) | 5.2K ⭐ |
| [heilcheng](https://github.com/heilcheng/awesome-agent-skills) | heilcheng/awesome-agent-skills | Multi-language catalog | 1.8K ⭐ |
| [Stripe](https://github.com/stripe/ai) | stripe/ai | Payment integrations | Official |
| [Cloudflare](https://github.com/cloudflare/skills) | cloudflare/skills | Workers, Pages, AI | Official |
| [Supabase](https://github.com/supabase/agent-skills) | supabase/agent-skills | PostgreSQL best practices | Official |
| [Trail of Bits](https://github.com/trailofbits/skills) | trailofbits/skills | Security (20+ skills) | Official |
| [Expo](https://github.com/expo/skills) | expo/skills | React Native | Official |
| [Sentry](https://github.com/getsentry/skills) | getsentry/skills | Code review, PR automation | Official |
| [Google Labs Stitch](https://github.com/google-labs-code/stitch-skills) | google-labs-stitch | MCP server skills | Google |
| [ComposioHQ](https://github.com/ComposioHQ/awesome-claude-skills) | composiohq/awesome-claude-skills | 20+ productivity skills | 1K+ integrations |
| [Better Auth](https://github.com/better-auth/skills) | better-auth/skills | Authentication | Official |
| [Tinybird](https://github.com/tinybirdco/tinybird-agent-skills) | tinybird/tinybird-agent-skills | Analytics | Official |
| [Neon Database](https://github.com/neondatabase/agent-skills) | neondatabase/agent-skills | Serverless Postgres | Official |
| [fal.ai](https://github.com/fal-ai-community/skills) | fal-ai/skills | AI models, image/video | Official |
| [Remotion](https://github.com/remotion-dev/skills) | remotion/skills | Video creation | Official |
| [nginity](https://github.com/alirezarezvani/claude-skills) | nginity/claude-skills | Enterprise skills | Official |
| [travisvn](https://github.com/travisvn/awesome-claude-skills) | travisvn/awesome-claude-skills | Community curated | Community |

### Community Collections

| Provider | Repository | Skills | Stars |
|----------|-----------|--------|-------|
| [SkillCreator.ai](https://github.com/skillcreatorai/Ai-Agent-Skills) | skillcreatorai/Ai-Agent-Skills | 47 | 624 ⭐ |
| [iOS Simulator](https://github.com/conorluddy/ios-simulator-skill) | ios-simulator-skill | 1 | 395 ⭐ |
| [Claude Marketplace](https://github.com/mhattingpete/claude-skills-marketplace) | claude-skills-marketplace | 18 | 271 ⭐ |
| [CSV Summarizer](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill) | csv-summarizer-skill | 1 | 193 ⭐ |
| [Tapestry Skills](https://github.com/michalparkola/tapestry-skills-for-claude-code) | tapestry-skills | 4 | 181 ⭐ |
| [AWS Skills](https://github.com/zxkane/aws-skills) | aws-skills | 5 | 101 ⭐ |
| [FFUF Web Fuzzing](https://github.com/jthack/ffuf_claude_skill) | ffuf-skill | 1 | 100 ⭐ |
| [D3.js Visualization](https://github.com/chrisvoncsefalvay/claude-d3js-skill) | d3js-skill | 1 | 83 ⭐ |
| [EPUB Converter](https://github.com/smerchek/claude-epub-skill) | epub-skill | 1 | 56 ⭐ |
| [Sanjay AI Skills](https://github.com/sanjay3290/ai-skills) | ai-skills | 12 | 43 ⭐ |
| [PICT Test Cases](https://github.com/omkamal/pypict-claude-skill) | pypict-skill | 1 | 28 ⭐ |
| [Family History](https://github.com/emaynard/claude-family-history-research-skill) | family-history-skill | 1 | 28 ⭐ |
| [Move Code Quality](https://github.com/1NickPappas/move-code-quality-skill) | move-quality-skill | 1 | 10 ⭐ |

**Total: 250+ skills • 150K+ combined stars**

[View all 41 providers →](https://dmgrok.github.io/agent_skills_directory/)

### Similar Directories & Listings

- 🌟 **[heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills)** - Curated list of agent skills and frameworks
- 🌟 **[Prat011/awesome-llm-skills](https://github.com/Prat011/awesome-llm-skills)** - Comprehensive collection of LLM agent skills
- 📖 **[Agent Skills Spec](https://agentskills.io/specification)** - Standard specification for agent skills

---

## Quick Start

### Installation

**macOS (Homebrew)**
```bash
brew install dmgrok/tap/skillsdir
```

**Linux/macOS (Install Script)**
```bash
curl -fsSL https://raw.githubusercontent.com/dmgrok/agent_skills_directory/main/install.sh | bash
```

**Python (pip)**
```bash
pip install skillsdir
```

---

## Usage

### 🎯 Smart Recommendations

Let the CLI analyze your project and recommend the best skills:

```bash
# Analyze current directory
skillsdir suggest

# Analyze specific project
skillsdir suggest /path/to/my-react-app

# Show detailed analysis
skillsdir suggest --verbose

# Optional: Enhance with LLM (requires Perplexity MCP)
skillsdir suggest --llm
```

**Example Output:**
```
1. playwright-skill/playwright-skill ⭐0 (high)
   Complete browser automation with Playwright...
   │ 🟢 Active • Updated: 15d ago • High Quality • 13 similar
   → tags match: playwright, testing; testing domain match

2. skillcreatorai/react-best-practices ⭐0 (high)
   React development guidelines with hooks...
   │ 🟡 Maintained • Updated: 45d ago • Good Quality • 3 similar
   → tags match: react; 4 keyword matches; frontend domain match
```

**How It Works:**
1. **README Analysis** - Extracts keywords and technical terms
2. **File Structure** - Detects languages, frameworks, file types
3. **Smart Pre-filtering** - Reduces 245+ skills to top 30 most relevant (88% reduction)
4. **Sophisticated Scoring** - Multi-factor algorithm with domain detection
5. **Rich Output** - Quality scores, maintenance status, similar skills count

**Scoring Algorithm:**
- Name matches (30pts) - Direct keyword in skill name
- Tag matches (25pts) - README keywords in skill tags
- Language/framework (20pts) - Tech stack alignment
- Domain detection (15pts) - API, database, testing, devops, etc.
- Quality score (10pts) - Documentation completeness
- Maintenance (8pts) - Active vs abandoned
- Provider trust (3pts) - Official sources

**No LLM Required!** Works 100% locally with excellent results.

### 🔍 Search & Discover

```bash
# Keyword search
skillsdir search "pdf"

# View detailed skill info
skillsdir info anthropic/pdf
```

**Search Output Shows:**
- Quality score (⭐0-100)
- Maintenance status (🟢 Active, 🟡 Maintained, 🟠 Stale, 🔴 Abandoned)
- Days since last update
- Tags and categories
- Installation status

### 📦 Install & Manage Skills

```bash
# Install globally (default)
skillsdir install anthropic/pdf

# Install to project (auto-detects your agent)
skillsdir install anthropic/pdf --project

# Install for specific agent
skillsdir install anthropic/pdf -p --agent claude   # → .claude/skills/
skillsdir install anthropic/pdf -p --agent copilot  # → .github/skills/
skillsdir install anthropic/pdf -p --agent codex    # → .codex/skills/
skillsdir install anthropic/pdf -p --agent cursor   # → .cursor/skills/

# Install specific version
skillsdir install anthropic/pdf@1.2.0

# List installed skills
skillsdir list
skillsdir list --json

# Update all skills
skillsdir update

# Remove a skill
skillsdir uninstall anthropic/pdf
```

### 🛠️ Create & Publish Skills

```bash
# Create new skill.json
skillsdir init

# Validate before publishing
skillsdir validate

# Publish to GitHub
skillsdir login
skillsdir publish

# Submit to official directory
skillsdir publish --submit
```

---

## Quality Indicators

### 🌟 Quality Score (0-100)
- **Maintenance** (50pts): Active=50, Maintained=40, Stale=20, Abandoned=5
- **Documentation** (30pts): Scripts=10, References=10, Assets=10
- **Provider Trust** (20pts): Official=20, Community=10

### 🟢 Maintenance Status
- **🟢 Active**: Updated <30 days ago
- **🟡 Maintained**: Updated <6 months ago
- **🟠 Stale**: Updated <1 year ago
- **🔴 Abandoned**: Updated >1 year ago

### 🔗 Similar Skills
Shows how many alternative skills exist with similar:
- Categories
- Tags (2+ overlap)
- Name keywords
- Description keywords

This helps you explore options and make informed comparisons.
# Create a new skill
skillsdir init

# Validate before publishing
skills validate .

# Publish to GitHub
skills login
skillsdir publish

# Submit to official directory
skillsdir publish --submit
```

---

## Supported Agents & Paths

| Agent | Project Path | Personal Path | Auto-Detection |
|-------|--------------|---------------|----------------|
| **Claude** | `.claude/skills/` | `~/.claude/skills/` | `CLAUDE.md`, `.claude/` |
| **Copilot** | `.github/skills/` | `~/.copilot/skills/` | `.github/copilot-instructions.md` |
| **Codex** | `.codex/skills/` | `~/.codex/skills/` | `AGENTS.md` |
| **Cursor** | `.cursor/skills/` | `~/.cursor/skills/` | `.cursorrules` |

---

## API Access

### Catalog API

The skills catalog is a JSON file updated daily at 06:00 UTC.

**CDN Endpoints:**
- **Latest:** `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.json`
- **Minified:** `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.min.json`
- **Versioned:** `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@v2026.01.26/catalog.json`

**Example Usage:**
```python
import requests

catalog = requests.get(
    "https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.json"
).json()

# Filter by quality and maintenance
quality_skills = [
    s for s in catalog["skills"] 
    if s["quality_score"] >= 80 
    and s["maintenance_status"] == "active"
]

# Group by category
from collections import defaultdict
by_category = defaultdict(list)
for skill in catalog["skills"]:
    by_category[skill["category"]].append(skill["id"])
```

---

## Contributing

### 🚀 Add Your Skills

Want to include your skills in the directory?

1. **[Create a Provider Issue](https://github.com/dmgrok/agent_skills_directory/issues/new?template=new-provider.yml)**
2. Our validation system checks:
   - ✅ Valid SKILL.md format with YAML frontmatter
   - ✅ License compatibility (MIT, Apache 2.0, etc.)
   - ✅ No hardcoded secrets (gitleaks scan)
   - ✅ No prompt injection attacks (Lakera Guard)
   - ✅ LGTM validation score 70+
3. Auto-PR created if validation passes
4. Skills appear in next daily aggregation

**See:** [Issue #11](https://github.com/dmgrok/agent_skills_directory/issues/11) for example submission

### 🐛 Report Issues

Found a bug or have a feature request? [Open an issue](https://github.com/dmgrok/agent_skills_directory/issues/new)

### 💻 Contribute Code

PRs welcome! Check out the [development guide](.github/copilot-instructions.md) for:
- Project architecture
- Aggregation pipeline
- CLI development
- Testing procedures

---

## Using Your Own Skills Repository

**For enterprises and teams needing governance and control.**

You can create your own private skills repository instead of using the public catalog. This is ideal for:

- **Security & Compliance** — Keep proprietary skills internal
- **Governance** — Control and audit skill usage across your organization
- **Custom Skills** — Share organization-specific workflows
- **Air-gapped Environments** — No external dependencies

### Setting Up a Private Repository

1. **Create a GitHub repository** with your skills:

```
your-org/internal-skills/
├── skills/
│   ├── security-audit/
│   │   ├── skill.json
│   │   └── SKILL.md
│   ├── compliance-check/
│   │   ├── skill.json
│   │   └── SKILL.md
│   └── ...
```

2. **Point the CLI to your repository**:

```bash
skillsdir config set registry https://cdn.jsdelivr.net/gh/your-org/internal-skills@main/catalog.json
```

3. **Generate your catalog**:

```bash
# Fork this repo and adjust PROVIDERS in scripts/aggregate.py
PROVIDERS = {
    "your-org": {
        "name": "Your Organization",
        "repo": "https://github.com/your-org/internal-skills",
        "api_tree_url": "https://api.github.com/repos/your-org/internal-skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/your-org/internal-skills/main",
        "skills_path_prefix": "skills/",
    },
}

python scripts/aggregate.py  # Generates catalog.json
```

4. **Distribute to your team**:

```bash
# Team members configure their CLI
skillsdir config set registry https://your-internal-cdn/catalog.json

# Now they can use your skills
skillsdir search "security"
skillsdir install your-org/security-audit
```

### Benefits for Enterprises

- **Centralized Management** — Single source of truth for approved skills
- **Version Control** — Pin skills to specific versions organization-wide
- **Audit Trail** — Track skill usage and updates via Git history
- **Custom Policies** — Enforce security, compliance, and coding standards
- **Private Hosting** — Host on internal infrastructure (S3, CDN, etc.)

---

## Creating Skills

A skill is a directory with two files:

```
my-skill/
├── skill.json    # Metadata (like package.json)
└── SKILL.md      # Instructions for the agent
```

### skill.json

```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "description": "What this skill does",
  "author": "your-username",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "runtime": "universal"
}
```

### SKILL.md

```markdown
---
name: My Skill
version: 1.0.0
description: What this skill does
---

# My Skill

Instructions for the AI agent on how to use this skill...
```

### Publish

```bash
cd my-skill
skills validate .    # Check for issues
skills login         # Authenticate with GitHub
skillsdir publish       # Push to GitHub
skillsdir publish --submit  # Request inclusion in directory
```

---

## Contributing

There are several ways to contribute skills to the directory:

### 1. Publish Your Own Skill (Easiest)

Create a skill and publish it directly:

```bash
# Create your skill
mkdir my-skill && cd my-skill
skillsdir init                      # Interactive setup

# Publish to GitHub + request directory inclusion
skills login                     # Authenticate with GitHub
skillsdir publish --submit          # Creates repo + submits to directory
```

This will:
1. Create a GitHub repo `your-username/skill-my-skill`
2. Push your `skill.json` and `SKILL.md`
3. Open a PR to add you as a single-skill provider

### 2. Contribute to an Existing Provider

Add your skill to an existing provider repository. Since we scan providers daily, your skill will appear automatically!

**Recommended providers accepting contributions:**

| Provider | How to Contribute |
|----------|-------------------|
| [skillcreatorai/Ai-Agent-Skills](https://github.com/skillcreatorai/Ai-Agent-Skills) | Fork → Add skill in `skills/` → PR |
| [sanjay3290/ai-skills](https://github.com/sanjay3290/ai-skills) | Fork → Add skill in `skills/` → PR |
| [mhattingpete/claude-skills-marketplace](https://github.com/mhattingpete/claude-skills-marketplace) | Fork → Add skill → PR |

### 3. Add a New Provider Source

Have a repository with multiple skills? Request to add it as a provider:

**Option A: Open an issue**

[➕ Request New Provider](https://github.com/dmgrok/agent_skills_directory/issues/new?labels=new-source&title=[New+Provider]+your-org/repo-name)

**Option B: Submit a PR** editing `scripts/aggregate.py`:

```python
PROVIDERS = {
    "your-org": {
        "name": "Your Organization",
        "repo": "https://github.com/your-org/skills-repo",
        "api_tree_url": "https://api.github.com/repos/your-org/skills-repo/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/your-org/skills-repo/main",
        "skills_path_prefix": "skills/",  # or "" for root-level SKILL.md
    },
}
```

### Provider Requirements

For a repository to be scanned as a provider:

- ✅ Each skill has a `SKILL.md` file with YAML frontmatter (`name`, `description`)
- ✅ Public GitHub repository
- ✅ Skills in a consistent path (e.g., `skills/*/SKILL.md` or root `SKILL.md`)

### Local Development

```bash
git clone https://github.com/dmgrok/agent_skills_directory.git
cd agent_skills_directory
pip install -e ".[validation]"
python scripts/aggregate.py      # Test aggregation locally
pytest                           # Run tests
```

---

## License

MIT License - Individual skills retain their original licenses.

---

## Related Projects

- 🌐 **[Browse Skills](https://dmgrok.github.io/agent_skills_directory/)** - Interactive web catalog
- 🔌 **[MCP Mother Skills](https://github.com/dmgrok/mcp_mother_skills)** - MCP server integration  
- 📖 **[Agent Skills Spec](https://agentskills.io/specification)** - Standard specification
- 🛡️ **[LGTM Agent Skills](https://github.com/dmgrok/LGTM_agent_skills)** - Quality validation tool
- 💻 **[skills.sh](https://skills.sh)** - Package manager for agent skills

---

**[🐛 Issues](https://github.com/dmgrok/agent_skills_directory/issues) • [💬 Discussions](https://github.com/dmgrok/agent_skills_directory/discussions) • [📊 Changelog](CHANGELOG.md)**
