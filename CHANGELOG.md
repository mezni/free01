# Changelog

All notable changes to this project will be documented in this file.

## [0.1.2] - 2026-10-13

### Added
- `Block` model carrying kind, text, heading level and page (`src/core/models.py`)
- Mime-based parser registry with `@register` decorator and `UnsupportedContentType` (`src/parsing/registry.py`)
- Markdown, plain-text and PDF parsers (`src/parsing/{markdown,text,pdf}.py`)
- `normalize_text()` (whitespace, ligatures, soft hyphens) and `clean()` dropping empty blocks, page numbers and text repeated on 2+ pages (`src/cleaning.py`)
- Parser/cleaning tests: `tests/test_parsing.py`, `tests/test_cleaning.py`, `tests/test_pdf.py`

### Changed
- Project is now an installable package (hatchling build backend, `package = true`), so `uv run python` can import the flat `src/` modules; reverses the earlier `package = false` decision

## [0.1.1] - 2026-10-13

### Added
- Synthetic telecom corpus with 5 Aether Wireless docs (billing, roaming, plans, network)
- Data manifest with version, plan_types, regions and effective dates
- Two roaming policy versions (v1 superseded, v2 current)
- Corpus tests: file existence, unique doc_id+version, valid dates, one current version per doc
- Stopped ignoring `data/raw/` directory
- `data/README.md` documenting manifest fields

## [0.1.0] - 2026-10-12

### Added
- Initial release
- `__version__ = "0.1.0"` in `src/rag/__init__.py`
- CLI entry point `triage` via `src/rag/cli.py`
- Smoke test `test_package_imports` in `tests/test_smoke.py`
- `.env.example` template
- `Makefile` with `install`, `test`, `lint`, `fmt`, `check` targets
- `.github/workflows/ci.yml` CI workflow