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

Next release will be **0.1.5**; subsequent releases increment the patch version (0.1.6, 0.1.7, ...).

## 0.1.5 - 2026-09-28

### Added

- `src/support_agent/memory.py` with `ConversationMemory` dataclass for managing conversation history
- `src/support_agent/agent.py` with `SupportAgent` class integrating memory with LLM calls and tool use
- `src/support_agent/state.py` with `AgentState` dataclass and `update_state_from_extraction()` function
- `src/support_agent/models.py` with `ExtractedTicket` and `CustomerMemory` models
- `src/support_agent/customer_memory.py` with in-memory customer memory store (`add_or_update_memory()`, `get_customer_memories()`, `delete_memory()`)
- `tests/test_memory.py` with 8 tests covering user messages, conversation history, clear memory, state extraction, memory creation, duplicate handling, value updates, and memory deletion

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