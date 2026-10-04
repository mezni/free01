# Changelog

## [0.0.8] - 2026-10-04
### Memory Layer
- Give the agent short-term conversation memory and per-customer long-term memory, and inject recalled customer context into the decision prompt

### Added
- Per-customer long-term memory storage
- Short-term conversation context tracking
- Decision prompt injection mechanism

### Changed
- Updated agent decision pipeline to include memory context
- Revised prompt templates to reference customer context

### Known Issues
- Live API calls may return Markdown prose instead of JSON for structured output
- Poolside/laguna-s-2.1:free model returns **Action:** prose rather than valid JSON

---

## [0.0.7] - 2026-10-02
### Knowledge Retrieval Layer
- Add an in-memory knowledge base with a retriever and a search tool; enforce the Tool contract on all tools

### Added
- In-memory knowledge base implementation
- Retriever component with search functionality
- Tool contract enforcement framework

### Changed
- All tools now implement the Tool interface
- Search integration updated for knowledge base access

### Known Issues
- TicketClassifier.classify still raises NotImplementedError unconditionally (see 0.0.6)

---

## [0.0.6] - 2026-10-02
### Tool Registry & Documentation
- Route agent actions through a pluggable tool registry; make the composition root explicit; bring both diagram documents up to date with the code

### Added
- Pluggable tool registry implementation
- Composition root configuration
- Updated diagram documents to match code state

### Changed
- Agent actions now routed through tool registry
- Diagram documents updated to reflect current code state

### Fixed
- ModuleNotFoundError: No module named 'tests' during collection (added __init__.py to tests package)

### Known Issues
- TicketClassifier.classify still raises NotImplementedError unconditionally
- ruff check: 3 pre-existing findings (unused pydantic.Field in domain/ticket.py, unused IncomingTicket in tests/domain/test_ticket.py, unused result in src/support_ops/classifier.py)
- Live API structured output failure: Model returns Markdown prose instead of JSON

---

## [0.0.5] - 2026-10-02
### Structured Output & Test Packaging
- Return typed agent decisions via OpenRouter structured output; make tests an importable package so test doubles can be shared.

### Added
- `LLMClient.structured(user_message, output_model)`, generic over TypeVar("T", bound=BaseModel). Calls chat.completions.parse with response_format=output_model and raises ValueError when the model returns no parsed object.
- `tests/__init__.py`, `tests/agent/__init__.py`, and `tests/domain/__init__.py`, making tests a regular package.
- `tests/agent/fakes.py` with a FakeLLM test double implementing structured, so agent tests do not require network access.

### Changed
- `SupportAgent.decide` now returns a typed `AgentDecision` via `llm.structured` instead of raising `NotImplementedError`. The prompt no longer requests raw JSON directly, relying on `response_format` for schema enforcement.
- `tests/agent/test_agent.py` uses the shared FakeLLM and now exercises `decide` in addition to `execute`.

### Fixed
- `ModuleNotFoundError: No module named 'tests'` during collection. `tests` had no `__init__.py`, so the dotted `tests.agent.fakes` import could not resolve.

### Known Issues
- The agent decision path fails against the live API. Verified against poolside/laguna-s-2.1:free: `SupportAgent.decide` raises `ValidationError: Invalid JSON: expected value at line 1 column 1` because the model returns Markdown prose (`**Action:** create_ticket ...`) instead of JSON. The unit test passes only because FakeLLM bypasses the transport entirely, so this is not covered by CI.
- Root cause is the prompt: `agent.py:19-40` no longer states the expected JSON shape. Re-adding an explicit `Return JSON with exactly these fields` block made the same live call succeed and return a validated `AgentAction.DRAFT_RESPONSE`. Relying on `response_format` alone is not sufficient for this model.
- `TicketClassifier.classify` (classifier.py:39) still raises `NotImplementedError` unconditionally and still calls `llm.chat` rather than `llm.structured`, so it is subject to the same failure above.
- `docs/sequence-diagram.md` was stale at this release: it stated that `SupportAgent.decide` raises `NotImplementedError` and that only `execute` is functional. Both were true at 0.0.4 but no longer hold. Corrected in 0.0.6.
- `ruff check` reports 3 pre-existing findings unrelated to this release: an unused pydantic.Field import in `domain/ticket.py`, an unused `IncomingTicket` import in `tests/domain/test_ticket.py`, and an unused `result` local in `src/support_ops/classifier.py`.

---

## [0.0.4] - 2026-10-02
### This release adds the missing agent decision types to the domain layer and documents the runtime with sequence diagrams.

### Added
- `AgentAction` (StrEnum) with `DRAFT_RESPONSE`, `CREATE_TICKET`, and `ESCALATE`, matching the action strings requested by the agent prompt in `agent.py`.
- `AgentDecision` (pydantic model) with `action: AgentAction` and `reason: str`. Verified that `AgentDecision.model_validate` parses the raw model string "create_ticket" into the enum and serializes back to JSON unchanged.
- `docs/sequence-diagram.md`: Mermaid sequence diagrams for configuration resolution, the inference path, agent tool dispatch, the unimplemented decision paths, and the outstanding wiring gap, plus a per-module status table.

### Fixed
- `ImportError: cannot import name 'AgentAction'` raised during test collection of `tests/agent/test_agent.py`. `agent.py` and the test both imported `AgentAction` and `AgentDecision` from `support_ops.domain.ticket`, but neither type existed anywhere in the repository, so the agent package could not be imported at all.

### Known Issues
- `TicketClassifier.classify` (classifier.py:39) still raises `NotImplementedError` unconditionally. See 0.0.6 for the live-API structured output failure that affected it once implemented.
- `ruff check` reports 3 pre-existing findings unrelated to this release: an unused pydantic.Field import in `domain/ticket.py`, an unused `IncomingTicket` import in `tests/domain/test_ticket.py`, and an unused `result` local in `src/support_ops/classifier.py`.

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
- Documentation structure updated to reflect parser capabilities

### Known Issues
- PDF parser is layout-aware but may require template adjustments for complex documents
- Word document parsing depends on proper file structure

---

## [0.0.2] - 2026-10-02
### Parser Module Added
- File input conversion to markdown for RAG pipeline ingestion

### Added
- `src/pipelines/ingestion/loader.py` module
- `FileLoader` abstract base class
- `PDFParser` with layout-aware extraction logic
- `WordDocumentParser` for .docx format
- `CSVTableParser` converting spreadsheets to markdown tables
- `MarkdownPassthrough` for existing markdown files
- `LoaderFactory` for format auto-detection and loading

### Changed
- Project structure reorganized under `src/` directory
- Ingestion pipeline now supports multiple document formats

### Known Issues
- Parser output formatting may require post-processing for complex layouts
- Initial release of parser module - additional format support planned for 0.0.3

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
- `docs/raw/` directory for source content
- Initial documentation sections: Architecture, Data Pipeline, Security, Quality, Operations, Developer Guides
- `assets/diagrams/` and `assets/images/` directories

### Changed
- None (initial scaffolding)

### Known Issues
- Documentation is skeletal; content to be added in subsequent releases
- Parser module not yet implemented (added in 0.0.2)
- No data connectors or integration pipelines configured