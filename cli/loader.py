#!/usr/bin/env python3
"""
Universal Skill Loader

Provides a unified interface for loading and executing skills across
different AI agent runtimes (MCP, LangChain, CrewAI, etc).

Usage:
    from cli.loader import SkillLoader, load_skill
    
    # Load a skill
    skill = load_skill("anthropic/pdf")
    
    # Get skill instructions
    instructions = skill.get_instructions()
    
    # Get skill metadata
    metadata = skill.get_metadata()
    
    # Export for specific runtime
    mcp_config = skill.to_mcp()
    langchain_tool = skill.to_langchain()
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field

# Try to import yaml, fall back to simple parsing
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

__all__ = ["SkillLoader", "Skill", "load_skill", "load_skills_from_dir"]


@dataclass
class SkillInput:
    """Skill input parameter definition."""
    name: str
    type: str = "string"
    description: str = ""
    required: bool = False
    default: Any = None


@dataclass
class SkillOutput:
    """Skill output definition."""
    name: str
    type: str = "string"
    description: str = ""


@dataclass
class Skill:
    """
    Universal skill representation.
    
    Can be loaded from SKILL.md, skill.json, or both.
    Provides methods to export to different runtime formats.
    """
    id: str
    name: str
    version: str = "0.0.0"
    description: str = ""
    instructions: str = ""
    author: str = ""
    license: str = ""
    runtime: str = "universal"
    keywords: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    dependencies: Dict[str, str] = field(default_factory=dict)
    inputs: List[SkillInput] = field(default_factory=list)
    outputs: List[SkillOutput] = field(default_factory=list)
    path: Optional[Path] = None
    raw_manifest: Dict[str, Any] = field(default_factory=dict)
    
    def get_instructions(self) -> str:
        """Get the skill instructions (from SKILL.md)."""
        return self.instructions
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get skill metadata as a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "license": self.license,
            "runtime": self.runtime,
            "keywords": self.keywords,
            "capabilities": self.capabilities,
            "dependencies": self.dependencies,
            "inputs": [vars(i) for i in self.inputs],
            "outputs": [vars(o) for o in self.outputs],
        }
    
    def to_mcp(self) -> Dict[str, Any]:
        """
        Export skill as MCP (Model Context Protocol) resource.
        
        Returns a dict that can be used with MCP servers.
        """
        return {
            "uri": f"skill://{self.id}",
            "name": self.name,
            "description": self.description,
            "mimeType": "text/markdown",
            "content": self.instructions,
            "metadata": {
                "version": self.version,
                "capabilities": self.capabilities,
            }
        }
    
    def to_langchain_prompt(self) -> str:
        """
        Export skill as a LangChain prompt template.
        
        Returns the skill instructions formatted for LangChain.
        """
        # Format inputs as template variables
        template = self.instructions
        for inp in self.inputs:
            # Replace {input_name} with LangChain variable syntax
            template = template.replace(f"{{{inp.name}}}", f"{{{{{inp.name}}}}}")
        
        return template
    
    def to_langchain_tool(self) -> Dict[str, Any]:
        """
        Export skill as a LangChain tool definition.
        
        Returns a dict that can be used to create a LangChain Tool.
        """
        return {
            "name": self.name.replace(" ", "_").lower(),
            "description": self.description,
            "args_schema": {
                "type": "object",
                "properties": {
                    inp.name: {
                        "type": inp.type,
                        "description": inp.description,
                    }
                    for inp in self.inputs
                },
                "required": [inp.name for inp in self.inputs if inp.required],
            },
            "instructions": self.instructions,
        }
    
    def to_crewai_agent(self) -> Dict[str, Any]:
        """
        Export skill as a CrewAI agent configuration.
        
        Returns a dict that can be used to configure a CrewAI agent.
        """
        return {
            "role": self.name,
            "goal": self.description,
            "backstory": self.instructions,
            "tools": [],  # Tools would be loaded separately
            "allow_delegation": "delegation" in self.capabilities,
            "verbose": True,
        }
    
    def to_autogen_agent(self) -> Dict[str, Any]:
        """
        Export skill as an AutoGen agent configuration.
        """
        return {
            "name": self.name.replace(" ", "_"),
            "system_message": self.instructions,
            "description": self.description,
        }
    
    def to_openai_assistant(self) -> Dict[str, Any]:
        """
        Export skill as OpenAI Assistant configuration.
        """
        tools = []
        if "code-interpreter" in self.capabilities:
            tools.append({"type": "code_interpreter"})
        if "web-browsing" in self.capabilities:
            tools.append({"type": "retrieval"})
        
        return {
            "name": self.name,
            "description": self.description,
            "instructions": self.instructions,
            "model": "gpt-4-turbo-preview",
            "tools": tools,
            "metadata": {
                "skill_id": self.id,
                "version": self.version,
            }
        }
    
    def to_anthropic_tools(self) -> List[Dict[str, Any]]:
        """
        Export skill inputs as Anthropic tool definitions.
        """
        if not self.inputs:
            return []
        
        return [{
            "name": f"{self.name.replace(' ', '_').lower()}_execute",
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": {
                    inp.name: {
                        "type": inp.type,
                        "description": inp.description,
                    }
                    for inp in self.inputs
                },
                "required": [inp.name for inp in self.inputs if inp.required],
            }
        }]
    
    def to_system_prompt(self) -> str:
        """
        Export skill as a system prompt for any LLM.
        
        This is the most universal format, usable with any chat model.
        """
        parts = [f"# {self.name}", ""]
        
        if self.description:
            parts.append(self.description)
            parts.append("")
        
        if self.instructions:
            parts.append("## Instructions")
            parts.append("")
            parts.append(self.instructions)
        
        if self.inputs:
            parts.append("")
            parts.append("## Expected Inputs")
            parts.append("")
            for inp in self.inputs:
                required = " (required)" if inp.required else ""
                parts.append(f"- **{inp.name}** ({inp.type}){required}: {inp.description}")
        
        if self.outputs:
            parts.append("")
            parts.append("## Expected Outputs")
            parts.append("")
            for out in self.outputs:
                parts.append(f"- **{out.name}** ({out.type}): {out.description}")
        
        return "\n".join(parts)


class SkillLoader:
    """
    Loads skills from various sources.
    
    Supports:
    - Local directories (with skill.json and/or SKILL.md)
    - Remote URLs (GitHub raw content)
    - Skill catalog entries
    """
    
    @staticmethod
    def from_directory(path: Path) -> Skill:
        """Load a skill from a local directory."""
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Skill directory not found: {path}")
        
        manifest = {}
        instructions = ""
        
        # Load skill.json if exists
        manifest_path = path / "skill.json"
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text())
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid skill.json: {e}")
        
        # Load SKILL.md if exists
        skill_md_path = path / "SKILL.md"
        if skill_md_path.exists():
            content = skill_md_path.read_text()
            instructions, frontmatter = SkillLoader._parse_skill_md(content)
            
            # Merge frontmatter into manifest (frontmatter takes precedence)
            manifest = {**manifest, **frontmatter}
        
        if not manifest and not instructions:
            raise ValueError(f"No skill.json or SKILL.md found in {path}")
        
        # Build skill ID from path or manifest
        skill_id = manifest.get("id") or f"local/{path.name}"
        
        # Parse inputs
        inputs = []
        for inp_data in manifest.get("inputs", []):
            inputs.append(SkillInput(
                name=inp_data.get("name", ""),
                type=inp_data.get("type", "string"),
                description=inp_data.get("description", ""),
                required=inp_data.get("required", False),
                default=inp_data.get("default"),
            ))
        
        # Parse outputs
        outputs = []
        for out_data in manifest.get("outputs", []):
            outputs.append(SkillOutput(
                name=out_data.get("name", ""),
                type=out_data.get("type", "string"),
                description=out_data.get("description", ""),
            ))
        
        return Skill(
            id=skill_id,
            name=manifest.get("name", path.name),
            version=manifest.get("version", "0.0.0"),
            description=manifest.get("description", ""),
            instructions=instructions,
            author=manifest.get("author", ""),
            license=manifest.get("license", ""),
            runtime=manifest.get("runtime", "universal"),
            keywords=manifest.get("keywords", []),
            capabilities=manifest.get("capabilities", []),
            dependencies=manifest.get("dependencies", {}),
            inputs=inputs,
            outputs=outputs,
            path=path,
            raw_manifest=manifest,
        )
    
    @staticmethod
    def from_url(skill_md_url: str, manifest_url: str = None) -> Skill:
        """Load a skill from remote URLs."""
        from urllib.request import urlopen, Request
        
        def fetch(url: str) -> str:
            req = Request(url, headers={"User-Agent": "skills-loader/1.0"})
            with urlopen(req, timeout=30) as response:
                return response.read().decode("utf-8")
        
        manifest = {}
        instructions = ""
        
        # Fetch manifest if URL provided
        if manifest_url:
            try:
                manifest = json.loads(fetch(manifest_url))
            except Exception:
                pass
        
        # Fetch SKILL.md
        content = fetch(skill_md_url)
        instructions, frontmatter = SkillLoader._parse_skill_md(content)
        manifest = {**manifest, **frontmatter}
        
        # Build skill ID from URL
        skill_id = manifest.get("id", "remote/skill")
        
        return Skill(
            id=skill_id,
            name=manifest.get("name", "Remote Skill"),
            version=manifest.get("version", "0.0.0"),
            description=manifest.get("description", ""),
            instructions=instructions,
            author=manifest.get("author", ""),
            license=manifest.get("license", ""),
            runtime=manifest.get("runtime", "universal"),
            keywords=manifest.get("keywords", []),
            capabilities=manifest.get("capabilities", []),
            dependencies=manifest.get("dependencies", {}),
            inputs=[],
            outputs=[],
            path=None,
            raw_manifest=manifest,
        )
    
    @staticmethod
    def from_catalog_entry(entry: Dict[str, Any], fetch_content: bool = True) -> Skill:
        """Load a skill from a catalog entry."""
        from urllib.request import urlopen, Request
        
        instructions = ""
        
        if fetch_content:
            source = entry.get("source", {})
            skill_md_url = source.get("skill_md_url")
            
            if skill_md_url:
                try:
                    req = Request(skill_md_url, headers={"User-Agent": "skills-loader/1.0"})
                    with urlopen(req, timeout=30) as response:
                        content = response.read().decode("utf-8")
                    instructions, _ = SkillLoader._parse_skill_md(content)
                except Exception:
                    pass
        
        return Skill(
            id=entry.get("id", "unknown/skill"),
            name=entry.get("name", "Unknown"),
            version=entry.get("version", "0.0.0"),
            description=entry.get("description", ""),
            instructions=instructions,
            author=entry.get("author", ""),
            license=entry.get("license", ""),
            runtime="universal",
            keywords=entry.get("tags", []),
            capabilities=[],
            dependencies={},
            inputs=[],
            outputs=[],
            path=None,
            raw_manifest=entry,
        )
    
    @staticmethod
    def _parse_skill_md(content: str) -> tuple[str, Dict[str, Any]]:
        """
        Parse SKILL.md content with YAML frontmatter.
        
        Returns (instructions, frontmatter_dict)
        """
        frontmatter = {}
        instructions = content
        
        # Check for YAML frontmatter (--- at start)
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    if HAS_YAML:
                        frontmatter = yaml.safe_load(parts[1]) or {}
                    else:
                        # Simple fallback parser for basic key: value pairs
                        for line in parts[1].strip().split("\n"):
                            if ":" in line:
                                key, val = line.split(":", 1)
                                frontmatter[key.strip()] = val.strip()
                except Exception:
                    pass
                instructions = parts[2].strip()
        
        return instructions, frontmatter


def load_skill(skill_id_or_path: str) -> Skill:
    """
    Load a skill by ID or path.
    
    If skill_id_or_path is a path, loads from that directory.
    If it's a skill ID, looks in installed locations.
    """
    path = Path(skill_id_or_path)
    
    # If it's a valid path, load from there
    if path.exists():
        return SkillLoader.from_directory(path)
    
    # Otherwise, search installed skills
    from cli.skills import get_installed_skills
    
    installed = get_installed_skills()
    if skill_id_or_path in installed:
        install_path = Path(installed[skill_id_or_path]["path"])
        return SkillLoader.from_directory(install_path)
    
    raise FileNotFoundError(f"Skill not found: {skill_id_or_path}")


def load_skills_from_dir(directory: Path) -> List[Skill]:
    """
    Load all skills from a directory.
    
    Scans for subdirectories containing skill.json or SKILL.md.
    """
    skills = []
    directory = Path(directory)
    
    if not directory.exists():
        return skills
    
    for entry in directory.iterdir():
        if not entry.is_dir():
            continue
        
        # Check if this looks like a skill directory
        has_skill = (entry / "skill.json").exists() or (entry / "SKILL.md").exists()
        
        if has_skill:
            try:
                skill = SkillLoader.from_directory(entry)
                skills.append(skill)
            except Exception:
                pass  # Skip invalid skills
        else:
            # Check for nested provider/skill structure
            for sub_entry in entry.iterdir():
                if sub_entry.is_dir():
                    has_skill = (sub_entry / "skill.json").exists() or (sub_entry / "SKILL.md").exists()
                    if has_skill:
                        try:
                            skill = SkillLoader.from_directory(sub_entry)
                            skills.append(skill)
                        except Exception:
                            pass
    
    return skills


# =============================================================================
# Runtime-specific helper functions
# =============================================================================

def create_mcp_resource_handler(skills_dir: Path) -> Callable:
    """
    Create an MCP resource handler that serves skills.
    
    Usage with MCP server:
        from mcp.server import Server
        from cli.loader import create_mcp_resource_handler
        
        server = Server("skills-server")
        handler = create_mcp_resource_handler(Path("~/.skills/installed"))
        
        @server.list_resources()
        async def list_resources():
            return handler.list()
        
        @server.read_resource()
        async def read_resource(uri):
            return handler.read(uri)
    """
    
    class MCPSkillHandler:
        def __init__(self, skills_dir: Path):
            self.skills_dir = Path(skills_dir).expanduser()
            self._cache: Dict[str, Skill] = {}
        
        def _load_skills(self):
            if not self._cache:
                skills = load_skills_from_dir(self.skills_dir)
                self._cache = {s.id: s for s in skills}
            return self._cache
        
        def list(self) -> List[Dict[str, Any]]:
            """List all skills as MCP resources."""
            skills = self._load_skills()
            return [skill.to_mcp() for skill in skills.values()]
        
        def read(self, uri: str) -> Dict[str, Any]:
            """Read a skill by URI."""
            # Parse skill:// URI
            if uri.startswith("skill://"):
                skill_id = uri[8:]  # Remove "skill://" prefix
            else:
                skill_id = uri
            
            skills = self._load_skills()
            if skill_id not in skills:
                raise KeyError(f"Skill not found: {skill_id}")
            
            return skills[skill_id].to_mcp()
    
    return MCPSkillHandler(skills_dir)


def export_skills_for_copilot(skills_dir: Path, output_file: Path) -> None:
    """
    Export skills as a combined instruction file for GitHub Copilot.
    
    Creates a markdown file that can be included in copilot-instructions.md.
    """
    skills = load_skills_from_dir(skills_dir)
    
    parts = ["# Loaded Skills", ""]
    
    for skill in skills:
        parts.append(f"## {skill.name}")
        parts.append("")
        parts.append(skill.to_system_prompt())
        parts.append("")
        parts.append("---")
        parts.append("")
    
    output_file.write_text("\n".join(parts))


def export_skills_for_claude(skills_dir: Path, output_file: Path) -> None:
    """
    Export skills as a combined instruction file for Claude.
    
    Creates a markdown file that can be used with CLAUDE.md.
    """
    skills = load_skills_from_dir(skills_dir)
    
    parts = ["# Agent Skills", ""]
    parts.append("The following skills are available for use:")
    parts.append("")
    
    for skill in skills:
        parts.append(f"## {skill.name} (v{skill.version})")
        parts.append("")
        if skill.description:
            parts.append(f"> {skill.description}")
            parts.append("")
        parts.append(skill.instructions)
        parts.append("")
    
    output_file.write_text("\n".join(parts))


if __name__ == "__main__":
    # Demo usage
    import sys
    
    if len(sys.argv) > 1:
        path = sys.argv[1]
        try:
            skill = load_skill(path)
            print(f"Loaded skill: {skill.id}")
            print(f"  Name: {skill.name}")
            print(f"  Version: {skill.version}")
            print(f"  Description: {skill.description}")
            print(f"  Runtime: {skill.runtime}")
            print(f"  Path: {skill.path}")
            print()
            print("MCP export:")
            print(json.dumps(skill.to_mcp(), indent=2))
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("Usage: python loader.py <skill-path-or-id>")
