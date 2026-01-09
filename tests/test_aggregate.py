import sys
from types import SimpleNamespace
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
    assert "Converter" in tags


def test_write_toon_output_uses_python_encoder(tmp_path, monkeypatch):
    # Provide a stub encoder to avoid CLI and the unimplemented upstream encoder
    monkeypatch.setattr(aggregate, "HAS_TOON", True)
    monkeypatch.setattr(aggregate, "toon_format", SimpleNamespace(encode=lambda data: "encoded"))

    output_dir = tmp_path
    catalog_json = output_dir / "catalog.json"
    catalog_json.write_text("{}", encoding="utf-8")

    aggregate.write_toon_output({"hello": "world"}, output_dir, catalog_json)

    toon_file = output_dir / "catalog.toon"
    assert toon_file.exists()
    assert toon_file.read_text(encoding="utf-8") == "encoded"