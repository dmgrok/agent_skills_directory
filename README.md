# Agent Skills Directory

**Intelligent skill discovery for AI agents.** Find, install, and manage quality-validated skills from 40+ official providers — all from one place.

```bash
skillsdir suggest           # Smart recommendations for your project
skillsdir search "testing"  # Search 130+ curated skills
skillsdir install anthropic/pdf  # Install with one command
```

[![Skills](https://img.shields.io/endpoint?url=https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/exports/badge-skills.json)](https://dmgrok.github.io/agent_skills_directory/)
[![Providers](https://img.shields.io/endpoint?url=https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/exports/badge-providers.json)](https://dmgrok.github.io/agent_skills_directory/)
[![Quality Tracked](https://img.shields.io/endpoint?url=https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/exports/badge-quality.json)](https://dmgrok.github.io/agent_skills_directory/)

---

## Why This Exists

There are thousands of AI agent skills scattered across GitHub. Which ones work? Which are maintained? Which fit your project?

We aggregate, validate, and score skills from **40+ official providers** so you can make informed decisions — no guesswork.

| Feature | Description |
|---------|-------------|
| 🎯 **Smart Recommendations** | Analyzes your project and suggests relevant skills |
| 📊 **Quality Scoring** | 0–100 points based on docs, maintenance, and trust |
| 🟢 **Maintenance Tracking** | Active · Maintained · Stale · Abandoned |
| 🛡️ **Security Validated** | Scanned for secrets and prompt injection |
| 🏢 **Official Sources** | Anthropic, OpenAI, GitHub, Vercel, Stripe, Cloudflare + more |
| 💯 **100% Local** | No LLM or external API required |

**[Browse all skills →](https://dmgrok.github.io/agent_skills_directory/)**

---

## Install

```bash
# macOS
brew install dmgrok/tap/skillsdir

# Linux / macOS
curl -fsSL https://raw.githubusercontent.com/dmgrok/agent_skills_directory/main/install.sh | bash

# Python
pip install skillsdir
```

---

## Usage

### Get recommendations for your project

```bash
skillsdir suggest                      # Analyze current directory
skillsdir suggest /path/to/project     # Analyze specific project
skillsdir suggest --verbose            # Show scoring details
```

The `suggest` command reads your README, detects languages and frameworks, and ranks skills using a multi-factor scoring algorithm — entirely offline, no LLM needed.

### Search and explore

```bash
skillsdir search "pdf extraction"      # Keyword search
skillsdir info anthropic/pdf           # Detailed skill info
```

### Install and manage

```bash
skillsdir install anthropic/pdf                     # Install globally
skillsdir install anthropic/pdf --project            # Install to project (auto-detects agent)
skillsdir install anthropic/pdf -p --agent claude    # → .claude/skills/
skillsdir install anthropic/pdf -p --agent copilot   # → .github/skills/
skillsdir install anthropic/pdf -p --agent codex     # → .codex/skills/
skillsdir install anthropic/pdf -p --agent cursor    # → .cursor/skills/

skillsdir list                         # List installed skills
skillsdir update                       # Update all skills
skillsdir uninstall anthropic/pdf      # Remove a skill
```

### Create and publish

```bash
skillsdir init               # Create a new skill.json
skillsdir validate           # Validate your skill
skillsdir login              # Authenticate with GitHub
skillsdir publish            # Push to GitHub
skillsdir publish --submit   # Request inclusion in directory
```

---

## Providers

Skills are aggregated from 40+ repositories across the AI agent ecosystem.

**[View all providers →](https://dmgrok.github.io/agent_skills_directory/)**

### Featured

| Provider | Repository | Stars |
|----------|-----------|-------|
| [Anthropic](https://github.com/anthropics/skills) | anthropics/skills | ⭐ 54K+ |
| [Obra Superpowers](https://github.com/obra/superpowers) | obra/superpowers | ⭐ 37K+ |
| [GitHub Copilot](https://github.com/github/awesome-copilot) | github/awesome-copilot | ⭐ 19K+ |
| [Vercel](https://github.com/vercel-labs/agent-skills) | vercel-labs/agent-skills | ⭐ 16K+ |
| [VoltAgent](https://github.com/VoltAgent/awesome-agent-skills) | voltagent/awesome-agent-skills | ⭐ 5K+ |
| [NotebookLM](https://github.com/PleasePrompto/notebooklm-skill) | notebooklm-skill | ⭐ 2K+ |
| [OpenAI Codex](https://github.com/openai/skills) | openai/skills | ⭐ 2K+ |
| [heilcheng](https://github.com/heilcheng/awesome-agent-skills) | heilcheng/awesome-agent-skills | ⭐ 1K+ |
| [HuggingFace](https://github.com/huggingface/skills) | huggingface/skills | ⭐ 1K+ |
| [Playwright](https://github.com/lackeyjb/playwright-skill) | playwright-skill | ⭐ 1K+ |

### Enterprise & Official

Stripe · Cloudflare · Supabase · Trail of Bits · Expo · Sentry · Google Labs Stitch · Better Auth · Tinybird · Neon Database · fal.ai · Remotion · nginity

### Community

SkillCreator.ai · iOS Simulator · Claude Marketplace · CSV Summarizer · Tapestry Skills · AWS Skills · FFUF Web Fuzzing · D3.js Visualization · EPUB Converter · Sanjay AI Skills · PICT Test Cases · Family History · Move Code Quality

---

## Quality System

Every skill gets a quality score (0–100) based on three factors:

| Factor | Max Points | Details |
|--------|-----------|---------|
| **Maintenance** | 50 | 🟢 Active (&lt;30d) = 50 · 🟡 Maintained (&lt;6mo) = 40 · 🟠 Stale (&lt;1yr) = 20 · 🔴 Abandoned = 5 |
| **Documentation** | 30 | Scripts (+10) · References (+10) · Assets (+10) |
| **Provider Trust** | 20 | Official = 20 · Community = 10 |

---

## Supported Agents

| Agent | Project Path | Auto-Detection |
|-------|-------------|----------------|
| **Claude** | `.claude/skills/` | `CLAUDE.md`, `.claude/` |
| **Copilot** | `.github/skills/` | `.github/copilot-instructions.md` |
| **Codex** | `.codex/skills/` | `AGENTS.md` |
| **Cursor** | `.cursor/skills/` | `.cursorrules` |

---

## API & Exports

The catalog is updated daily at 06:00 UTC and available via CDN:

```
https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.json
```

Pre-filtered exports for specific ecosystems:

| Export | Filter | URL |
|--------|--------|-----|
| Claude Skills | Quality ≥ 50 | [`exports/claude-skills.json`](https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/exports/claude-skills.json) |
| Copilot Skills | Quality ≥ 50 | [`exports/copilot-skills.json`](https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/exports/copilot-skills.json) |
| Premium Skills | Quality ≥ 70 | [`exports/premium-skills.json`](https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/exports/premium-skills.json) |
| Active Skills | Updated &lt; 6mo | [`exports/active-skills.json`](https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/exports/active-skills.json) |
| MCP-Compatible | Tagged `mcp` | [`exports/mcp-compatible.json`](https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/exports/mcp-compatible.json) |

```python
import requests
catalog = requests.get(
    "https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.json"
).json()

quality_skills = [s for s in catalog["skills"] if s["quality_score"] >= 80]
```

---

## Contributing

### Add your skills to the directory

1. **[Create a New Provider Issue](https://github.com/dmgrok/agent_skills_directory/issues/new?template=new-provider.yml)** with your repo details
2. Automated validation runs:
   - ✅ SKILL.md format with YAML frontmatter
   - 🔒 Secrets scan (gitleaks)
   - 🛡️ Prompt injection check (Lakera Guard)
   - 📊 Quality score ≥ 70 ([LGTM validation](https://github.com/dmgrok/LGTM_agent_skills))
3. Auto-PR created on pass → skills appear in the next daily aggregation

**See [issue #11](https://github.com/dmgrok/agent_skills_directory/issues/11) for an example submission.**

### Contribute to an existing provider

Add skills to repositories accepting contributions:
[skillcreatorai/Ai-Agent-Skills](https://github.com/skillcreatorai/Ai-Agent-Skills) · [sanjay3290/ai-skills](https://github.com/sanjay3290/ai-skills) · [mhattingpete/claude-skills-marketplace](https://github.com/mhattingpete/claude-skills-marketplace)

### Local development

```bash
git clone https://github.com/dmgrok/agent_skills_directory.git
cd agent_skills_directory
pip install -e ".[validation]"
python scripts/aggregate.py   # Test aggregation
pytest                        # Run tests
```

---

## Creating Skills

A skill is a directory with two files:

```
my-skill/
├── skill.json    # Metadata (like package.json)
└── SKILL.md      # Instructions for the agent
```

<details>
<summary><b>skill.json example</b></summary>

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
</details>

<details>
<summary><b>SKILL.md example</b></summary>

```markdown
---
name: My Skill
version: 1.0.0
description: What this skill does
---

# My Skill

Instructions for the AI agent on how to use this skill...
```
</details>

---

## Private Registries

For teams needing governance and control, point the CLI at your own catalog:

```bash
skillsdir config set registry https://your-cdn/catalog.json
```

Fork this repo, update `PROVIDERS` in `scripts/aggregate.py`, and run `python scripts/aggregate.py` to generate your own `catalog.json`.

---

## CI/CD Validation

```yaml
# .github/workflows/validate.yml
name: Validate Skill
on: [push, pull_request]
jobs:
  validate:
    uses: dmgrok/agent_skills_directory/.github/workflows/validate-skill.yml@main
    with:
      skill-path: '.'
```

---

## Badges

```markdown
[![Listed on Agent Skills Directory](https://img.shields.io/badge/Listed_on-Agent_Skills_Directory-6366f1?style=flat)](https://dmgrok.github.io/agent_skills_directory/)
```

Dynamic (auto-updated):
```markdown
![Skills](https://img.shields.io/endpoint?url=https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/exports/badge-skills.json)
![Providers](https://img.shields.io/endpoint?url=https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/exports/badge-providers.json)
```

---

## Related Projects

- 🌐 [Browse Skills](https://dmgrok.github.io/agent_skills_directory/) — Interactive web catalog
- 🔌 [MCP Mother Skills](https://github.com/dmgrok/mcp_mother_skills) — MCP server integration
- 🛡️ [LGTM Agent Skills](https://github.com/dmgrok/LGTM_agent_skills) — Quality validation tool
- 📖 [Agent Skills Spec](https://agentskills.io/specification) — Standard specification
- 💻 [skills.sh](https://skills.sh) — Package manager for agent skills

---

MIT License — Individual skills retain their original licenses.

**[🐛 Issues](https://github.com/dmgrok/agent_skills_directory/issues) · [💬 Discussions](https://github.com/dmgrok/agent_skills_directory/discussions) · [📊 Changelog](CHANGELOG.md)**
