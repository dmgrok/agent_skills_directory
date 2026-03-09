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

## Skills Listing

<!-- AUTO-GENERATED SKILLS TABLE START -->
## 📋 All Skills — 687 skills across 43 providers · v2026.03.06

> Auto-generated daily · [Browse interactively →](https://dmgrok.github.io/agent_skills_directory/)  
> Legend: 🔒 Secrets scan · 🛡️ Injection check · 📝 Content · 🔄 No duplicate · ✅ Full skill · S=Scripts · R=References · A=Assets

| Skill | Provider | Compat | 🔒 | 🛡️ | 📝 | 🔄 | ✅ | S | R | A | Quality | Status | Dup |
|-------|----------|--------|----|----|----|----|---|---|---|---|---------|--------|-----|
| [playwright](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/playwright/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100/100 | 🟢 active |  |
| [skill-creator](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100/100 | 🟢 active |  |
| [slides](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/slides/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100/100 | 🟢 active |  |
| [app-store-optimization](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/app-store-optimization/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [aspnet-core](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/aspnet-core/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [campaign-analytics](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/campaign-analytics/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [chatgpt-apps](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/chatgpt-apps/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 90/100 | 🟢 active |  |
| [content-production](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/content-production/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [customer-success-manager](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/business-growth/customer-success-manager/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [datanalysis-credit-risk](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/datanalysis-credit-risk/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 90/100 | 🟢 active |  |
| [develop-web-game](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/develop-web-game/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟡 maintained |  |
| [emblem-ai-agent-wallet](https://raw.githubusercontent.com/EmblemCompany/Agent-skills/main/skills/emblem-ai-agent-wallet/SKILL.md) | emblemcompany | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [excalidraw-diagram-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/excalidraw-diagram-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟡 maintained |  |
| [fal-workflow](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-workflow/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 90/100 | 🟢 active |  |
| [financial-analyst](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/finance/financial-analyst/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [game-engine](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/game-engine/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [hugging-face-paper-publisher](https://raw.githubusercontent.com/huggingface/skills/main/skills/hugging-face-paper-publisher/SKILL.md) | huggingface | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟡 maintained |  |
| [imagegen](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/imagegen/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟡 maintained |  |
| [interpreting-culture-index](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/culture-index/skills/interpreting-culture-index/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [jupyter-notebook](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/jupyter-notebook/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟡 maintained |  |
| [nano-banana-pro-openrouter](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/nano-banana-pro-openrouter/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | 90/100 | 🟢 active |  |
| [openai-docs](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/openai-docs/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [openai-docs](https://raw.githubusercontent.com/openai/skills/main/skills/.system/openai-docs/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ✅ | ✅ | 90/100 | 🟢 active | 🔄 → openai/openai-docs |
| [revenue-operations](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/business-growth/revenue-operations/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [sales-engineer](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/business-growth/sales-engineer/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [scrum-master](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/project-management/scrum-master/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [senior-pm](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/project-management/senior-pm/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [skill-creator](https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 90/100 | 🟢 active |  |
| [social-media-analyzer](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/social-media-analyzer/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [sora](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/sora/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟡 maintained |  |
| [speech](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/speech/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟡 maintained |  |
| [spreadsheet](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/spreadsheet/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [transcribe](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/transcribe/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 90/100 | 🟡 maintained |  |
| [vercel-deploy](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/vercel-deploy/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | 90/100 | 🟢 active |  |
| [winui-app](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/winui-app/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 90/100 | 🟢 active |  |
| [ab-test-setup](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/ab-test-setup/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [ad-creative](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/ad-creative/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [agents-sdk](https://raw.githubusercontent.com/cloudflare/skills/main/skills/agents-sdk/SKILL.md) | cloudflare | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [analytics-tracking](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/analytics-tracking/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [appinsights-instrumentation](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/appinsights-instrumentation/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟡 maintained |  |
| [aspire](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/aspire/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [aws-cdk-development](https://raw.githubusercontent.com/zxkane/aws-skills/main/plugins/aws-cdk/skills/aws-cdk-development/SKILL.md) | aws-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [aws-solution-architect](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/aws-solution-architect/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 80/100 | 🟡 maintained |  |
| [azure-devops-cli](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/azure-devops-cli/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [azure-pricing](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/azure-pricing/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [board-deck-builder](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/board-deck-builder/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟢 active |  |
| [board-meeting](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/board-meeting/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟢 active |  |
| [building-ai-agent-on-cloudflare](https://raw.githubusercontent.com/cloudflare/skills/main/skills/building-ai-agent-on-cloudflare/SKILL.md) | cloudflare | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [building-mcp-server-on-cloudflare](https://raw.githubusercontent.com/cloudflare/skills/main/skills/building-mcp-server-on-cloudflare/SKILL.md) | cloudflare | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [building-native-ui](https://raw.githubusercontent.com/expo/skills/main/plugins/expo-app-design/skills/building-native-ui/SKILL.md) | expo | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [ceo-advisor](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/ceo-advisor/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [cfo-advisor](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/cfo-advisor/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [chro-advisor](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/chro-advisor/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [churn-prevention](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/churn-prevention/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [ciso-advisor](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/ciso-advisor/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [cloudflare](https://raw.githubusercontent.com/cloudflare/skills/main/skills/cloudflare/SKILL.md) | cloudflare | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [cloudflare-deploy](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/cloudflare-deploy/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟡 maintained |  |
| [cmo-advisor](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/cmo-advisor/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [cold-email](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/cold-email/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [competitive-intel](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/competitive-intel/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟢 active |  |
| [competitor-alternatives](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/competitor-alternatives/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [content-creator](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/content-creator/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟢 active |  |
| [content-humanizer](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/content-humanizer/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [coo-advisor](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/coo-advisor/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [copy-editing](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/copy-editing/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [copywriting](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/copywriting/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [cpo-advisor](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/cpo-advisor/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [create-web-form](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-web-form/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [cro-advisor](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/cro-advisor/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [cs-onboard](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/cs-onboard/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟢 active |  |
| [cto-advisor](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/cto-advisor/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [culture-architect](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/culture-architect/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟢 active |  |
| [debug-buttercup](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/debug-buttercup/skills/debug-buttercup/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [decision-logger](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/decision-logger/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | 80/100 | 🟢 active |  |
| [doc](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/doc/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | 80/100 | 🟡 maintained |  |
| [docx](https://raw.githubusercontent.com/anthropics/skills/main/skills/docx/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [durable-objects](https://raw.githubusercontent.com/cloudflare/skills/main/skills/durable-objects/SKILL.md) | cloudflare | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [executive-mentor](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/executive-mentor/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [fabric-lakehouse](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/fabric-lakehouse/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [fal-3d](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-3d/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [fal-audio](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-audio/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [fal-generate](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-generate/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [fal-image-edit](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-image-edit/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [fal-kling-o3](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-kling-o3/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [fal-lip-sync](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-lip-sync/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [fal-platform](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-platform/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [fal-realtime](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-realtime/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [fal-restore](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-restore/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [fal-train](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-train/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [fal-tryon](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-tryon/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [fal-upscale](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-upscale/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [fal-video-edit](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-video-edit/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [fal-vision](https://raw.githubusercontent.com/fal-ai-community/skills/main/skills/claude.ai/fal-vision/SKILL.md) | fal-ai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [figma](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/figma/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟡 maintained |  |
| [finnish-humanizer](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/finnish-humanizer/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [flowstudio-power-automate-mcp](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/flowstudio-power-automate-mcp/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [fluentui-blazor](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/fluentui-blazor/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [free-tool-strategy](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/free-tool-strategy/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [gh-address-comments](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-address-comments/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | 80/100 | 🟡 maintained |  |
| [gh-fix-ci](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | 80/100 | 🟡 maintained |  |
| [github-issues](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/github-issues/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [hugging-face-datasets](https://raw.githubusercontent.com/huggingface/skills/main/skills/hugging-face-datasets/SKILL.md) | huggingface | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | 80/100 | 🟡 maintained |  |
| [hugging-face-jobs](https://raw.githubusercontent.com/huggingface/skills/main/skills/hugging-face-jobs/SKILL.md) | huggingface | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟡 maintained |  |
| [hugging-face-model-trainer](https://raw.githubusercontent.com/huggingface/skills/main/skills/hugging-face-model-trainer/SKILL.md) | huggingface | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟡 maintained |  |
| [hugging-face-trackio](https://raw.githubusercontent.com/huggingface/skills/main/skills/hugging-face-trackio/SKILL.md) | huggingface | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [internal-narrative](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/internal-narrative/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟢 active |  |
| [interview-system-designer](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering/interview-system-designer/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟢 active |  |
| [let-fate-decide](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/let-fate-decide/skills/let-fate-decide/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [make-repo-contribution](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/make-repo-contribution/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ | 80/100 | 🟢 active |  |
| [marketing-context](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/marketing-context/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | 80/100 | 🟢 active |  |
| [marketing-demand-acquisition](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/marketing-demand-acquisition/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [mcp-builder](https://raw.githubusercontent.com/anthropics/skills/main/skills/mcp-builder/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟡 maintained |  |
| [microsoft-skill-creator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/microsoft-skill-creator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [native-data-fetching](https://raw.githubusercontent.com/expo/skills/main/plugins/expo-app-design/skills/native-data-fetching/SKILL.md) | expo | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [netlify-deploy](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/netlify-deploy/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟡 maintained |  |
| [noob-mode](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/noob-mode/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [notebooklm](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/notebooklm/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [notion-knowledge-capture](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/notion-knowledge-capture/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟡 maintained |  |
| [notion-meeting-intelligence](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/notion-meeting-intelligence/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟡 maintained |  |
| [notion-research-documentation](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/notion-research-documentation/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟡 maintained |  |
| [notion-spec-to-implementation](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/notion-spec-to-implementation/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟡 maintained |  |
| [org-health-diagnostic](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/org-health-diagnostic/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [paid-ads](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/paid-ads/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [pdftk-server](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/pdftk-server/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [playwright-interactive](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/playwright-interactive/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ | 80/100 | 🟢 active |  |
| [playwright-pro](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/playwright-pro/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟢 active |  |
| [pricing-strategy](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/pricing-strategy/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [prompt-engineer-toolkit](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/prompt-engineer-toolkit/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [referral-program](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/referral-program/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [render-deploy](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/render-deploy/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟡 maintained |  |
| [sandbox-sdk](https://raw.githubusercontent.com/cloudflare/skills/main/skills/sandbox-sdk/SKILL.md) | cloudflare | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [scenario-war-room](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/scenario-war-room/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [schema-markup](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/schema-markup/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [screenshot](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/screenshot/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | 80/100 | 🟡 maintained |  |
| [security-ownership-map](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/security-ownership-map/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟡 maintained |  |
| [self-improving-agent](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/self-improving-agent/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 80/100 | 🟢 active |  |
| [semgrep](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/static-analysis/skills/semgrep/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [senior-fullstack](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/senior-fullstack/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [sentry](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/sentry/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | 80/100 | 🟡 maintained |  |
| [site-architecture](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/site-architecture/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [skill-installer](https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-installer/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | 80/100 | 🟡 maintained |  |
| [skill-scanner](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/skill-scanner/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [skill-security-auditor](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering/skill-security-auditor/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [skill-writer](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/skill-writer/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [strategic-alignment](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/strategic-alignment/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [tdd-guide](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/tdd-guide/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 80/100 | 🟡 maintained |  |
| [tech-stack-evaluator](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/tech-stack-evaluator/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 80/100 | 🟡 maintained |  |
| [terraform-azurerm-set-diff-analyzer](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/terraform-azurerm-set-diff-analyzer/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 80/100 | 🟡 maintained |  |
| [upgrading-expo](https://raw.githubusercontent.com/expo/skills/main/plugins/upgrading-expo/skills/upgrading-expo/SKILL.md) | expo | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [web-coder](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/web-coder/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [winmd-api-search](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/winmd-api-search/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 80/100 | 🟢 active |  |
| [workers-best-practices](https://raw.githubusercontent.com/cloudflare/skills/main/skills/workers-best-practices/SKILL.md) | cloudflare | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 80/100 | 🟢 active |  |
| [add-educational-comments](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/add-educational-comments/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [agent-governance](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/agent-governance/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [agent-protocol](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/agent-protocol/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [agentic-actions-auditor](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/agentic-actions-auditor/skills/agentic-actions-auditor/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [agile-product-owner](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/product-team/agile-product-owner/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [ai-prompt-engineering-safety-review](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/ai-prompt-engineering-safety-review/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [ai-seo](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/ai-seo/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [algorithmic-art](https://raw.githubusercontent.com/anthropics/skills/main/skills/algorithmic-art/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ | 70/100 | 🟡 maintained |  |
| [apple-appstore-reviewer](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/apple-appstore-reviewer/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [arch-linux-triage](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/arch-linux-triage/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [architecture-blueprint-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/architecture-blueprint-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [architecture-diagram-creator](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/visual-documentation-plugin/skills/architecture-diagram-creator/SKILL.md) | claude-marketplace-visual | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 70/100 | 🟡 maintained |  |
| [aspnet-minimal-api-openapi](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/aspnet-minimal-api-openapi/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [atlassian](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/atlassian/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [aws-cost-operations](https://raw.githubusercontent.com/zxkane/aws-skills/main/plugins/aws-cost-ops/skills/aws-cost-operations/SKILL.md) | aws-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [aws-serverless-eda](https://raw.githubusercontent.com/zxkane/aws-skills/main/plugins/serverless-eda/skills/aws-serverless-eda/SKILL.md) | aws-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [az-cost-optimize](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/az-cost-optimize/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [azure-deployment-preflight](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/azure-deployment-preflight/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [azure-devops](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/azure-devops/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [azure-resource-health-diagnose](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/azure-resource-health-diagnose/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [azure-resource-visualizer](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/azure-resource-visualizer/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ | 70/100 | 🟡 maintained |  |
| [better-auth-best-practices](https://raw.githubusercontent.com/better-auth/skills/main/better-auth/best-practices/SKILL.md) | better-auth | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [bigquery-pipeline-audit](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/bigquery-pipeline-audit/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [boost-prompt](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/boost-prompt/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [breakdown-epic-arch](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/breakdown-epic-arch/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [breakdown-epic-pm](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/breakdown-epic-pm/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [breakdown-feature-implementation](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/breakdown-feature-implementation/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [breakdown-feature-prd](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/breakdown-feature-prd/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [breakdown-plan](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/breakdown-plan/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [breakdown-test](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/breakdown-test/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [burpsuite-project-parser](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/burpsuite-project-parser/skills/burpsuite-project-parser/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [capa-officer](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/ra-qm-team/capa-officer/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [centos-linux-triage](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/centos-linux-triage/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [change-management](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/change-management/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [chief-of-staff](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/chief-of-staff/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [claimable-postgres](https://raw.githubusercontent.com/neondatabase/agent-skills/main/skills/claimable-postgres/SKILL.md) | neondatabase | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [claude-api](https://raw.githubusercontent.com/anthropics/skills/main/skills/claude-api/SKILL.md) | anthropics | Claude | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [code-exemplars-blueprint-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/code-exemplars-blueprint-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [code-reviewer](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/code-reviewer/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [codeql](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/static-analysis/skills/codeql/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [comment-code-generate-a-tutorial](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/comment-code-generate-a-tutorial/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [company-os](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/company-os/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [confluence-expert](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/project-management/confluence-expert/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [containerize-aspnet-framework](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/containerize-aspnet-framework/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [containerize-aspnetcore](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/containerize-aspnetcore/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [content-strategy](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/content-strategy/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [context-engine](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/context-engine/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [context-map](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/context-map/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [conventional-commit](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/conventional-commit/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [convert-plaintext-to-md](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/convert-plaintext-to-md/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [copilot-cli-quickstart](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/copilot-cli-quickstart/SKILL.md) | github | Copilot | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [copilot-instructions-blueprint-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/copilot-instructions-blueprint-generator/SKILL.md) | github | Copilot | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [copilot-spaces](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/copilot-spaces/SKILL.md) | github | Copilot | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [copilot-usage-metrics](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/copilot-usage-metrics/SKILL.md) | github | Copilot | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [cosmosdb-datamodeling](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/cosmosdb-datamodeling/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-agentsmd](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-agentsmd/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-architectural-decision-record](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-architectural-decision-record/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-auth-skill](https://raw.githubusercontent.com/better-auth/skills/main/better-auth/create-auth/SKILL.md) | better-auth | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-github-action-workflow-specification](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-github-action-workflow-specification/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-github-issue-feature-from-specification](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-github-issue-feature-from-specification/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-github-issues-feature-from-implementation-plan](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-github-issues-feature-from-implementation-plan/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-github-issues-for-unmet-specification-requirements](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-github-issues-for-unmet-specification-requirements/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-github-pull-request-from-specification](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-github-pull-request-from-specification/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-implementation-plan](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-implementation-plan/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-llms](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-llms/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-oo-component-documentation](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-oo-component-documentation/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-readme](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-readme/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-specification](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-specification/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-spring-boot-java-project](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-spring-boot-java-project/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-spring-boot-kotlin-project](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-spring-boot-kotlin-project/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-technical-spike](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-technical-spike/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [create-tldr-page](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/create-tldr-page/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [csharp-async](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/csharp-async/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [csharp-docs](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/csharp-docs/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [csharp-mcp-server-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/csharp-mcp-server-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [csharp-mstest](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/csharp-mstest/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [csharp-nunit](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/csharp-nunit/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [csharp-tunit](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/csharp-tunit/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [csharp-xunit](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/csharp-xunit/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [dashboard-creator](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/visual-documentation-plugin/skills/dashboard-creator/SKILL.md) | claude-marketplace-visual | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 70/100 | 🟡 maintained |  |
| [dataverse-python-advanced-patterns](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/dataverse-python-advanced-patterns/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [dataverse-python-production-code](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/dataverse-python-production-code/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [dataverse-python-quickstart](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/dataverse-python-quickstart/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [dataverse-python-usecase-builder](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/dataverse-python-usecase-builder/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [debian-linux-triage](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/debian-linux-triage/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [declarative-agents](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/declarative-agents/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [deep-research](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/deep-research/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [deploy-to-vercel](https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/deploy-to-vercel/SKILL.md) | vercel | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [designing-workflow-skills](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/workflow-skill-design/skills/designing-workflow-skills/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [devcontainer-setup](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/devcontainer-setup/skills/devcontainer-setup/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [devops-rollout-plan](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/devops-rollout-plan/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [django-access-review](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/django-access-review/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [documentation-writer](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/documentation-writer/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [dotnet-best-practices](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/dotnet-best-practices/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [dotnet-design-pattern-review](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/dotnet-design-pattern-review/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [dotnet-upgrade](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/dotnet-upgrade/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [editorconfig](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/editorconfig/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [ef-core](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/ef-core/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [elevenlabs](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/elevenlabs/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [email-and-password-best-practices](https://raw.githubusercontent.com/better-auth/skills/main/better-auth/emailAndPassword/SKILL.md) | better-auth | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [email-sequence](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/email-sequence/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [entra-agent-user](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/entra-agent-user/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [expo-cicd-workflows](https://raw.githubusercontent.com/expo/skills/main/plugins/expo-deployment/skills/expo-cicd-workflows/SKILL.md) | expo | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟡 maintained |  |
| [expo-deployment](https://raw.githubusercontent.com/expo/skills/main/plugins/expo-deployment/skills/expo-deployment/SKILL.md) | expo | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [fda-consultant-specialist](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/ra-qm-team/fda-consultant-specialist/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [fedora-linux-triage](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/fedora-linux-triage/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [figma-implement-design](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/figma-implement-design/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ | 70/100 | 🟡 maintained |  |
| [finalize-agent-prompt](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/finalize-agent-prompt/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [first-ask](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/first-ask/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [flowchart-creator](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/visual-documentation-plugin/skills/flowchart-creator/SKILL.md) | claude-marketplace-visual | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 70/100 | 🟡 maintained |  |
| [folder-structure-blueprint-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/folder-structure-blueprint-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [form-cro](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/form-cro/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [founder-coach](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/founder-coach/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [fp-check](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/fp-check/skills/fp-check/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [gdpr-dsgvo-expert](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/ra-qm-team/gdpr-dsgvo-expert/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [gen-specs-as-issues](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/gen-specs-as-issues/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [generate-custom-instructions-from-codebase](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/generate-custom-instructions-from-codebase/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [gh-cli](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/gh-cli/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [gh-review-requests](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/gh-review-requests/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [gha-security-review](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/gha-security-review/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [git-flow-branch-creator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/git-flow-branch-creator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [github-copilot-starter](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/github-copilot-starter/SKILL.md) | github | Copilot | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [gmail](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/gmail/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [go-mcp-server-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/go-mcp-server-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [google-calendar](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/google-calendar/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [google-chat](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/google-chat/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [google-docs](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/google-docs/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [google-drive](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/google-drive/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [google-sheets](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/google-sheets/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [google-slides](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/google-slides/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [google-tts](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/google-tts/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [gradio](https://raw.githubusercontent.com/huggingface/skills/main/skills/huggingface-gradio/SKILL.md) | huggingface | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [hf-cli](https://raw.githubusercontent.com/huggingface/skills/main/skills/hf-cli/SKILL.md) | huggingface | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [hugging-face-dataset-viewer](https://raw.githubusercontent.com/huggingface/skills/main/skills/hugging-face-dataset-viewer/SKILL.md) | huggingface | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [hugging-face-evaluation](https://raw.githubusercontent.com/huggingface/skills/main/skills/hugging-face-evaluation/SKILL.md) | huggingface | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟡 maintained |  |
| [hugging-face-tool-builder](https://raw.githubusercontent.com/huggingface/skills/main/skills/hugging-face-tool-builder/SKILL.md) | huggingface | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [imagen](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/imagen/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [import-infrastructure-as-code](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/import-infrastructure-as-code/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [information-security-manager-iso27001](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/ra-qm-team/information-security-manager-iso27001/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [intl-expansion](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/intl-expansion/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [isms-audit-expert](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/ra-qm-team/isms-audit-expert/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [iterate-pr](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/iterate-pr/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [java-add-graalvm-native-image-support](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/java-add-graalvm-native-image-support/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [java-docs](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/java-docs/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [java-junit](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/java-junit/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [java-mcp-server-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/java-mcp-server-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [java-refactoring-extract-method](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/java-refactoring-extract-method/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [java-refactoring-remove-parameter](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/java-refactoring-remove-parameter/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [java-springboot](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/java-springboot/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [javascript-typescript-jest](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/javascript-typescript-jest/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [jira-expert](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/project-management/jira-expert/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [kotlin-mcp-server-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/kotlin-mcp-server-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [kotlin-springboot](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/kotlin-springboot/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [launch-strategy](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/launch-strategy/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [legacy-circuit-mockups](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/legacy-circuit-mockups/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [linear](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/linear/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ | 70/100 | 🟡 maintained |  |
| [ma-playbook](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/ma-playbook/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [manus](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/manus/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [markdown-to-html](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/markdown-to-html/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [marketing-ideas](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/marketing-ideas/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [marketing-ops](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/marketing-ops/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [marketing-psychology](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/marketing-psychology/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [marketing-strategy-pmm](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/marketing-strategy-pmm/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [mcp-configure](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/mcp-configure/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [mcp-copilot-studio-server-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/mcp-copilot-studio-server-generator/SKILL.md) | github | Copilot | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [mcp-create-adaptive-cards](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/mcp-create-adaptive-cards/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [mcp-create-declarative-agent](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/mcp-create-declarative-agent/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [mcp-deploy-manage-agents](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/mcp-deploy-manage-agents/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [mdr-745-specialist](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/ra-qm-team/mdr-745-specialist/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [memory-merger](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/memory-merger/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [mentoring-juniors](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/mentoring-juniors/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [microsoft-docs](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/microsoft-docs/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [mkdocs-translations](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/mkdocs-translations/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [model-recommendation](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/model-recommendation/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [modern-python](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/modern-python/skills/modern-python/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 70/100 | 🟡 maintained |  |
| [ms365-tenant-manager](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/ms365-tenant-manager/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [mssql](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/mssql/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [msstore-cli](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/msstore-cli/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [multi-stage-dockerfile](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/multi-stage-dockerfile/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [my-issues](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/my-issues/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [my-pull-requests](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/my-pull-requests/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [mysql](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/mysql/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [neon-postgres](https://raw.githubusercontent.com/neondatabase/agent-skills/main/skills/neon-postgres/SKILL.md) | neondatabase | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [next-intl-add-language](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/next-intl-add-language/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [obsidian](https://raw.githubusercontent.com/gapmiss/obsidian-plugin-skill/main/.claude/skills/obsidian/SKILL.md) | obsidian-plugin | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [onboarding-cro](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/onboarding-cro/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [openapi-to-application-code](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/openapi-to-application-code/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [organization-best-practices](https://raw.githubusercontent.com/better-auth/skills/main/better-auth/organization/SKILL.md) | better-auth | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [outline](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/outline/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [page-cro](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/page-cro/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [pdf](https://raw.githubusercontent.com/anthropics/skills/main/skills/pdf/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟡 maintained |  |
| [pdf](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/pdf/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ | 70/100 | 🟡 maintained |  |
| [penpot-uiux-design](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/penpot-uiux-design/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [php-mcp-server-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/php-mcp-server-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [playwright-automation-fill-in-form](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/playwright-automation-fill-in-form/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [playwright-explore-website](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/playwright-explore-website/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [playwright-generate-test](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/playwright-generate-test/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [polyglot-test-agent](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/polyglot-test-agent/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [postgres](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/postgres/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [postgresql-code-review](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/postgresql-code-review/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [postgresql-optimization](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/postgresql-optimization/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [power-apps-code-app-scaffold](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/power-apps-code-app-scaffold/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [power-bi-dax-optimization](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/power-bi-dax-optimization/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [power-bi-model-design-review](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/power-bi-model-design-review/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [power-bi-performance-troubleshooting](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/power-bi-performance-troubleshooting/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [power-bi-report-design-consultation](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/power-bi-report-design-consultation/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [power-platform-mcp-connector-suite](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/power-platform-mcp-connector-suite/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [powerbi-modeling](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/powerbi-modeling/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [pptx](https://raw.githubusercontent.com/anthropics/skills/main/skills/pptx/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟡 maintained |  |
| [product-manager-toolkit](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/product-team/product-manager-toolkit/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [product-strategist](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/product-team/product-strategist/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [programmatic-seo](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/programmatic-seo/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [project-workflow-analysis-blueprint-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/project-workflow-analysis-blueprint-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [prompt-builder](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/prompt-builder/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [property-based-testing](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/property-based-testing/skills/property-based-testing/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [pytest-coverage](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/pytest-coverage/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [python-mcp-server-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/python-mcp-server-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [qms-audit-expert](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/ra-qm-team/qms-audit-expert/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [quality-documentation-manager](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/ra-qm-team/quality-documentation-manager/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [quality-manager-qmr](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/ra-qm-team/quality-manager-qmr/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [quality-manager-qms-iso13485](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/ra-qm-team/quality-manager-qms-iso13485/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [quasi-coder](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/quasi-coder/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [react:components](https://raw.githubusercontent.com/google-labs-code/stitch-skills/main/skills/react-components/SKILL.md) | google-labs-stitch | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [readme-blueprint-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/readme-blueprint-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [refactor-method-complexity-reduce](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/refactor-method-complexity-reduce/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [refactor-plan](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/refactor-plan/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [regulatory-affairs-head](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/ra-qm-team/regulatory-affairs-head/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [remember](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/remember/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [remember-interactive-programming](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/remember-interactive-programming/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [remotion-best-practices](https://raw.githubusercontent.com/remotion-dev/skills/main/skills/remotion/SKILL.md) | remotion | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [repo-story-time](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/repo-story-time/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [review-and-refactor](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/review-and-refactor/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [risk-management-specialist](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/ra-qm-team/risk-management-specialist/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [ruby-mcp-server-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/ruby-mcp-server-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [rust-mcp-server-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/rust-mcp-server-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [second-opinion](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/second-opinion/skills/second-opinion/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [security-best-practices](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/security-best-practices/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [security-review](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/security-review/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [security-threat-model](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/security-threat-model/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [senior-architect](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/senior-architect/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [senior-backend](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/senior-backend/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [senior-computer-vision](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/senior-computer-vision/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [senior-data-engineer](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/senior-data-engineer/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [senior-data-scientist](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/senior-data-scientist/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [senior-devops](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/senior-devops/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [senior-frontend](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/senior-frontend/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [senior-ml-engineer](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/senior-ml-engineer/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [senior-prompt-engineer](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/senior-prompt-engineer/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [senior-qa](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/senior-qa/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [senior-secops](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/senior-secops/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [senior-security](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/senior-security/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [seo-audit](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/seo-audit/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [shareplay-developer](https://raw.githubusercontent.com/tomkrikorian/visionOSAgents/main/skills/shareplay-developer/SKILL.md) | visionos-agents | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [shuffle-json-data](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/shuffle-json-data/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [signup-flow-cro](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/signup-flow-cro/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [social-content](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/social-content/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [social-media-manager](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/social-media-manager/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [sponsor-finder](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/sponsor-finder/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [sql-code-review](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/sql-code-review/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [sql-optimization](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/sql-optimization/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [sred-project-organizer](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/sred-project-organizer/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [stripe-best-practices](https://raw.githubusercontent.com/stripe/ai/main/skills/stripe-best-practices/SKILL.md) | stripe | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [structured-autonomy-generate](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/structured-autonomy-generate/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [structured-autonomy-implement](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/structured-autonomy-implement/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [structured-autonomy-plan](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/structured-autonomy-plan/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [suggest-awesome-github-copilot-agents](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/suggest-awesome-github-copilot-agents/SKILL.md) | github | Copilot | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [suggest-awesome-github-copilot-instructions](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/suggest-awesome-github-copilot-instructions/SKILL.md) | github | Copilot | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [suggest-awesome-github-copilot-prompts](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/suggest-awesome-github-copilot-prompts/SKILL.md) | github | Copilot | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [suggest-awesome-github-copilot-skills](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/suggest-awesome-github-copilot-skills/SKILL.md) | github | Copilot | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [supabase-postgres-best-practices](https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase-postgres-best-practices/SKILL.md) | supabase | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [swift-mcp-server-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/swift-mcp-server-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [technical-doc-creator](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/visual-documentation-plugin/skills/technical-doc-creator/SKILL.md) | claude-marketplace-visual | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 70/100 | 🟡 maintained |  |
| [technology-stack-blueprint-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/technology-stack-blueprint-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [timeline-creator](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/visual-documentation-plugin/skills/timeline-creator/SKILL.md) | claude-marketplace-visual | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | 70/100 | 🟡 maintained |  |
| [tinybird](https://raw.githubusercontent.com/tinybirdco/tinybird-agent-skills/main/skills/tinybird-best-practices/SKILL.md) | tinybird | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [tinybird-cli-guidelines](https://raw.githubusercontent.com/tinybirdco/tinybird-agent-skills/main/skills/tinybird-cli-guidelines/SKILL.md) | tinybird | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [tinybird-typescript-sdk-guidelines](https://raw.githubusercontent.com/tinybirdco/tinybird-agent-skills/main/skills/tinybird-typescript-sdk-guidelines/SKILL.md) | tinybird | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [tldr-prompt](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/tldr-prompt/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [transloadit-media-processing](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/transloadit-media-processing/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [two-factor-authentication-best-practices](https://raw.githubusercontent.com/better-auth/skills/main/better-auth/twoFactor/SKILL.md) | better-auth | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [typescript-mcp-server-generator](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/typescript-mcp-server-generator/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [typespec-api-operations](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/typespec-api-operations/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [typespec-create-agent](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/typespec-create-agent/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [typespec-create-api-plugin](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/typespec-create-api-plugin/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [ui-design-system](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/product-team/ui-design-system/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [update-avm-modules-in-bicep](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/update-avm-modules-in-bicep/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [update-implementation-plan](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/update-implementation-plan/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [update-llms](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/update-llms/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [update-markdown-file-index](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/update-markdown-file-index/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [update-oo-component-documentation](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/update-oo-component-documentation/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [update-specification](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/update-specification/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [upgrade-stripe](https://raw.githubusercontent.com/stripe/ai/main/skills/upgrade-stripe/SKILL.md) | stripe | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [ux-researcher-designer](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/product-team/ux-researcher-designer/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [vercel-react-best-practices](https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/react-best-practices/SKILL.md) | vercel | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [visionos-immersive-media-developer](https://raw.githubusercontent.com/tomkrikorian/visionOSAgents/main/skills/visionos-immersive-media-developer/SKILL.md) | visionos-agents | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [visionos-widgetkit-developer](https://raw.githubusercontent.com/tomkrikorian/visionOSAgents/main/skills/visionos-widgetkit-developer/SKILL.md) | visionos-agents | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [web-artifacts-builder](https://raw.githubusercontent.com/anthropics/skills/main/skills/web-artifacts-builder/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟡 maintained |  |
| [web-design-reviewer](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/web-design-reviewer/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [web-perf](https://raw.githubusercontent.com/cloudflare/skills/main/skills/web-perf/SKILL.md) | cloudflare | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [webapp-testing](https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟡 maintained |  |
| [what-context-needed](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/what-context-needed/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [winapp-cli](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/winapp-cli/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [winui3-migration-guide](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/winui3-migration-guide/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [wrangler](https://raw.githubusercontent.com/cloudflare/skills/main/skills/wrangler/SKILL.md) | cloudflare | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [write-coding-standards-from-file](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/write-coding-standards-from-file/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 70/100 | 🟢 active |  |
| [xlsx](https://raw.githubusercontent.com/anthropics/skills/main/skills/xlsx/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 70/100 | 🟡 maintained |  |
| [yara-rule-authoring](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/yara-authoring/skills/yara-rule-authoring/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | 70/100 | 🟡 maintained |  |
| [yeet](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/yeet/SKILL.md) | openai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ | 70/100 | 🟡 maintained |  |
| [zeroize-audit](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/zeroize-audit/skills/zeroize-audit/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 70/100 | 🟢 active |  |
| [aflpp](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/aflpp/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [agentic-eval](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/agentic-eval/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [agents-md](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/agents-md/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [arkit-visionos-developer](https://raw.githubusercontent.com/tomkrikorian/visionOSAgents/main/skills/arkit-visionos-developer/SKILL.md) | visionos-agents | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [artifacts-builder](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/artifacts-builder/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [atlassian-admin](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/project-management/atlassian-admin/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [atlassian-templates](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/project-management/atlassian-templates/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [audit-context-building](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/audit-context-building/skills/audit-context-building/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [aws-agentic-ai](https://raw.githubusercontent.com/zxkane/aws-skills/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/SKILL.md) | aws-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [aws-mcp-setup](https://raw.githubusercontent.com/zxkane/aws-skills/main/plugins/aws-common/skills/aws-mcp-setup/SKILL.md) | aws-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [azure-role-selector](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/azure-role-selector/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [azure-static-web-apps](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/azure-static-web-apps/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [best-practices](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/best-practices/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [blog-writing-guide](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/blog-writing-guide/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [brainstorming](https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md) | obra-superpowers | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [brand-guidelines](https://raw.githubusercontent.com/anthropics/skills/main/skills/brand-guidelines/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [brand-guidelines](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/brand-guidelines/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [browserstack](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/playwright-pro/skills/browserstack/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [c-level-advisor](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/c-level-advisor/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [canvas-design](https://raw.githubusercontent.com/anthropics/skills/main/skills/canvas-design/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [chrome-devtools](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/chrome-devtools/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [claude-settings-audit](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/claude-settings-audit/SKILL.md) | getsentry | Claude | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [code-simplifier](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/code-simplifier/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [code-transfer](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/code-operations-plugin/skills/code-transfer/SKILL.md) | claude-marketplace-code | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [commit](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/commit/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [constant-time-analysis](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/constant-time-analysis/skills/constant-time-analysis/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [conversation-analyzer](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/productivity-skills-plugin/skills/conversation-analyzer/SKILL.md) | claude-marketplace-productivity | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [copilot-sdk](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/copilot-sdk/SKILL.md) | github | Copilot | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [coverage](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/playwright-pro/skills/coverage/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [create-branch](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/create-branch/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [create-pr](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/create-pr/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [django-perf-review](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/django-perf-review/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [doc-coauthoring](https://raw.githubusercontent.com/anthropics/skills/main/skills/doc-coauthoring/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [dwarf-expert](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/dwarf-expert/skills/dwarf-expert/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [enhance-prompt](https://raw.githubusercontent.com/google-labs-code/stitch-skills/main/skills/enhance-prompt/SKILL.md) | google-labs-stitch | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [ensemble-solving](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/engineering-workflow-plugin/skills/ensemble-solving/SKILL.md) | claude-marketplace-engineering | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [entry-point-analyzer](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/entry-point-analyzer/skills/entry-point-analyzer/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [expo-api-routes](https://raw.githubusercontent.com/expo/skills/main/plugins/expo-app-design/skills/expo-api-routes/SKILL.md) | expo | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [expo-dev-client](https://raw.githubusercontent.com/expo/skills/main/plugins/expo-app-design/skills/expo-dev-client/SKILL.md) | expo | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [expo-tailwind-setup](https://raw.githubusercontent.com/expo/skills/main/plugins/expo-app-design/skills/expo-tailwind-setup/SKILL.md) | expo | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [extract](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/self-improving-agent/skills/extract/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [feature-planning](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/engineering-workflow-plugin/skills/feature-planning/SKILL.md) | claude-marketplace-engineering | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [firebase-apk-scanner](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/firebase-apk-scanner/skills/firebase-apk-scanner/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [fix](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/playwright-pro/skills/fix/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [frontend-design](https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [generate](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/playwright-pro/skills/generate/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [git-cleanup](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/git-cleanup/skills/git-cleanup/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [git-commit](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/git-commit/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [git-pushing](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/engineering-workflow-plugin/skills/git-pushing/SKILL.md) | claude-marketplace-engineering | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [image-manipulation-image-magick](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/image-manipulation-image-magick/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [init](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/playwright-pro/skills/init/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [insecure-defaults](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/insecure-defaults/skills/insecure-defaults/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [internal-comms](https://raw.githubusercontent.com/anthropics/skills/main/skills/internal-comms/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [ios-simulator-skill](https://raw.githubusercontent.com/conorluddy/ios-simulator-skill/main/ios-simulator-skill/SKILL.md) | ios-simulator-skill | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [ipsw](https://raw.githubusercontent.com/blacktop/ipsw-skill/main/skill/SKILL.md) | ipsw-skill | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [jules](https://raw.githubusercontent.com/sanjay3290/ai-skills/main/skills/jules/SKILL.md) | sanjay-ai-skills | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [learn-this](https://raw.githubusercontent.com/michalparkola/tapestry-skills-for-claude-code/main/learn-this/SKILL.md) | tapestry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [make-skill-template](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/make-skill-template/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [markdown-to-epub-converter](https://raw.githubusercontent.com/smerchek/claude-epub-skill/main/markdown-to-epub/SKILL.md) | epub-skill | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [marketing-skills](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [mcp-cli](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/mcp-cli/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [meeting-minutes](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/meeting-minutes/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [microsoft-code-reference](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/microsoft-code-reference/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [migrate](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/playwright-pro/skills/migrate/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [nuget-manager](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/nuget-manager/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [paywall-upgrade-cro](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/paywall-upgrade-cro/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [plantuml-ascii](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/plantuml-ascii/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [popup-cro](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/marketing-skill/popup-cro/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [pr-writer](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/pr-writer/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [prd](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/prd/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [promote](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/self-improving-agent/skills/promote/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [realitykit-visionos-developer](https://raw.githubusercontent.com/tomkrikorian/visionOSAgents/main/skills/realitykit-visionos-developer/SKILL.md) | visionos-agents | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [refactor](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/refactor/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [remember](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/self-improving-agent/skills/remember/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [remotion](https://raw.githubusercontent.com/google-labs-code/stitch-skills/main/skills/remotion/SKILL.md) | google-labs-stitch | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [report](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/playwright-pro/skills/report/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [review](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/playwright-pro/skills/review/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [review](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/self-improving-agent/skills/review/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [sarif-parsing](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/static-analysis/skills/sarif-parsing/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [scoutqa-test](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/scoutqa-test/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [scrum-sage](https://raw.githubusercontent.com/michalparkola/tapestry-skills-for-claude-code/main/scrum-sage/SKILL.md) | tapestry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [seatbelt-sandboxer](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/seatbelt-sandboxer/skills/seatbelt-sandboxer/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [semgrep-rule-creator](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/semgrep-rule-creator/skills/semgrep-rule-creator/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [semgrep-rule-variant-creator](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/semgrep-rule-variant-creator/skills/semgrep-rule-variant-creator/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [session-log](https://raw.githubusercontent.com/michalparkola/tapestry-skills-for-claude-code/main/session-log/SKILL.md) | tapestry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [shadcn-ui](https://raw.githubusercontent.com/google-labs-code/stitch-skills/main/skills/shadcn-ui/SKILL.md) | google-labs-stitch | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [shadergraph-editor](https://raw.githubusercontent.com/tomkrikorian/visionOSAgents/main/skills/shadergraph-editor/SKILL.md) | visionos-agents | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [sharp-edges](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/sharp-edges/skills/sharp-edges/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [skill-creator](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/skill-creator/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [skill-improver](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/skill-improver/skills/skill-improver/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [slack-gif-creator](https://raw.githubusercontent.com/anthropics/skills/main/skills/slack-gif-creator/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [slack-gif-creator](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/slack-gif-creator/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ | 60/100 | 🟡 maintained |  |
| [snowflake-semanticview](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/snowflake-semanticview/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [spatial-swiftui-developer](https://raw.githubusercontent.com/tomkrikorian/visionOSAgents/main/skills/spatial-swiftui-developer/SKILL.md) | visionos-agents | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [spec-to-code-compliance](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/spec-to-code-compliance/skills/spec-to-code-compliance/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [sred-work-summary](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/sred-work-summary/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [status](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/self-improving-agent/skills/status/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [stitch-loop](https://raw.githubusercontent.com/google-labs-code/stitch-skills/main/skills/stitch-loop/SKILL.md) | google-labs-stitch | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [stream-coding](https://raw.githubusercontent.com/frmoretto/stream-coding/main/skills/stream-coding/SKILL.md) | stream-coding | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [supply-chain-risk-auditor](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/supply-chain-risk-auditor/skills/supply-chain-risk-auditor/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [testing-handbook-generator](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/testing-handbook-generator/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ | 60/100 | 🟡 maintained |  |
| [testrail](https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/engineering-team/playwright-pro/skills/testrail/SKILL.md) | nginity | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [theme-factory](https://raw.githubusercontent.com/anthropics/skills/main/skills/theme-factory/SKILL.md) | anthropics | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [unblock-action](https://raw.githubusercontent.com/michalparkola/tapestry-skills-for-claude-code/main/unblock-action/SKILL.md) | tapestry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [usd-editor](https://raw.githubusercontent.com/tomkrikorian/visionOSAgents/main/skills/usd-editor/SKILL.md) | visionos-agents | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | 60/100 | 🟡 maintained |  |
| [use-dom](https://raw.githubusercontent.com/expo/skills/main/plugins/expo-app-design/skills/use-dom/SKILL.md) | expo | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [using-superpowers](https://raw.githubusercontent.com/obra/superpowers/main/skills/using-superpowers/SKILL.md) | obra-superpowers | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [variant-analysis](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/variant-analysis/skills/variant-analysis/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [vercel-composition-patterns](https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/composition-patterns/SKILL.md) | vercel | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [vercel-react-native-skills](https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/react-native-skills/SKILL.md) | vercel | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [vscode-ext-commands](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/vscode-ext-commands/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [vscode-ext-localization](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/vscode-ext-localization/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [web-design-guidelines](https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/web-design-guidelines/SKILL.md) | vercel | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [webapp-testing](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/webapp-testing/SKILL.md) | github | Copilot+Universal | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained | 🔄 → anthropics/webapp-testing |
| [workiq-copilot](https://raw.githubusercontent.com/github/awesome-copilot/main/skills/workiq-copilot/SKILL.md) | github | Copilot | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟡 maintained |  |
| [writing-plans](https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-plans/SKILL.md) | obra-superpowers | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [writing-skills](https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-skills/SKILL.md) | obra-superpowers | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 60/100 | 🟢 active |  |
| [address-sanitizer](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/address-sanitizer/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [algorand-vulnerability-scanner](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/building-secure-contracts/skills/algorand-vulnerability-scanner/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [algorithmic-art](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/algorithmic-art/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [api-testing](https://raw.githubusercontent.com/aiqualitylab/agent-skills/main/skills/api-testing/SKILL.md) | aiqualitylab | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [article-extractor](https://raw.githubusercontent.com/michalparkola/tapestry-skills-for-claude-code/main/article-extractor/SKILL.md) | tapestry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [ask-questions-if-underspecified](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/ask-questions-if-underspecified/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [ask-questions-if-underspecified](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/ask-questions-if-underspecified/skills/ask-questions-if-underspecified/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained | ⚠️ ~84% → skillcreatorai/ask-questions-if-underspecified |
| [atheris](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/atheris/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [audit-prep-assistant](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/building-secure-contracts/skills/audit-prep-assistant/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [backend-development](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/backend-development/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [brand-guidelines](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/brand-guidelines/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [brand-guidelines](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/brand-guidelines/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [cairo-vulnerability-scanner](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/building-secure-contracts/skills/cairo-vulnerability-scanner/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [canvas-design](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/canvas-design/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [cargo-fuzz](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/cargo-fuzz/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [changelog-generator](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/changelog-generator/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [claude-in-chrome-troubleshooting](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/claude-in-chrome-troubleshooting/skills/claude-in-chrome-troubleshooting/SKILL.md) | trailofbits | Claude | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [code-auditor](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/productivity-skills-plugin/skills/code-auditor/SKILL.md) | claude-marketplace-productivity | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [code-documentation](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/code-documentation/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [code-execution](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/code-operations-plugin/skills/code-execution/SKILL.md) | claude-marketplace-code | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [code-maturity-assessor](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/building-secure-contracts/skills/code-maturity-assessor/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [code-refactor](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/code-operations-plugin/skills/code-refactor/SKILL.md) | claude-marketplace-code | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [code-refactoring](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/code-refactoring/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [code-review](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/code-review/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [code-review](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/code-review/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [codebase-documenter](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/productivity-skills-plugin/skills/codebase-documenter/SKILL.md) | claude-marketplace-productivity | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [coding-standards-enforcer](https://raw.githubusercontent.com/tomkrikorian/visionOSAgents/main/skills/coding-standards-enforcer/SKILL.md) | visionos-agents | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [competitive-ads-extractor](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/competitive-ads-extractor/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [constant-time-testing](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/constant-time-testing/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [content-research-writer](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/content-research-writer/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [cosmos-vulnerability-scanner](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/building-secure-contracts/skills/cosmos-vulnerability-scanner/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [coverage-analysis](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/coverage-analysis/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [csv-data-summarizer](https://raw.githubusercontent.com/coffeefuelbump/csv-data-summarizer-claude-skill/main/SKILL.md) | csv-summarizer-skill | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [d3-viz](https://raw.githubusercontent.com/chrisvoncsefalvay/claude-d3js-skill/main/SKILL.md) | d3js-skill | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [database-design](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/database-design/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [design-md](https://raw.githubusercontent.com/google-labs-code/stitch-skills/main/skills/design-md/SKILL.md) | google-labs-stitch | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [developer-growth-analysis](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/developer-growth-analysis/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [differential-review](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/differential-review/skills/differential-review/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [dispatching-parallel-agents](https://raw.githubusercontent.com/obra/superpowers/main/skills/dispatching-parallel-agents/SKILL.md) | obra-superpowers | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [doc-coauthoring](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/doc-coauthoring/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained | 🔄 → anthropics/doc-coauthoring |
| [doc-coauthoring](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/doc-coauthoring/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained | 🔄 → anthropics/doc-coauthoring |
| [docx](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/docx/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [domain-name-brainstormer](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/domain-name-brainstormer/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [executing-plans](https://raw.githubusercontent.com/obra/superpowers/main/skills/executing-plans/SKILL.md) | obra-superpowers | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [expo-app-design](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/expo-app-design/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [expo-deployment](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/expo-deployment/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [family-history-planning](https://raw.githubusercontent.com/emaynard/claude-family-history-research-skill/main/SKILL.md) | family-history-skill | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [ffuf-web-fuzzing](https://raw.githubusercontent.com/jthack/ffuf_claude_skill/main/ffuf-skill/SKILL.md) | ffuf-skill | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [file-operations](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/code-operations-plugin/skills/file-operations/SKILL.md) | claude-marketplace-code | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [file-organizer](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/file-organizer/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [find-bugs](https://raw.githubusercontent.com/getsentry/skills/main/plugins/sentry-skills/skills/find-bugs/SKILL.md) | getsentry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [finishing-a-development-branch](https://raw.githubusercontent.com/obra/superpowers/main/skills/finishing-a-development-branch/SKILL.md) | obra-superpowers | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [frontend-design](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/frontend-design/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained | 🔄 → anthropics/frontend-design |
| [fuzzing-dictionary](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/fuzzing-dictionary/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [fuzzing-obstacles](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/fuzzing-obstacles/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [guidelines-advisor](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/building-secure-contracts/skills/guidelines-advisor/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [harness-writing](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/harness-writing/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [image-enhancer](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/image-enhancer/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [internal-comms](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/internal-comms/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [invoice-organizer](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/invoice-organizer/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [javascript-typescript](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/javascript-typescript/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [jira-issues](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/jira-issues/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [job-application](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/job-application/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [lead-research-assistant](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/lead-research-assistant/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [libafl](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/libafl/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [libfuzzer](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/libfuzzer/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [llm-application-dev](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/llm-application-dev/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [mcp-builder](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/mcp-builder/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained | 🔄 → anthropics/mcp-builder |
| [meeting-insights-analyzer](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/meeting-insights-analyzer/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [move-code-quality](https://raw.githubusercontent.com/1NickPappas/move-code-quality-skill/main/SKILL.md) | move-quality-skill | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [ossfuzz](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/ossfuzz/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [pdf](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/pdf/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [pict-test-designer](https://raw.githubusercontent.com/omkamal/pypict-claude-skill/main/SKILL.md) | pypict-skill | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [playwright-skill](https://raw.githubusercontent.com/lackeyjb/playwright-skill/main/skills/playwright-skill/SKILL.md) | playwright-skill | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [pptx](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/pptx/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [project-bootstrapper](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/productivity-skills-plugin/skills/project-bootstrapper/SKILL.md) | claude-marketplace-productivity | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [python-development](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/python-development/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [qa-regression](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/qa-regression/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [raffle-winner-picker](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/raffle-winner-picker/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [react-best-practices](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/react-best-practices/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [receiving-code-review](https://raw.githubusercontent.com/obra/superpowers/main/skills/receiving-code-review/SKILL.md) | obra-superpowers | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [requesting-code-review](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/SKILL.md) | obra-superpowers | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [review-implementing](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/engineering-workflow-plugin/skills/review-implementing/SKILL.md) | claude-marketplace-engineering | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [ruzzy](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/ruzzy/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [secure-workflow-guide](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/building-secure-contracts/skills/secure-workflow-guide/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [Selenium Self-Healing](https://raw.githubusercontent.com/aiqualitylab/agent-skills/main/skills/selenium-selfhealing/SKILL.md) | aiqualitylab | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [ship-learn-next](https://raw.githubusercontent.com/michalparkola/tapestry-skills-for-claude-code/main/ship-learn-next/SKILL.md) | tapestry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [skill-creator](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/skill-creator/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [solana-vulnerability-scanner](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/building-secure-contracts/skills/solana-vulnerability-scanner/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [subagent-driven-development](https://raw.githubusercontent.com/obra/superpowers/main/skills/subagent-driven-development/SKILL.md) | obra-superpowers | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [substrate-vulnerability-scanner](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/building-secure-contracts/skills/substrate-vulnerability-scanner/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [systematic-debugging](https://raw.githubusercontent.com/obra/superpowers/main/skills/systematic-debugging/SKILL.md) | obra-superpowers | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [test-driven-development](https://raw.githubusercontent.com/obra/superpowers/main/skills/test-driven-development/SKILL.md) | obra-superpowers | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [test-fixing](https://raw.githubusercontent.com/mhattingpete/claude-skills-marketplace/main/engineering-workflow-plugin/skills/test-fixing/SKILL.md) | claude-marketplace-engineering | Claude+Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [theme-factory](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/theme-factory/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained | 🔄 → anthropics/theme-factory |
| [tkr-skill-writer](https://raw.githubusercontent.com/tomkrikorian/visionOSAgents/main/skills/tkr-skill-writer/SKILL.md) | visionos-agents | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [token-integration-analyzer](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/building-secure-contracts/skills/token-integration-analyzer/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [ton-vulnerability-scanner](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/building-secure-contracts/skills/ton-vulnerability-scanner/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [upgrading-expo](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/upgrading-expo/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [using-git-worktrees](https://raw.githubusercontent.com/obra/superpowers/main/skills/using-git-worktrees/SKILL.md) | obra-superpowers | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [vercel-deploy](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/vercel-deploy/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [verification-before-completion](https://raw.githubusercontent.com/obra/superpowers/main/skills/verification-before-completion/SKILL.md) | obra-superpowers | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [video-downloader](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/video-downloader/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [web-design-guidelines](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/web-design-guidelines/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [webapp-testing](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/webapp-testing/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained | 🔄 → anthropics/webapp-testing |
| [wycheproof](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/testing-handbook-skills/skills/wycheproof/SKILL.md) | trailofbits | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [xlsx](https://raw.githubusercontent.com/skillcreatorai/Ai-Agent-Skills/main/skills/xlsx/SKILL.md) | skillcreatorai | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [youtube-transcript](https://raw.githubusercontent.com/michalparkola/tapestry-skills-for-claude-code/main/youtube-transcript/SKILL.md) | tapestry | Universal | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 50/100 | 🟡 maintained |  |
| [notebooklm](https://raw.githubusercontent.com/PleasePrompto/notebooklm-skill/master/SKILL.md) | notebooklm-skill | Universal | ⬜ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | 35/100 | ⚪ unknown |  |

<!-- AUTO-GENERATED SKILLS TABLE END -->

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
