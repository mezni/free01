from __future__ import annotations

from io import BytesIO

from core.models import Block

from .registry import register


@register("application/pdf")
def parse(data: bytes) -> list[Block]:
    """Extract one paragraph block per non-empty line, keeping the page number.

    No OCR: scanned PDFs yield no text.
    """
    from pypdf import PdfReader

    reader = PdfReader(BytesIO(data))
    blocks: list[Block] = []
    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for line in text.splitlines():
            stripped = line.strip()
            if stripped:
                blocks.append(Block(kind="paragraph", text=stripped, page=number))
    return blocks
