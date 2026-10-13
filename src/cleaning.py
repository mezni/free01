from __future__ import annotations

import re
from collections import defaultdict

from core.models import Block

_PAGE_NUMBER = re.compile(r"^page \d+ of \d+$", re.IGNORECASE)
_LIGATURES = {
    "\ufb00": "ff",
    "\ufb01": "fi",
    "\ufb02": "fl",
    "\ufb03": "ffi",
    "\ufb04": "ffl",
}


def normalize_text(text: str) -> str:
    """Collapse whitespace and repair common PDF artefacts (ligatures, soft hyphens)."""
    text = text.replace("\u00ad", "")
    for ligature, replacement in _LIGATURES.items():
        text = text.replace(ligature, replacement)
    text = text.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip()


def clean(blocks: list[Block]) -> list[Block]:
    """Normalize blocks and drop noise.

    Removes empty blocks, bare page numbers and any text repeated on two or
    more pages (headers and footers).
    """
    normalized = [block.model_copy(update={"text": normalize_text(block.text)}) for block in blocks]
    normalized = [
        block for block in normalized if block.text and not _PAGE_NUMBER.match(block.text)
    ]

    pages_by_text: dict[str, set[int]] = defaultdict(set)
    for block in normalized:
        if block.page is not None:
            pages_by_text[block.text].add(block.page)

    repeated = {text for text, pages in pages_by_text.items() if len(pages) >= 2}
    return [block for block in normalized if block.text not in repeated]
