from __future__ import annotations

from core.models import Block

from ._blocks import split_blocks
from .registry import register


@register("text/markdown")
def parse(data: bytes) -> list[Block]:
    return split_blocks(data.decode("utf-8", errors="replace"), allow_headings=True)
