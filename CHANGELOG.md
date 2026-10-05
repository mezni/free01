# Changelog

All notable changes to this project are documented in this file. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Version History

| Version | Feature Domain | Key Objectives |
|---------|----------------|----------------|
| Unreleased | Documentation Foundation | Documentation homepage and MkDocs site configuration |
| 0.0.1 | Project Scaffolding | Initial project structure and documentation framework |

## [Unreleased]
### Documentation Foundation
- Documentation homepage and MkDocs site configuration

### Added
- `docs/mkdocs.yml` site configuration using `docs_dir: .` with output to `../site`
- Material for MkDocs theme with section navigation and copy-to-clipboard on code blocks
- `mkdocs-minify-plugin` for HTML minification
- `pymdownx.superfences` Mermaid fence support
- Navigation tree for the six planned sections, enabled as pages are authored
- `docs/index.md` documentation homepage with system overview, ingestion and query
  pipeline diagrams, repository layout, and local build instructions
- MkDocs toolchain installed into `.venv` via `uv pip install`

### Changed
- Documentation links on the homepage reference section pages as paths rather than
  markdown links, so `mkdocs build --strict` succeeds before those pages exist

### Known Issues
- Section pages are not authored yet; the navigation tree contains only Home
- `pyproject.toml` still declares an empty dependency list; the docs toolchain is not
  recorded as a dev dependency group

---

## [0.0.1] - 2026-10-02
### Project Scaffolding
- Initial project structure and documentation framework

### Added
- `pyproject.toml` defining the `telco-rag` package, version 0.1.0, requiring Python 3.12+
- `docs/` documentation root
- `README.md`, `PLAN.md`, and `CHANGELOG.md` placeholders
- `data/raw/` for raw ingested documents
- `.gitignore` covering virtualenvs, caches, logs, and editor artifacts
