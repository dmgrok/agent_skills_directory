# Agent Skills Directory

A centralized, automatically-updated catalog of [Agent Skills](https://agentskills.io) from multiple providers.

> **🔄 Updated Daily** — A GitHub Action runs every day at 06:00 UTC to fetch the latest skills from all providers and update the catalog. You can always target `@main` for the latest or pin to a specific version.

## What is this?

This repository aggregates skills from various providers into a single, standardized JSON catalog that can be consumed by MCP servers, AI agents, and developer tools.

**Used by:** [MCP Mother Skills](https://github.com/dmgrok/mcp_mother_skills) — An MCP server that exposes these skills to AI agents.

**Providers:**
- [Anthropic](https://github.com/anthropics/skills) - Official skills from Anthropic
- [OpenAI](https://github.com/openai/skills) - Skills for OpenAI Codex
- [GitHub](https://github.com/github/awesome-copilot) - Skills from GitHub Awesome Copilot
- [Vercel](https://github.com/vercel-labs/agent-skills) - Skills from Vercel Labs

## Usage

### Quick Start

```python
import requests

# Fetch the latest catalog
catalog = requests.get(
    "https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.json"
).json()

# List all skills
for skill in catalog["skills"]:
    print(f"{skill['id']}: {skill['description']}")

# Filter by category
dev_skills = [s for s in catalog["skills"] if s["category"] == "development"]

# Get a specific skill's full content
skill = catalog["skills"][0]
skill_md = requests.get(skill["source"]["skill_md_url"]).text
```

### URLs

| Use Case | URL |
|----------|-----|
| **Latest (CDN)** | `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.json` |
| **Latest (Raw)** | `https://raw.githubusercontent.com/dmgrok/agent_skills_directory/main/catalog.json` |
| **Specific Version** | `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@v2026.01.08/catalog.json` |
| **Minified JSON** | `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.min.json` |
| **TOON** | `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.toon` |
| **TOON (minified JSON source)** | `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.min.toon` |

### MCP Server Integration

### Browser (docs site) URL filters

The static browser supports query-string filters so you can share/bookmark filtered views:

- `?provider=anthropics`
- `?category=development`
- `?search=notion` (or `?q=...`)
- `?tags=git,api`
- `?id=anthropics/pdf` (opens modal directly)

Examples:

- `https://dmgrok.github.io/agent_skills_directory/?category=documents`
- `https://dmgrok.github.io/agent_skills_directory/?provider=openai&search=notion`
```python
from mcp.server import Server
import aiohttp

CATALOG_URL = "https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.json"

class SkillsServer(Server):
    def __init__(self):
        super().__init__("skills-directory")
        self.catalog = None
    
    async def load_catalog(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(CATALOG_URL) as resp:
                self.catalog = await resp.json()
    
    @server.list_tools()
    async def list_tools(self):
        return [
            Tool(
                name="search_skills",
                description="Search the agent skills catalog",
                inputSchema={...}
            )
        ]
    
    @server.call_tool()
    async def call_tool(self, name: str, arguments: dict):
        if name == "search_skills":
            query = arguments.get("query", "").lower()
            matches = [
                s for s in self.catalog["skills"]
                if query in s["name"] or query in s["description"].lower()
            ]
            return matches
```

## Catalog Format

```json
{
  "version": "2026.01.08",
  "generated_at": "2026-01-08T06:00:00Z",
  "total_skills": 47,
  "providers": {
    "anthropics": { "name": "Anthropic", "repo": "...", "skills_count": 35 },
    "openai": { "name": "OpenAI", "repo": "...", "skills_count": 12 }
  },
  "categories": ["development", "documents", "creative", "enterprise", ...],
  "skills": [
    {
      "id": "anthropics/pdf-processing",
      "name": "pdf-processing",
      "description": "Extract text and tables from PDF files...",
      "provider": "anthropics",
      "category": "documents",
      "license": "Apache-2.0",
            "last_updated_at": "2026-01-07T12:00:00Z",
      "source": {
        "repo": "https://github.com/anthropics/skills",
        "path": "skills/pdf",
        "skill_md_url": "https://raw.githubusercontent.com/..."
      },
      "has_scripts": true,
      "has_references": false,
      "has_assets": true,
      "tags": ["pdf", "documents", "extraction"]
    }
  ]
}
```

## Skill Bundles

In addition to the full catalog, we maintain curated **skill bundles** — collections of skills grouped by common use cases. Bundles make it easy to discover and install related skills together.

### Quick Start with Bundles

```python
import requests

# Fetch the bundles catalog
bundles = requests.get(
    "https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/bundles.json"
).json()

# List all bundles
for bundle in bundles["bundles"]:
    print(f"{bundle['icon']} {bundle['name']}: {bundle['description']}")
    print(f"   Skills: {', '.join(bundle['skills'])}")

# Find bundles by category
frontend_bundles = [b for b in bundles["bundles"] if b["category"] == "frontend"]

# Get skills from a specific bundle
react_bundle = next(b for b in bundles["bundles"] if b["id"] == "frontend-react")
skill_ids = react_bundle["skills"]  # ["skillcreatorai/react-best-practices", ...]
```

### Bundle URLs

| Use Case | URL |
|----------|-----|
| **Latest (CDN)** | `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/bundles.json` |
| **Latest (Raw)** | `https://raw.githubusercontent.com/dmgrok/agent_skills_directory/main/bundles.json` |
| **Specific Version** | `https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@v2026.01.08/bundles.json` |

### Bundle Format

```json
{
  "version": "1.0.0",
  "generated_at": "2026-01-23T00:00:00Z",
  "total_bundles": 18,
  "bundles": [
    {
      "id": "frontend-react",
      "name": "React Frontend",
      "description": "Modern React development with testing and best practices",
      "icon": "⚛️",
      "skills": [
        "skillcreatorai/react-best-practices",
        "vercel/vercel-react-best-practices",
        "anthropics/frontend-design",
        "skillcreatorai/webapp-testing"
      ],
      "use_cases": ["Building React SPAs", "Component libraries", "Dashboard UIs"],
      "tags": ["frontend", "web", "react"],
      "category": "frontend"
    }
  ]
}
```

### Using Bundles with MCP

```python
import requests

# CDN URLs
CATALOG_URL = "https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/catalog.json"
BUNDLES_URL = "https://cdn.jsdelivr.net/gh/dmgrok/agent_skills_directory@main/bundles.json"

# Fetch both catalog and bundles
catalog = requests.get(CATALOG_URL).json()
bundles = requests.get(BUNDLES_URL).json()

# Get skills for a bundle
def get_bundle_skills(bundle_id: str):
    bundle = next((b for b in bundles["bundles"] if b["id"] == bundle_id), None)
    if not bundle:
        return []
    
    # Map skill IDs to full skill objects
    skills_map = {s["id"]: s for s in catalog["skills"]}
    return [skills_map[sid] for sid in bundle["skills"] if sid in skills_map]

# Example: Get all skills for React development
react_skills = get_bundle_skills("frontend-react")
```

## Development

- Python dependencies: PyYAML, toon_format (TOON encoder, optional), pytest.
- Virtual environment (recommended): `python -m venv .venv && . .venv/bin/activate`
- Install deps: `python -m pip install pyyaml toon_format pytest`
- Run tests: `pytest`

## Update Schedule

The catalog is automatically updated daily at 06:00 UTC via GitHub Actions.

- Each update creates a new release with version `vYYYY.MM.DD`
- Changes are only committed if new skills are detected
- Historical versions are preserved in GitHub Releases

## Adding a Provider

To add a new skills provider, edit `scripts/aggregate.py`:

```python
PROVIDERS = {
    # ... existing providers
    "your-org": {
        "name": "Your Organization",
        "repo": "https://github.com/your-org/skills",
        "api_tree_url": "https://api.github.com/repos/your-org/skills/git/trees/main?recursive=1",
        "raw_base": "https://raw.githubusercontent.com/your-org/skills/main",
        "skills_path_prefix": "skills/",
    },
}
```

## Local Development

```bash
# Clone the repository
git clone https://github.com/dmgrok/agent_skills_directory.git
cd agent_skills_directory

# Install dependencies
pip install pyyaml

# Run aggregation
python scripts/aggregate.py

# Outputs: catalog.json, catalog.min.json
```

## Schema

The catalog and bundles follow JSON Schemas:
- **Catalog**: [schema/catalog-schema.json](schema/catalog-schema.json)
- **Bundles**: [schema/bundles-schema.json](schema/bundles-schema.json)

Validate your files:
```bash
pip install jsonschema
python -c "
import json
from jsonschema import validate

# Validate catalog
catalog_schema = json.load(open('schema/catalog-schema.json'))
catalog = json.load(open('catalog.json'))
validate(catalog, catalog_schema)
print('✓ Catalog valid')

# Validate bundles
bundles_schema = json.load(open('schema/bundles-schema.json'))
bundles = json.load(open('bundles.json'))
validate(bundles, bundles_schema)
print('✓ Bundles valid')
"
```

## License

This aggregation tool is MIT licensed. Individual skills retain their original licenses as specified in their respective repositories.

## Related

- [MCP Mother Skills](https://github.com/dmgrok/mcp_mother_skills) - MCP server that consumes this catalog
- [Agent Skills Specification](https://agentskills.io/specification)
- [Anthropic Skills](https://github.com/anthropics/skills)
- [OpenAI Skills](https://github.com/openai/skills)
- [GitHub Awesome Copilot](https://github.com/github/awesome-copilot)
- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)
- [Model Context Protocol](https://modelcontextprotocol.io)
