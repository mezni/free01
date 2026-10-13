from __future__ import annotations

from collections.abc import Callable

from core.models import Block

Parser = Callable[[bytes], list[Block]]

_PARSERS: dict[str, Parser] = {}


class UnsupportedContentType(ValueError):
    """Raised when no parser is registered for a content type."""


def register(mime: str) -> Callable[[Parser], Parser]:
    """Register a parser for a given MIME type."""

    def decorator(func: Parser) -> Parser:
        _PARSERS[mime] = func
        return func

    return decorator


def get_parser(mime: str) -> Parser | None:
    return _PARSERS.get(mime)


def parse(data: bytes, mime: str) -> list[Block]:
    parser = get_parser(mime)
    if parser is None:
        raise UnsupportedContentType(mime)
    return parser(data)
