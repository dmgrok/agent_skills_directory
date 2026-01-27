# skills

**The package manager for AI agent skills.**

```bash
brew install dmgrok/tap/skills
```

[![npm-like CLI](https://img.shields.io/badge/CLI-npm--like-CB3837?logo=npm)](https://github.com/dmgrok/agent_skills_directory/releases)
[![Skills](https://img.shields.io/badge/Skills-174-blue)](https://dmgrok.github.io/agent_skills_directory/)
[![Providers](https://img.shields.io/badge/Providers-24-green)](https://dmgrok.github.io/agent_skills_directory/)
[![Stars](https://img.shields.io/badge/Combined%20Stars-136K+-yellow)](https://dmgrok.github.io/agent_skills_directory/)

---

## What is this?

**skills** is to AI agents what **npm** is to JavaScript.

Search, install, publish, and manage reusable skills for Claude, Copilot, Codex, and Cursor—all from your terminal.

```bash
skills search "web scraping"     # Find skills
skills install anthropic/pdf     # Install a skill
skills publish                   # Share your own
```

🌐 **[Browse 174+ Skills Online →](https://dmgrok.github.io/agent_skills_directory/)**

---

## Skills Providers

This directory aggregates skills from **24 provider repositories** across the AI agent ecosystem:

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

**Total: 177 skills • 136K+ combined stars**

[View all 24 providers →](https://dmgrok.github.io/agent_skills_directory/)

### Similar Directories & Listings

- 🌟 **[heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills)** - Curated list of agent skills and frameworks
- 🌟 **[Prat011/awesome-llm-skills](https://github.com/Prat011/awesome-llm-skills)** - Comprehensive collection of LLM agent skills
- 📖 **[Agent Skills Spec](https://agentskills.io/specification)** - Standard specification for agent skills

---

## Quick Install

### macOS (Homebrew)

```bash
brew install dmgrok/tap/skills
```

### One-liner (macOS/Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/dmgrok/agent_skills_directory/main/install.sh | sh
```

### Direct Download

| Platform | Download |
|----------|----------|
| **macOS** (Apple Silicon & Intel) | [skills-macos-arm64](https://github.com/dmgrok/agent_skills_directory/releases/latest/download/skills-macos-arm64) |
| **Linux** (x64) | [skills-linux-x64](https://github.com/dmgrok/agent_skills_directory/releases/latest/download/skills-linux-x64) |
| **Windows** (x64) | [skills-windows-x64.exe](https://github.com/dmgrok/agent_skills_directory/releases/latest/download/skills-windows-x64.exe) |

### From Source (if you prefer Python)

```bash
git clone https://github.com/dmgrok/agent_skills_directory.git
cd agent_skills_directory && pip install -e .
```

---

## Usage

### Search & Discover

```bash
# Search by keyword
skills search "pdf"

# Browse by provider
skills search --provider anthropic

# View skill details
skills info anthropic/pdf
```

### Install Skills

```bash
# Install globally (default)
skills install anthropic/pdf

# Install to project (auto-detects your agent)
skills install anthropic/pdf --project

# Install for specific agent
skills install anthropic/pdf -p --agent claude   # → .claude/skills/
skills install anthropic/pdf -p --agent copilot  # → .github/skills/
skills install anthropic/pdf -p --agent codex    # → .codex/skills/
skills install anthropic/pdf -p --agent cursor   # → .cursor/skills/

# Install specific version
skills install anthropic/pdf@1.2.0
```

### Manage Skills

```bash
# List installed skills
skills list
skills list --json

# Update all skills
skills update

# Remove a skill
skills uninstall anthropic/pdf

# Detect which agent you're using
skills detect
```

### Create & Publish

```bash
# Create a new skill
skills init

# Validate before publishing
skills validate .

# Publish to GitHub
skills login
skills publish

# Submit to official directory
skills publish --submit
```

---

## Supported Agents

| Agent | Project Path | Personal Path | Detection |
|-------|--------------|---------------|-----------|
| **Claude** | `.claude/skills/` | `~/.claude/skills/` | `CLAUDE.md` |
| **Copilot** | `.github/skills/` | `~/.copilot/skills/` | `.github/copilot-instructions.md` |
| **Codex** | `.codex/skills/` | `~/.codex/skills/` | `AGENTS.md` |
| **Cursor** | `.cursor/skills/` | `~/.cursor/skills/` | `.cursorrules` |

---

## Catalog API

The skills catalog is a JSON file updated daily at 06:00 UTC.

### Endpoints

| Format | URL |
|--------|-----|
| **JSON (CDN)** | `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.json` |
| **Minified** | `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.min.json` |
| **Bundles** | `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/bundles.json` |
| **Pinned Version** | `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@v2026.01.26/catalog.json` |

### Example

```python
import requests

catalog = requests.get(
    "https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.json"
).json()

# List skills
for skill in catalog["skills"]:
    print(f"{skill['id']}: {skill['description']}")

# Filter by category
dev_skills = [s for s in catalog["skills"] if s["category"] == "development"]
```

---

## Providers

We aggregate skills from **24 repositories** with **136K+ combined GitHub stars**:

### Major Providers

| Provider | Repository | Skills | ⭐ |
|----------|------------|:------:|:--:|
| **Anthropic** | [anthropics/skills](https://github.com/anthropics/skills) | 16 | 54K |
| **Obra** | [obra/superpowers](https://github.com/obra/superpowers) | 14 | 36K |
| **GitHub** | [github/awesome-copilot](https://github.com/github/awesome-copilot) | 26 | 19K |
| **Vercel** | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 3 | 17K |
| **OpenAI** | [openai/skills](https://github.com/openai/skills) | 12 | 2K |
| **HuggingFace** | [huggingface/skills](https://github.com/huggingface/skills) | 8 | 1K |

### Community

| Provider | Repository | Skills | ⭐ |
|----------|------------|:------:|:--:|
| **SkillCreator.ai** | [skillcreatorai/Ai-Agent-Skills](https://github.com/skillcreatorai/Ai-Agent-Skills) | 47 | 620 |
| **Claude Marketplace** | [mhattingpete/claude-skills-marketplace](https://github.com/mhattingpete/claude-skills-marketplace) | 18 | 267 |
| **NotebookLM** | [PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill) | 1 | 2.7K |
| **Playwright** | [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill) | 1 | 1.5K |

[View all 24 providers →](https://dmgrok.github.io/agent_skills_directory/)

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
skills config set registry https://cdn.jsdelivr.net/gh/your-org/internal-skills@main/catalog.json
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
skills config set registry https://your-internal-cdn/catalog.json

# Now they can use your skills
skills search "security"
skills install your-org/security-audit
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
skills publish       # Push to GitHub
skills publish --submit  # Request inclusion in directory
```

---

## Contributing

### Add a Provider

Edit `scripts/aggregate.py`:

```python
PROVIDERS = {
    "your-org": {
        "name": "Your Organization",
        "repo": "https://github.com/your-org/skills",
        "api_tree_url": "https://api.github.com/repos/your-org/skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/your-org/skills/main",
        "skills_path_prefix": "skills/",
    },
}
```

### Local Development

```bash
git clone https://github.com/dmgrok/agent_skills_directory.git
cd agent_skills_directory
pip install -e ".[validation]"
python scripts/aggregate.py
pytest
```

---

## Related

- 🌐 [Browse Skills](https://dmgrok.github.io/agent_skills_directory/) — Interactive catalog
- 🔌 [MCP Mother Skills](https://github.com/dmgrok/mcp_mother_skills) — MCP server integration
- 📖 [Agent Skills Spec](https://agentskills.io/specification) — Standard specification

---

## License

MIT. Individual skills retain their original licenses.
