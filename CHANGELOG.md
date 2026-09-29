# Changelog

All notable changes to this project will be documented in this file.

## Version History

| Version | Feature Domain      | Key Objectives                                                            |
| ------- | ------------------- | ------------------------------------------------------------------------ |
| 0.1.4   | LLM Integration | `ChatOpenRouter` client factory wired to settings; new `llm` package     |
| 0.1.3   | CLI: Ticket Listing | `triage-ai tickets` command rendering seed tickets from the JSON loader |
| 0.1.2   | Data Ingestion      | JSON ticket loader with Pydantic validation into `SupportTicket` objects |
| 0.1.1   | Domain Models       | Pydantic `SupportTicket` model with validation, unit tests               |
| 0.1.0   | Project Foundations | Scaffold layout, pydantic-settings config, Typer CLI, pytest suite        |

## Unreleased

Next release will be **0.1.6**; subsequent releases increment the patch version (0.1.7, 0.1.8, ...).

## 0.1.6 - 2026-09-28

### Added

- `src/support_agent/models.py` with `RetrievedMemory` model
- `src/support_agent/memory_retrieval.py` with `retrieve_relevant_memories()` and `format_retrieved_memories()` functions
- `tests/test_memory_retrieval.py` with 2 tests for memory retrieval and customer isolation

### Fixed

- N/A

## 0.1.5 - 2026-09-28

### Added

- `src/support_agent/memory.py` with `ConversationMemory` dataclass for managing conversation history
- `src/support_agent/agent.py` with `SupportAgent` class integrating memory with LLM calls and tool use
- `src/support_agent/state.py` with `AgentState` dataclass and `update_state_from_extraction()` function
- `src/support_agent/models.py` with `ExtractedTicket`, `CustomerMemory`, `MemoryCandidate`, and `MemoryExtractionResult` models
- `src/support_agent/prompts.py` with `MEMORY_EXTRACTION_SYSTEM_PROMPT`
- `src/support_agent/customer_memory.py` with in-memory customer memory store (`add_or_update_memory()`, `get_customer_memories()`, `delete_memory()`)
- `src/support_agent/memory_extraction.py` with `extract_memory_candidates()` function for LLM-based memory extraction
- `src/support_agent/memory_policy.py` with `should_store_memory()` policy function and constants (`MIN_MEMORY_CONFIDENCE`, `ALLOWED_MEMORY_KEYS`)
- `src/support_agent/memory_manager.py` with `process_message_for_memory()` to connect extraction, policy, and storage
- `tests/test_memory.py` with 8 tests covering user messages, conversation history, clear memory, state extraction, memory creation, duplicate handling, value updates, and memory deletion
- `tests/test_memory_extraction.py` with 3 tests for `MemoryCandidate` and `MemoryExtractionResult` models
- `tests/test_memory_policy.py` with 5 tests for `should_store_memory()` policy validation
- `tests/test_memory_manager.py` with 2 integration tests connecting extraction → policy → storage (using monkeypatched LLM)

### Fixed

- `update_state_from_extraction()` now handles both enum and string values for category and priority fields

## 0.1.2 - 2026-09-24

### Added

- `src/triage_ai/data` package with `loader.py` exposing `load_tickets()`.
- `load_tickets()` reads a JSON array and validates each entry into a `SupportTicket` model.

## 0.1.1 - 2026-09-24

### Added

- `SupportTicket` Pydantic model (`ticket_id`, `customer_id`, `subject`, `description`) with field validation.
- `tests/test_ticket.py` covering model creation and validation errors.

## 0.1.0 - 2026-09-24

### Added

- Project scaffold: `src/triage_ai`, `tests`, `data`, `prompts`, `docs` layout.
- Dependency management via `uv` (`pyproject.toml`, `uv.lock`).
- Configuration layer with `pydantic-settings` (`Settings` model, `.env` support).
- Typer CLI with `info` command and Rich output.
- CLI entry point `triage-ai` registered in `pyproject.toml`.
- `pytest` test suite covering configuration defaults.
- `.env.example` and `.gitignore` for local development.