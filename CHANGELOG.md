# Changelog

## Version History

| Version | Feature Domain | Key Objectives |
|---------|----------------|----------------|
| 0.0.5 | Configuration & Pipeline Setup | Add pipeline configuration loader and ingestion_config.yaml for RAG pipeline setup |
| 0.0.4 | Metadata Processor | Add metadata processor with YAML frontmatter and validation for document fields |
| 0.0.3 | Parser Integration | Add file-to-markdown conversion pipeline for ingested documents |
| 0.0.2 | Parser Module Added | File input conversion to markdown for RAG pipeline ingestion |
| 0.0.1 | Project Scaffolding | Initial project structure and documentation framework |

## [0.0.5] - 2026-10-04
### Configuration & Pipeline Setup
- Add pipeline configuration loader and ingestion_config.yaml for RAG pipeline setup

### Added
- `config/ingestion_config.yaml` with full pipeline configuration (pipeline, ingestion, metadata, chunking, vector_store, generation, evaluation)
- `src/utils/config_loader.py` module with dataclasses for all config sections
- `IngestionPipelineConfig` with load_from_yaml(), from_dict(), to_dict() methods
- `tests/config_loader_test.py` with 3 tests for config loading/serialization
- `src/utils/__init__.py` to make utils a proper package

### Changed
- Moved `config_loader.py` to `src/utils/` for better organization

### Fixed
- Python path resolution for config loader tests

---

## [0.0.4] - 2026-10-04
### Metadata Processor
- Add metadata processor with YAML frontmatter and validation for document fields

### Added
- `src/pipelines/ingestion/processor.py` module with `DocumentMetadata` dataclass
- Required metadata fields: department, doc_type, version, effective_date, source, file_type, title, owner, privacy_level, audience
- `MetadataProcessor` class for adding YAML frontmatter to markdown content
- Automatic frontmatter replacement when existing frontmatter is present
- `create_from_file()` method to infer metadata from file paths
- `tests/processor_test.py` with comprehensive test coverage
- `tests/__init__.py` to make tests a proper package

### Changed
- Moved `test_loader.py` from `src/pipelines/ingestion/` to `tests/` as `loader_test.py`

### Fixed
- Python path resolution for tests

---

## [0.0.3] - 2026-10-02
### Parser Integration
- Add file-to-markdown conversion pipeline for ingested documents

### Added
- `loader.py` under `src/pipelines/ingestion/` with format-specific parsers
- `PDFLoader` with layout-aware extraction
- `WordLoader` for .docx documents
- `CSVLoader` converting tables to markdown
- `MarkdownLoader` for passthrough processing
- `LoaderFactory` with extension-based auto-dispatch
- Test suite for parser modules

### Changed
- Ingestion pipeline now supports multiple file formats

---

## [0.0.2] - 2026-10-02
### Parser Module Added
- File input conversion to markdown for RAG pipeline ingestion

### Added
- `src/pipelines/ingestion/loader.py` module
- `FileLoader` abstract base class
- `PDFLoader` for PDF documents
- `WordLoader` for .docx documents
- `CSVLoader` converting spreadsheets to markdown tables
- `MarkdownLoader` for markdown files
- `LoaderFactory` for format auto-detection and loading
- `tests/loader_test.py` and `tests/parser_test.py`

### Changed
- Project structure organized under `src/` directory
- Ingestion pipeline now supports multiple document formats

---

## [0.0.1] - 2026-10-02
### Project Scaffolding
- Initial project structure and documentation framework

### Added
- `mkdocs.yml` configuration with Material theme
- `docs/` directory structure with 6-section navigation
- `index.md` documentation homepage
- `README.md` project overview
- `PLAN.md` 6-phase roadmap
- `CHANGELOG.md` version history file
- `src/__init__.py` package foundation
- `src/utils/` utilities package
- Initial documentation sections
- `assets/diagrams/` and `assets/images/` directories
- Pytest as dev dependency via uv

### Changed
- None (initial scaffolding)

### Known Issues
- Documentation is skeletal; content to be added in subsequent releases
