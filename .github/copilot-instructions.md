# Agent Skills Directory - AI Agent Instructions

## Project Overview

This repository aggregates agent skills from **41 provider repositories** (Anthropic, OpenAI, GitHub, Vercel, HuggingFace, Stripe, Cloudflare, Supabase, and 33+ community repos) into a unified JSON catalog consumed by MCP servers and AI agents. A GitHub Action runs daily at 06:00 UTC to fetch the latest skills, generating versioned releases with `YYYY.MM.DD` format.

**Current stats:** 250+ skills, 41 providers, 150K+ combined GitHub stars

**Key consumers:** [MCP Mother Skills](https://github.com/dmgrok/mcp_mother_skills) server.

## Architecture

### Core Components

1. **`scripts/aggregate.py`** - Main aggregation script (425 lines)
   - Fetches skills from GitHub API using tree endpoints
   - Parses `SKILL.md` files with YAML frontmatter
   - Generates 4 output formats: `catalog.json`, `catalog.min.json`, `catalog.toon`, `catalog.min.toon`
   - Auto-updates `CHANGELOG.md` with version metadata
   - Uses `GITHUB_TOKEN` env var to avoid rate limits

2. **Provider System** - Extensible provider configuration (lines 35-207 in aggregate.py)
   ```python
   PROVIDERS = {
       "provider-id": {
           "name": "Display Name",
           "repo": "https://github.com/org/repo",
           "api_tree_url": "https://api.github.com/repos/.../git/trees/main?recursive=1",
           "raw_base": "https://raw.githubusercontent.com/.../main",
           "skills_path_prefix": "skills/",  # Can be "" for root-level SKILL.md
       }
   }
   ```
   - Add new providers by extending this dict - no other code changes needed
   - Supports root-level `SKILL.md` files (single-skill repos) with `skills_path_prefix: ""`
   - Some repos use `master` branch instead of `main` - adjust URLs accordingly
   - Provider stats include `stars` and `description` fetched from GitHub API

3. **Category System** - Keyword-based auto-categorization (lines 67-74)
   - Maps skills to categories: `documents`, `development`, `creative`, `enterprise`, `integrations`, `data`, `other`
   - Based on keyword matching in name/description
   - To add categories: extend `CATEGORY_KEYWORDS` dict

4. **Quality Scoring System** - Composite quality metrics (0-100 points)
   - **Maintenance score (50pts max)**: active=50, maintained=40, stale=20, abandoned=5
     - active: updated < 30 days ago
     - maintained: updated < 6 months ago
     - stale: updated < 1 year ago
     - abandoned: updated > 1 year ago
   - **Documentation completeness (30pts max)**: scripts=10, references=10, assets=10
   - **Provider trust (20pts max)**: trusted providers=20, community=10
     - Trusted: anthropics, openai, github, vercel, stripe, cloudflare, supabase, etc.
   - Used for informed discoverability - helping users choose between similar skills
   - Displayed in web UI as colored badges and in CLI with ⭐ emoji

5. **Schema** - `schema/catalog-schema.json` defines the output contract
   - JSON Schema draft-07
   - Validates version format: `^\d{4}\.\d{2}\.\d{2}$`
   - Each skill has: `source` (repo metadata), `has_scripts`, `has_references`, `has_assets` flags
   - Includes `quality_score` (0-100), `maintenance_status`, `days_since_update`

6. **Static Docs Site** - `docs/` directory (HTML/JS/CSS)
   - Pure client-side catalog browser
   - Fetches catalog via jsdelivr CDN
   - Supports URL query params: `?provider=`, `?category=`, `?search=`, `?tags=`, `?id=`
   - Shows quality scores, maintenance badges, and similar skills with score comparison

## Critical Workflows

### Running Aggregation Locally
```bash
# Required: PyYAML, optional: toon_format (for TOON encoding), python-dotenv (for .env support), pytest
python -m venv .venv && . .venv/bin/activate
pip install pyyaml toon_format python-dotenv pytest

# Optional: Create .env file with GitHub token to avoid rate limits
echo "GITHUB_TOKEN=your_token_here" > .env

# Run full aggregation (fetches all providers)
python scripts/aggregate.py

# Run incremental aggregation (only fetches changed providers - saves API requests)
python scripts/aggregate.py --incremental

# Outputs: catalog.json, catalog.min.json, catalog.toon, catalog.min.toon, 
#          CHANGELOG.md updated, aggregation_state.json (for incremental mode)
```

### Incremental Mode (New!)
The aggregator supports an **incremental mode** that dramatically reduces GitHub API requests:
- Uses `aggregation_state.json` to track last run timestamp and provider commit SHAs
- Checks each provider's HEAD commit to detect changes
- Only fetches/processes providers with new commits
- **Savings**: With 41 providers, typically saves 70-80+ GitHub API requests per run
- **Daily GH Actions runs**: Use `--incremental` by default
- **Manual full refresh**: Available via workflow_dispatch with `full_refresh: true`

State file structure:
```json
{
  "last_run": "2026-01-31T12:00:00+00:00",
  "provider_commits": {
    "anthropics": "abc123...",
    "openai": "def456..."
  },
  "skills_count": 250,
  "version": "2026.01.31"
}
```

### Testing
```bash
pytest  # Runs tests/test_aggregate.py
```

### TOON Format Fallback Strategy
The script tries Python `toon_format.encode()` first, then falls back to `npx @toon-format/cli` if unavailable or fails. Both `catalog.toon` (from full JSON) and `catalog.min.toon` (from minified JSON) are generated.

### Changelog Generation
`update_changelog()` function (starting around line 335) automatically:
- Inserts new version entry after `## [Unreleased]` section
- Includes total skills, provider breakdown, categories
- Preserves existing changelog history

## Project-Specific Conventions

### Skill Metadata Enrichment
- **`last_updated_at`**: Fetched via GitHub API commits endpoint for each `SKILL.md` file (see `fetch_last_updated_at()`)
- **`has_scripts/has_references/has_assets`**: Detected by checking tree paths for `scripts/`, `references/`, `assets/` directories
- **`tags`**: Auto-extracted from name/description using keyword matching (max 10 tags)
- **`quality_score`**: Calculated via `calculate_quality_score()` combining maintenance (50pts), documentation (30pts), and provider trust (20pts)
- **`maintenance_status`**: Derived from `days_since_update` via `calculate_maintenance_status()`

### Error Handling
- Network requests use retry logic with exponential backoff (3 retries, see `fetch_url()`)
- Failed skills are logged to stderr but don't stop aggregation
- GitHub API failures gracefully degrade (missing `last_updated_at` is allowed)

### GitHub Actions Integration
- **Workflow**: `.github/workflows/update-catalog.yml`
- **Incremental mode**: Daily runs use `--incremental` to save API requests
- **Full refresh option**: workflow_dispatch supports `full_refresh: true` for manual full runs
- **Commit strategy**: Only commits if `catalog.json` changes
- **Release strategy**: Creates GitHub release with `vYYYY.MM.DD` tag on changes
- **Files committed**: `catalog.json`, `catalog.min.json`, `catalog.toon`, `catalog.min.toon`, `CHANGELOG.md`, `aggregation_state.json`
- **Git user**: `github-actions[bot]` (NOT dmgrok) for automated commits

### CDN Delivery
Primary distribution via jsdelivr CDN with two patterns:
- Latest: `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.json`
- Pinned: `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@v2026.01.26/catalog.json`

## Common Development Tasks

### Adding a New Provider
1. Edit `PROVIDERS` dict in `scripts/aggregate.py`
2. Ensure repo follows one of these structures:
   - Multi-skill repo: `skills/*/SKILL.md` with YAML frontmatter
   - Single-skill repo: `SKILL.md` at root (use `skills_path_prefix: ""`)
3. Check the branch name (main vs master) and adjust URLs accordingly
4. Run `python scripts/aggregate.py` to test
5. Verify in `catalog.json` under `providers` object
6. Update README.md provider tables if adding a significant provider

### Modifying Categorization Logic
Edit `CATEGORY_KEYWORDS` dict or `categorize_skill()` function (line 195).

### Updating Schema
1. Modify `schema/catalog-schema.json`
2. Update README.md examples if contract changes
3. Consider backward compatibility for existing consumers

### Debugging Aggregation Issues
- Check stderr output for warnings about failed fetches or parse errors
- Verify `GITHUB_TOKEN` is set to avoid rate limits (60 req/hr → 5000 req/hr)
- Use `python scripts/aggregate.py` locally with verbose output before pushing

## Anti-Patterns to Avoid

- ❌ Don't hardcode skill data - always fetch from source repos
- ❌ Don't skip CHANGELOG updates - `update_changelog()` must be called in `main()`
- ❌ Don't commit without testing schema validation
- ❌ Don't modify GitHub Actions workflow without updating commit file list (currently: catalog.json, catalog.min.json, catalog.toon, catalog.min.toon, CHANGELOG.md)
- ❌ Don't use `dmgrok` as git user in automated workflows - use `github-actions[bot]` instead
- ❌ **Don't add new features without updating the docs site** - always update `docs/index.html`, `docs/app.js`, and `docs/style.css` when adding user-facing features

## Adding New Features Checklist

When adding a new feature that users can interact with (new JSON files, new data types, new endpoints):

1. **Schema**: Create/update schema in `schema/` directory
2. **Docs Site**: Update the static docs site in `docs/`:
   - `index.html`: Add new tabs/sections in the UI
   - `app.js`: Add fetch logic, rendering functions, and event handlers
   - `style.css`: Add styles for new components
3. **README.md**: Document the feature with usage examples
4. **Copilot Instructions**: Update this file to document the new feature
5. **GitHub Actions**: Update workflow if new files need to be committed

## Key Files Reference

- `scripts/aggregate.py`: Core aggregation logic (~1200 lines, 41 providers, incremental mode support)
- `scripts/analyze_repo.py`: Utility to evaluate potential new provider repos
- `cli/skills.py`: CLI tool for installing/managing skills (npm-like)
- `cli/__init__.py`: CLI package init
- `pyproject.toml`: Python package configuration for CLI distribution
- `schema/catalog-schema.json`: Output contract with stars/description fields
- `schema/bundles-schema.json`: Curated skill bundles schema
- `schema/skill-manifest-schema.json`: skill.json manifest schema (like package.json)
- `.github/workflows/update-catalog.yml`: Automation pipeline with incremental mode
- `docs/app.js`: Static site catalog and bundles display logic (shows stars)
- `docs/index.html`: Static site HTML with tabs for Skills, Bundles, CLI, and Help
- `docs/style.css`: Static site styling (star badges, CLI styles, etc.)
- `tests/test_aggregate.py`: Unit tests for parsing and encoding
- `CHANGELOG.md`: Auto-generated version history
- `README.md`: User-facing documentation with provider tables
- `bundles.json`: Curated skill bundles for common use cases
- `catalog.json`: Aggregated skills catalog (auto-generated)
- `aggregation_state.json`: Incremental mode state file (tracks commit SHAs)

## CLI Tool (`cli/skills.py`)

The CLI provides npm-like package management for skills:

### Commands
- `skillsdir search <query>` - Search skills by name/description/tags
- `skillsdir info <skill-id>` - Show detailed skill information
- `skillsdir suggest [path]` - AI-powered skill recommendations based on project README and structure
- `skillsdir install <skill-id>[@version]` - Install a skill to `~/.skills/installed/`
- `skillsdir uninstall <skill-id>` - Remove an installed skill
- `skillsdir list [--json]` - List installed skills
- `skillsdir init` - Create a new skill.json manifest interactively
- `skillsdir update` - Check for and apply updates
- `skillsdir config list|get|set` - Manage CLI configuration
- `skillsdir cache clean|list` - Manage cache
- `skillsdir run <skill-id>` - Preview/run a skill (placeholder for runtime integration)

### Suggest Command (New!)
The `suggest` command uses AI to analyze projects and recommend relevant skills:
- **Input**: Project README + file structure analysis (languages, frameworks, file types)
- **Processing**: Uses Perplexity MCP's reasoning capability to match project needs with catalog skills
- **Output**: 5-10 ranked recommendations with confidence levels and quality scores
- **Fallback**: Heuristic-based matching when LLM is unavailable (keyword matching in README + tech stack)
- **Usage**: `skillsdir suggest [path] [--verbose]`

Implementation details:
- `find_readme()` - Locates README.md in project
- `cmd_suggest()` - Main command handler (uses MCP if available)
- `generate_heuristic_suggestions()` - Fallback for when LLM unavailable (scores skills by README keywords, language/framework matching, quality, and maintenance status)

### Local Registry Structure
```
~/.skills/
├── config.json          # CLI configuration
├── installed/           # Installed skills
│   ├── provider/
│   │   └── skill-name/
│   │       ├── skill.json   # Manifest
│   │       └── SKILL.md     # Instructions
└── cache/               # Catalog cache
```

### skill.json Manifest Schema
Defines skill metadata, dependencies, and capabilities (like package.json for skills):
- `name`, `version`, `description` - Basic info
- `dependencies` - Other skills required
- `runtime` - Target framework (mcp, langchain, crewai, etc.)
- `capabilities` - Required permissions (web-browsing, file-system, etc.)
- `inputs`/`outputs` - Parameter definitions

See `schema/skill-manifest-schema.json` for full specification.
