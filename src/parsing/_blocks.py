from __future__ import annotations

import re

from core.models import Block

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_CLAUSE = re.compile(r"^\d+(\.\d+)*\s")


def split_blocks(text: str, *, allow_headings: bool, page: int | None = None) -> list[Block]:
    """Turn raw text into blocks.

    A new block starts at a heading, a clause number (``2.1``) or after a line
    ending in ``.``, so clauses stay separate while a wrapped line that does not
    end a sentence is joined to the previous one.
    """
    blocks: list[Block] = []
    kind: str | None = None
    level: int | None = None
    lines: list[str] = []

    def flush() -> None:
        nonlocal kind, level, lines
        if lines:
            joined = " ".join(lines).strip()
            if joined:
                blocks.append(Block(kind=kind or "paragraph", text=joined, level=level, page=page))
        kind, level, lines = None, None, []

    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped:
            flush()
            continue
        if allow_headings:
            match = _HEADING.match(stripped)
            if match:
                flush()
                blocks.append(
                    Block(
                        kind="heading",
                        text=match.group(2).strip(),
                        level=len(match.group(1)),
                        page=page,
                    )
                )
                continue
        if _CLAUSE.match(stripped):
            flush()
            kind = "paragraph"
            lines = [stripped]
        else:
            if kind is None:
                kind = "paragraph"
            lines.append(stripped)
        if stripped.endswith("."):
            flush()
    flush()
    return blocks
