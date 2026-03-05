import sys
from pathlib import Path


# Ensure project root is on path so we can import scripts.aggregate
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts import aggregate  # noqa: E402


def test_parse_skill_md_extracts_frontmatter_and_body():
    content = """---
name: Sample Skill
description: Does something
---
Body text here.
"""
    parsed = aggregate.parse_skill_md(content)
    assert parsed is not None
    assert parsed["frontmatter"]["name"] == "Sample Skill"
    assert "Body text" in parsed["body"]


def test_extract_tags_includes_keywords_and_name_words():
    tags = aggregate.extract_tags("PDF Converter", "Convert PDF to text")
    assert "pdf" in tags
    assert "convert" in tags
    assert "converter" in tags